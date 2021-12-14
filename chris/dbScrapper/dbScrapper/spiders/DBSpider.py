import scrapy


class QuotesSpider(scrapy.Spider):
    name = "db"

    def start_requests(self):
        urls = [
            ['Karlsruhe Hbf', 'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Karlsruhe&boardType=dep&start=Suche'],
            ['Rastatt', 'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Rastatt&boardType=dep&start=Suche']
        ]
        for url in urls:
            request = scrapy.Request(url=url[1], callback=self.parse)
            request.meta['station'] = url[0]
            yield request


    def parse(self, response):
        table = response.css('table.result.stboard.dep tr')

        for row in table:

            result = {'station': response.meta['station'], 'train': row.css('td.train a::text').get(), 'platform': '', 'route': '', 'delayTime': '',
                      'information': ''}

            try:
                result['route'] = row.css('td.route::text').getall()[2]
            except:
                result['route'] = ''

            platform = row.css('td.platform strong::text').get()
            if platform is None:
                platform = row.css('td.platform strong span.red::text').get()
                if platform is None:
                    try:
                        platform = row.css('td.platform::text').getall()[1]
                    except:
                        platform = ''
            result['platform'] = platform

            delayTime = row.css('td.ris span.delay.bold::text').get()

            if delayTime == '':
                delayTime = row.css('td.ris span.red::text').get()
                result['delayReason'] = row.css('td.ris span.delay.bold::text').get()

            result['delayTime'] = delayTime

            for key in result:
                if isinstance(result[key], str):
                    result[key] = " ".join(result[key].split())

            yield result

        #for entry in response.css('table.result.stboard.dep').get():

            #print(entry)
