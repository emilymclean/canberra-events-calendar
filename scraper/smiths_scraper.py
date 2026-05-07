import hashlib

from icalendar import Event

from scraper.base import ICalScraper


class SmithsAlternativeScraper(ICalScraper):

    def id(self) -> str:
        return "smiths-alternative"

    def url(self) -> str:
        return "https://www.smithsalternative.com/infomaxim/api/v1/events/search.ics"

    def _modify(self, event: Event) -> Event:
        event.uid = f'{self.id()}-{hashlib.md5(f"{event.name}{event.DTSTART}{event.DTEND}".encode()).hexdigest()}'
        event.pop("location")
        event.add("location", "Smiths Alternative, 76 Alinga St, Canberra ACT 2601")
        event.add("organizer", "Smiths Alternative")
        return event
