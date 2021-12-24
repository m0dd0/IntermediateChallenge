import scrapy
import datetime
from helper import *
import time
import json


class DBSpider(scrapy.Spider):
    name = "multi_station"

    def __init__(self, stations=None, sleep=1, **kwargs):
        self.stations = json.loads(stations)
        self.sleep = sleep
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        for station_name, url in self.stations.items():
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta["station"] = self.station
            yield request
            time.sleep(self.sleep)

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
