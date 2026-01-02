import datetime
import re
import urllib
from abc import ABC, abstractmethod
from typing import List
from urllib.request import urlopen, Request
import json

import dateutil.parser
import dirtyjson
import icalendar
import urllib3
from bs4 import BeautifulSoup
from icalendar import Event, Calendar


class Scraper(ABC):

    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def scrape(self) -> List[Event]:
        pass


class ICalScraper(Scraper, ABC):

    @abstractmethod
    def url(self) -> str:
        pass

    def _modify(self, event: Event) -> Event:
        return event

    def _modify_internal(self, event: Event) -> Event:
        event.uid = f"{self.id()}-{event.uid}"
        return self._modify(event)

    def scrape(self) -> List[Event]:
        req = Request(self.url())
        req.add_header('Accepts', 'text/calendar')

        calendar_str = urlopen(req).read().decode("utf-8")
        calendar = Calendar.from_ical(calendar_str)
        return [self._modify_internal(e) for e in calendar.events]


class WebScraper(Scraper, ABC):

    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    def _parse(self, document: BeautifulSoup) -> List[Event]:
        pass

    def scrape(self) -> List[Event]:
        html = urllib3.request(
            "GET",
            self.url(),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/31.0.1650.16 Safari/537.36"
            }
        ).data

        return self._parse(BeautifulSoup(html, features="html.parser"))


class HumanitixScraper(WebScraper, ABC):

    def _modify(self, event: Event) -> Event:
        return event

    def _parse(self, document: BeautifulSoup) -> List[Event]:
        data = re.findall("id:\"([\\w\\d]+)\"", next((x for x in (
            document.find_all('script')[-2].get_text().strip().splitlines()) if x.strip().startswith("data: ")
        )).strip()[len("data: "):], re.DOTALL)
        print(data)
        print(urllib.parse.quote(
                json.dumps({
                    "0": {
                        "eventIds": data
                    },
                    "skip": 0,
                    "limit": 100,
                    "stackRecurring": True,
                    "showPastEvents": True,
                    "privacyLevel": "public",
                    "userTimezone": "UTC",
                    "tabType": "month",
                    "tabData": "2026-03",
                    "searchFilters": {
                        "hosts": [],
                        "accessibilityValues": [],
                        "tags": []
                    }
                })
            ))

        events_json = urllib3.request(
            "GET",
            f"https://collections.humanitix.com/trpc/events.getEventsFromIds?batch=1&input={urllib.parse.quote(
                json.dumps({
                    "0": {
                        "eventIds": data,
                        "skip": 0,
                        "limit": 100,
                        "stackRecurring": True,
                        "showPastEvents": True,
                        "privacyLevel": "public",
                        "userTimezone": "UTC",
                        "searchFilters": {
                            "hosts": [],
                            "accessibilityValues": [],
                            "tags": []
                        }
                    }
                })
            )}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/31.0.1650.16 Safari/537.36"
            }
        ).data
        events_json = json.loads(events_json)

        events = []

        for event in events_json[0]["result"]["data"]["events"]:
            dt = dateutil.parser.isoparse(event["dates"]["timeTagDate"])

            out = icalendar.Event()
            out.add("uid", f"{self.id()}-{event["id"]}")
            out.add("summary", event["title"])
            out.add("dtstart", dt)
            out.add("dtend", dt + datetime.timedelta(hours=1))
            out.add("location", event["location"]["displayLocation"])
            out.add("status", "CONFIRMED")
            events.append(self._modify(out))

        return events

