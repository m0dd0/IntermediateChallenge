import scrapy


class QuotesSpider(scrapy.Spider):
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
            request.meta['time'] = url[0]
            yield request


    def parse(self, response):
        table = response.css('table.result.stboard.dep tr')

        for row in table:

            result = {'station': response.meta['station'], 'time': row.css('td.time::text').get(), 'train': row.css('td.train a::text').get(), 'platform': '', 'route': '', 'delayTime': '',
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
                result['information'] = row.css('td.ris span.delay.bold::text').get()

            result['delayTime'] = delayTime

            for key in result:
                if isinstance(result[key], str):
                    result[key] = " ".join(result[key].split())

            yield result

        #for entry in response.css('table.result.stboard.dep').get():

            #print(entry)
