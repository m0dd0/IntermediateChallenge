import scrapy
from protego import Protego


class Dbspider(scrapy.Spider):
    name = 'dbSpider'

    start_urls = ['https://www.boerse.de/aktien/Apple-Aktie/US0378331005']
    #https://reiseauskunft.bahn.de/bin/bhftafel.exe

    def parse(self, response):
        print('INFO BEGIN:')
        print(response.css('.green::text').extract())
        #.pagetitle
        print('INFO END:')
