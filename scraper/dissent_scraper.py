from icalendar import Event, Component

from scraper.base import ICalScraper, HumanitixScraper


class DissentScraper(HumanitixScraper):

    def id(self) -> str:
        return "dissent"

    def url(self) -> str:
        return "https://collections.humanitix.com/dissent-gigs"
