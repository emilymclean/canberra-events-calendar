from icalendar import Event, Component

from scraper.base import ICalScraper


class GangGangScraper(ICalScraper):

    def id(self) -> str:
        return "ganggang"

    def url(self) -> str:
        return "https://ganggangcafe.com.au/events/?ical=1"

    def _modify(self, event: Event) -> Event:
        return event
