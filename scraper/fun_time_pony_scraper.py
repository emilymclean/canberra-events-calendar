import hashlib
from abc import ABC
from datetime import datetime, time, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

import pandas as pd
from icalendar import Event

from scraper.base import CsvScraper


class FunTimePonyScraper(CsvScraper):
    _date_format = "%Y-%m-%d"
    _time_format = "%I:%M %p"

    def id(self) -> str:
        return "fun-time-pony"

    def url(self) -> str:
        return "https://docs.google.com/spreadsheets/d/e/2PACX-1vTXz9JpgOiz7AAkQI3ad8yxilSdmROEYcT47HmfWpnRZe3sSLEl6ojwp950jFndzcxdHRICl9yYC5E4/pub?gid=260071046&single=true&output=csv"

    def _parse(self, event: Event, row: pd.Series) -> Optional[Event]:
        try:
            start_date = datetime.strptime(row['start_date'], self._date_format).date()
            try:
                start_date = datetime.combine(
                    start_date,
                    datetime.strptime(row['start_time'], self._time_format).time()
                )
            except Exception as e:
                start_date = datetime.combine(
                    start_date,
                    time(hour=20)
                )

        except Exception as e:
            return None

        try:
            end_date = datetime.strptime(row['end_date'], self._date_format).date()

            try:
                end_date = datetime.combine(
                    end_date,
                    datetime.strptime(row['start_time'], self._time_format).time()
                )
            except Exception as e:
                end_date = datetime.combine(
                    end_date,
                    time(hour=4) if end_date > start_date else time(hour=24)
                )
        except Exception as e:
            end_date = datetime.combine(
                start_date.date() + timedelta(days=1),
                time(hour=4)
            )

        event.uid = f"{self.id()}-{hashlib.md5(f"{row['title']}-{row['start_date']}".encode()).hexdigest()}"
        event.add("summary", row["title"])
        event.add("dtstart", start_date.replace(tzinfo=ZoneInfo('Australia/Sydney')))
        event.add("dtend", end_date.replace(tzinfo=ZoneInfo('Australia/Sydney')))
        event.add("location", "Fun Time Pony, 2/122 Alinga St, Canberra ACT 2601")
        event.add("description", row['description'])
        event.add("status", "CONFIRMED")

        return event
