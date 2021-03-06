from legistar.events import LegistarEventsScraper
from pupa.scrape import Event
from collections import deque

import datetime
import re

class OaklandEventsScraper(LegistarEventsScraper):
    TIMEZONE = 'America/Pacific'
    EVENTSPAGE = "https://oakland.legistar.com/Calendar.aspx"
    BASE_URL = "'https://oakland.legistar.com/'"

    def scrape(self):
            last_events = deque(maxlen=10)
            for event, agenda in self.events(since=2011) :
                other_orgs = ''
                extras = []

                #this whole block needs to be reconfigured. Joint meetings are indicated
                #in the name column
                # if '--em--' in event[u'Meeting Location'] :
                #     location_string, note = event[u'Meeting Location'].split('--em--')[:2]
                #     for each in note.split(' - ') :
                #         if each.startswith('Concurrent') :
                #             other_orgs = each
                #         else :
                #             extras.append(each)
                else :
                    location_string = event[u'Meeting Location'] 
                
                location_list = location_string.split('-', 2)
                location = ', '.join([each.strip() for each in location_list[0:2]])
                if not location :
                    continue

                when = self.toTime(event[u'Meeting Date'])

                #this might be a problem. Slightly different format for NYC
                #not sure we need this anyway
                event_time = event['iCalendar'].subcomponents[0]['DTSTART'].dt
                when = when.replace(hour=event_time.hour,
                                    minute=event_time.minute)

                time_string = event['Meeting Time']
                if time_string in ('Deferred',) :
                    status = 'cancelled'
                elif self.now() < when :
                    status = 'confirmed'
                else :
                    status = 'passed'

                #not part of Oakland site
                # description = event['Meeting\xa0Topic']
                # if any(each in description 
                #        for each 
                #        in ('Multiple meeting items',
                #            'AGENDA TO BE ANNOUNCED')) :
                #     description = ''

                event_name = event['Name']

                event_id = (event_name, when)

                if event_id in last_events :
                    continue
                else :
                    last_events.append(event_id)

                #setting description to blank, since I'm not sure where we should pull from
                e = Event(name=event_name,
                          start_time=when,
                          timezone=self.TIMEZONE,
                          description="",
                          location_name=location,
                          status=status)

                if extras :
                    e.extras = {'location note' : ' '.join(extras)}

                #media type is probably wrong
                if event['Video'] != 'Not\xa0available' : 
                    e.add_media_link(note='Recording',
                                     url = event['Video']['url'],
                                     type="recording",
                                     media_type = 'text/html')

                self.addDocs(e, event, 'Agenda')
                self.addDocs(e, event, 'Minutes')

                #what's the Oakland equivalent of City Council Stated Meeting?
                if event['Name'] == 'City Council Stated Meeting' :
                    participating_orgs = ['New York City Council']
                elif 'committee' in event['Name'].lower() :
                    participating_orgs = [event["Name"]]
                else :
                    participating_orgs = []

                #see comment on line 19
                # if other_orgs : 
                #     other_orgs = re.sub('Jointl*y with the ', '', other_orgs)
                #     participating_orgs += re.split(' and the |, the ', other_orgs)
     
                # for org in participating_orgs :
                #     e.add_committee(name=org)

                if agenda :
                    e.add_source(event["Meeting Details"]['url'], note='web')

                    
                    for item, _, _ in agenda :
                        if item["Name"] :
                            agenda_item = e.add_agenda_item(item["Name"])
                            if item["File\xa0#"] :
                                if item['Action'] :
                                    note = item['Action']
                                else :
                                    note = 'consideration'
                                agenda_item.add_bill(item["File\xa0#"]['label'],
                                                     note=note)
                else :
                    e.add_source(self.EVENTSPAGE, note='web')

                yield e
   