import hashlib
import json
import re
from datetime import date, datetime, timedelta, time
from typing import List

import icalendar
import pytz
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from icalendar import Event

from scraper.base import WebScraper


def parse_human_date(text: str, today: date | None = None) -> date:
    """
    Parse dates like 'Friday, 12th December'.

    - Assumes current year
    - If resulting date is more than 10 months in the future,
      assumes previous year instead
    """
    if today is None:
        today = date.today()

    # Remove weekday and ordinal suffix (st/nd/rd/th)
    cleaned = re.sub(r'^\w+,\s*', '', text)  # remove weekday
    cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', cleaned)

    # Parse using current year
    current_year = today.year
    parsed = datetime.strptime(
        f"{cleaned} {current_year}",
        "%d %B %Y"
    ).date()

    # If more than 10 months in the future, roll back one year
    if parsed > today + relativedelta(months=10):
        parsed = parsed.replace(year=current_year - 1)

    return parsed


class FunTimePonyScraper(WebScraper):

    def id(self) -> str:
        return "ftp"

    def url(self) -> str:
        return "https://www.funtimepony.com.au/whatson"

    def _parse(self, document: BeautifulSoup) -> List[Event]:
        content = document.find("ul", class_="user-items-list-item-container").attrs['data-current-context']
        content = json.loads(content)
        # print(json.dumps(content, indent=2))

        events = []
        for event in content["userItems"]:
            description = BeautifulSoup(event["description"], features="html.parser")
            dt = datetime.combine(
                parse_human_date(description.find("p").get_text()),
                time=time(hour=20),
                tzinfo=pytz.timezone("Australia/Sydney")
            )

            out = icalendar.Event()
            out.add("uid", f"{self.id()}-{hashlib.md5(f"{event["title"]}{event["description"]}".encode()).hexdigest()}")
            out.add("summary", event["title"])
            out.add("description", event["description"])
            out.add("url", event["button"]["buttonLink"])
            out.add("dtstart", dt)
            out.add("dtend", dt + timedelta(hours=1))
            out.add("location", "Fun Time Pony, 2/122 Alinga St, Canberra ACT 2601")
            out.add("status", "CONFIRMED")
            events.append(out)

        return events

