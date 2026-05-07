import icalendar

from scraper.dissent_scraper import DissentScraper
from scraper.fun_time_pony_scraper import FunTimePonyScraper
from scraper.gang_gang_scraper import GangGangScraper
from scraper.smiths_scraper import SmithsAlternativeScraper

scrapers = [
    SmithsAlternativeScraper(),
    GangGangScraper(),
    DissentScraper(),
    FunTimePonyScraper(),
]

if __name__ == '__main__':
    cal = icalendar.Calendar()
    cal.add("X-WR-CALNAME", "Canberra Events Calendar")

    for scraper in scrapers:
        events = scraper.scrape()
        for event in events:
            cal.add_component(event)

    with open("events.ics", "wb") as f:
        f.write(cal.to_ical())
        f.close()
