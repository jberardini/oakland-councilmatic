from legistar.bills import LegistarBillScraper
from pupa.scrape import Bill, VoteEvent
from pupa.utils import _make_pseudo_id
import datetime
from collections import defaultdict
import pytz

class OaklandBillScraper(LegistarBillScraper):
	LEGISLATION_URL = 'https://oakland.legistar.com/Legislation.aspx'
	BASE_URL = 'https://oakland.legistar.com/'
	TIMEZONE = 'US/Pacific'

	#necessary?
	VOTE_OPTIONS = {'aye': 'yes',
					'excused': 'excused'
					'abstained': 'abstained'}


	#this probably needs to be customized
	SESSION_STARTS = (2014, 2010, 2006, 2002, 1996)

	def sessions(self, action_date):
		for session in self.SESSION_STARTS:
			if action_date >= datetime.datetime(session, 1, 1, 
												tzinfo=pytz.timezone(self.TIMEZONE))
				return str(session)


	def scrape(self):
		for leg_summary in self.legislation(created_after=datetime.datetime(2014, 1, 1)):
			leg_type = BILL_TYPES[leg_summary['Type']]

			bill = Bill(identifier=leg_summary['File\xa0#'],
						title=leg_summary['Title'],
						legislative_session=None,
						classification=leg_type,
						from_organization={'name':'Oakland City Council'})
			bill.add_source(leg_summary['url'], note='web')

			leg_details = self.legDetails(leg_summary['url'])
            history = self.history(leg_summary['url'])

            bill.add_title(leg_details['Name'], 
                           note='created by administrative staff')

            if 'Summary' in leg_details :
                bill.add_abstract(leg_details['Summary'], note='')

            #not a category for Oakland
            # if leg_details['Law number'] :
            #     bill.add_identifier(leg_details['Law number'], 
            #                         note='law number')

            
            #not sure where this is coming from
            for sponsorship in self._sponsors(leg_details.get('Sponsors', [])) :
                sponsor, sponsorship_type, primary = sponsorship
                bill.add_sponsorship(sponsor, sponsorship_type,
                                     'person', primary)


            #not sure where this is coming from
            for attachment in leg_details.get('Attachments', []) :
                           if attachment['label']:
                               bill.add_document_link(attachment['label'],
                                                      attachment['url'],
                                                      media_type="application/pdf")

                       history = list(history)

                       if history :
                           earliest_action = min(self.toTime(action['Date']) 
                                                 for action in history)

                           bill.legislative_session = self.sessions(earliest_action)
                       else :
                           bill.legislative_session = str(self.SESSION_STARTS[0])

                       for action in history :
                           action_description = action['Action']
                           if not action_description :
                               continue
                               
                           action_class = ACTION_CLASSIFICATION[action_description]

                           action_date = self.toDate(action['Date'])
                           responsible_org = action['Action\xa0By']
                           if responsible_org == 'City Council' :
                               responsible_org = 'New York City Council'
                           elif responsible_org == 'Administration' :
                               responsible_org = 'Mayor'
                              
                           if responsible_org == 'Town Hall Meeting' :
                               continue
                           else :
                               act = bill.add_action(action_description,
                                                     action_date,
                                                     organization={'name': responsible_org},
                                                     classification=action_class)

                           if 'url' in action['Action\xa0Details'] :
                               action_detail_url = action['Action\xa0Details']['url']
                               if action_class == 'committee-referral' :
                                   action_details = self.actionDetails(action_detail_url)
                                   referred_committee = action_details['Action text'].rsplit(' to the ', 1)[-1]
                                   act.add_related_entity(referred_committee,
                                                          'organization',
                                                          entity_id = _make_pseudo_id(name=referred_committee))
                               result, votes = self.extractVotes(action_detail_url)
                               if result and votes :
                                   action_vote = VoteEvent(legislative_session=bill.legislative_session, 
                                                      motion_text=action_description,
                                                      organization={'name': responsible_org},
                                                      classification=action_class,
                                                      start_date=action_date,
                                                      result=result,
                                                      bill=bill)
                                   action_vote.add_source(action_detail_url, note='web')

                                   for option, voter in votes :
                                       action_vote.vote(option, voter)


                                   yield action_vote
                       
                       text = self.text(leg_summary['url'])

                       if text :
                           bill.extras = {'local_classification' : leg_summary['Type'],
                                          'full_text' : text}
                       else :
                           bill.extras = {'local_classification' : leg_summary['Type']}

                       yield bill


               def _sponsors(self, sponsors) :
                   for i, sponsor in enumerate(sponsors) :
                       if i == 0 :
                           primary = True
                           sponsorship_type = "Primary"
                       else :
                           primary = False
                           sponsorship_type = "Regular"
                       
                       sponsor_name = sponsor['label']
                       if sponsor_name.startswith(('(in conjunction with',
                                                   '(by request of')) :
                           continue 

                       yield sponsor_name, sponsorship_type, primary
             
          #where to classify informational report / ordinance? 
          #leaving off informational report for now             

           BILL_TYPES = {
                         'City Resolution': 'resolution',
                         'Ordinance': 'ordinance'
                         }


           ACTION_CLASSIFICATION = {
               'No Action Taken': 'deferred',
               'Scheduled': None
           }

