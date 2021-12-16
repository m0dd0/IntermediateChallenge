#!/bin/bash

while true
do
  scrapy crawl db -o test.csv
  sleep 10000
done