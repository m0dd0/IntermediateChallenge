import scrapy
import datetime
from helper import *
import json


class DBSpider(scrapy.Spider):
    name = "db_multi_station"

    def __init__(self, stations, **kwargs):
        """Scrapes the data from the passed train stations

        Args:
            stations (str): A jsonified dict where each key is the name of a train station
                and the values the corresponding urls.
        """
        self.stations = json.loads(stations)
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        for station_name, url in self.stations.items():
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta["station"] = station_name
            yield request

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
