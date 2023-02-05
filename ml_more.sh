#!/usr/bin/env bash
echo 'var'
cd ml_more
scrapy crawl ml -O data.csv
cd ..