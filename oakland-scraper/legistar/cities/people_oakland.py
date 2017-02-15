from pupa.scrape import Person, Organization
from legistar.people import LegistarPersonScraper
import datetime

class OaklandPersonScraper(LegistarPersonScraper):
    MEMBERLIST = ''
    TIMEZONE = 'US/Pacific'
    ALL_MEMBERS = "3:2"