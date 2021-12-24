import scrapy
import datetime
from helper import *
import time
import json


class DBSpider(scrapy.Spider):
    name = "db_multi_station"

    def __init__(
        self,
        stations,
        stations_interval: int = 1,
        scraping_interval: int = 600,
        **kwargs
    ):
        """Scrapes the data from the passed train stations

        Args:
            stations (str): A jsonified dict where each key is the name of a train station
                and the values the corresponding urls.
            stations_interval (int, optional): The delay between each request of a
                different station. Defaults to 1.
            scraping_interval (int, optional): The interval after which all stations get
                scraped again. If negative they get only scraped once. Defaults to 600.
        """
        self.stations = json.loads(stations)
        self.stations_interval = stations_interval
        self.scraping_interval = scraping_interval
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        while True:
            for station_name, url in self.stations.items():
                request = scrapy.Request(url=url, callback=self.parse)
                request.meta["station"] = station_name
                yield request
                time.sleep(self.stations_interval)
            if self.scraping_interval < 0:
                break
            time.sleep(self.scraping_interval)

    def parse(self, response):
        # get the table from the response object
        table = response.css("table.result.stboard.dep tr")

        # iterate the table rows
        for row in table:
            # define the result object and fill it with data in subsequent steps
            yield {
                "station": response.meta["station"],
                "time": row.css("td.time::text").get(),
                "train": get_train(row),
                "platform": get_platform(row),
                "route": get_route(row),
                "delayedTime": get_delay_time(row),
                "information": get_info(row),
                "timestampScraping": datetime.datetime.now(),
            }
