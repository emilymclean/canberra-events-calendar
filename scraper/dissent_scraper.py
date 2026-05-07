from icalendar import Event, Component

from scraper.base import ICalScraper, HumanitixScraper


class DissentScraper(HumanitixScraper):

    def id(self) -> str:
        return "dissent"

    def url(self) -> str:
        return "https://collections.humanitix.com/dissent-gigs"

    def _modify(self, event: Event) -> Event:
        event.add("organizer", "Dissent Cafe and Bar")
        return event


