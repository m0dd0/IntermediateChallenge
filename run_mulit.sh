
#!/bin/bash

while true
do
  scrapy crawl db_multi_station -o ./data/db_data_2.csv -a stations="$(<./dbScrapper/stations.json)"
  sleep 600
done