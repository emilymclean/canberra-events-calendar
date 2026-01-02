import hashlib

from icalendar import Event

from scraper.base import ICalScraper


class SmithsAlternativeScraper(ICalScraper):

    def id(self) -> str:
        return "smiths-alternative"

    def url(self) -> str:
        return "https://www.smithsalternative.com/infomaxim/api/v1/events/search.ics"

    def _modify(self, event: Event) -> Event:
        event.uid = f'{self.id()}-{hashlib.md5(f"{event.name}{event.DTSTART}{event.DTEND}{event.DTSTAMP}".encode()).hexdigest()}'
        return event
