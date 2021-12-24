#!/bin/bash

while true
do
    scrapy crawl db -o db_data_1.csv -a url="https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Karlsruhe&boardType=dep&start=Suche" -a station="Karlsruhe Hbf"
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Karlsruhe-Durlach&boardType=dep&start=Suche' -a station='Karlruhe Durlach'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Rastatt&boardType=dep&start=Suche' -a station='Rastatt'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Baden-Baden&boardType=dep&start=Suche' -a station='Baden-Baden'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Freudenstadt&boardType=dep&start=Suche' -a station='Freudenstadt'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Pforzheim&boardType=dep&start=Suche' -a station='Pforzheim'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Mühlacker&boardType=dep&start=Suche' -a station='Muehlacker'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Bretten&boardType=dep&start=Suche' -a station='Bretten'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Bruchsal&boardType=dep&start=Suche' -a station='Bruchsal'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Germersheim&boardType=dep&start=Suche' -a station='Germersheim'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Stuttgart&boardType=dep&start=Suche' -a station='Stuttgart'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Freiburg&boardType=dep&start=Suche' -a station='Freiburg'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Heidelberg&boardType=dep&start=Suche' -a station='Heidelberg'
    sleep 1
    scrapy crawl db -o db_data_1.csv -a url='https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Mannheim&boardType=dep&start=Suche' -a station='Mannheim'
    sleep 600
done