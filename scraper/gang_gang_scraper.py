from icalendar import Event, Component

from scraper.base import ICalScraper


class GangGangScraper(ICalScraper):

    def id(self) -> str:
        return "ganggang"

    def url(self) -> str:
        return "https://ganggangcafe.com.au/events/?ical=1"

    def _modify(self, event: Event) -> Event:
        if event.get("location") is None:
            event.add("location", "Gang Gang Cafe, Shop 4/2 Frencham Pl, Downer ACT 2602")
        return event
