import scrapy
import datetime
from helper import *
import time

class DBSpider(scrapy.Spider):
    name = "db"

    def start_requests(self):
        urls = [
            ['Karlsruhe Hbf',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Karlsruhe&boardType=dep&start=Suche'],
            ['Karlsruhe Durlach',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Karlsruhe-Durlach&boardType=dep&start=Suche'],
            ['Rastatt',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Rastatt&boardType=dep&start=Suche'],
            ['Baden Baden',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Baden-Baden&boardType=dep&start=Suche'],
            ['Freudenstadt',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Freudenstadt&boardType=dep&start=Suche'],
            ['Pforzheim Hbf',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Pforzheim&boardType=dep&start=Suche'],
            ['Mühlacker',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Mühlacker&boardType=dep&start=Suche'],
            ['Bretten',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Bretten&boardType=dep&start=Suche'],
            ['Bruchsal',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Bruchsal&boardType=dep&start=Suche'],
            ['Germersheim',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Germersheim&boardType=dep&start=Suche'],
            ['Stuttgart Hbf',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Stuttgart&boardType=dep&start=Suche'],
            ['Freiburg Hbf',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Freiburg&boardType=dep&start=Suche'],
            ['Heidelberg Hbf',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Heidelberg&boardType=dep&start=Suche'],
            ['Mannheim Hbf',
             'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Mannheim&boardType=dep&start=Suche'],
        ]

        for url in urls:
            request = scrapy.Request(url=url[1], callback=self.parse)
            request.meta['station'] = url[0]
            time.sleep(3)
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
