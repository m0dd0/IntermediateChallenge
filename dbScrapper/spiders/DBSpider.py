import scrapy
import datetime
from helper import *
import time


class DBSpider(scrapy.Spider):
    name = "db"

    def __init__(self, url='', station='', **kwargs):
        self.start_url = url
        self.station = station
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        request = scrapy.Request(url=self.start_url, callback=self.parse)
        request.meta['station'] = self.station
        yield request

    def parse(self, response):
        # get the table from the response object
        table = response.css('table.result.stboard.dep tr')

        # iterate the table rows
        for row in table:
            # define the result object and fill it with data in subsequent steps
            yield {'station': response.meta['station'],
                   'time': row.css('td.time::text').get(),
                   'train': get_train(row),
                   'platform': get_platform(row),
                   'route': get_route(row),
                   'delayedTime': get_delay_time(row),
                   'information': get_info(row),
                   'timestampScraping': datetime.datetime.now()}
