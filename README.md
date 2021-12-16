# IntermediateChallenge

To run the scraper use a conda environment were you installed all packages from requirements.txt.

Then you can run the following command to get the results written in a .csv file:

```scrapy crawl db -o test2.csv -a url="https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?country=DEU&protocol=https:&rt=1&input=Karlsruhe&boardType=dep&start=Suche" -a station="Karlsruhe Hbf"```
