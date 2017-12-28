#!/bin/bash

MAX_INSTANCES=3

while [ true ]
do
  if [[ $MAX_INSTANCES > $(echo $(pgrep scrapy | wc -l)) ]]; then {
      scrapy crawl TorScrapyMYSQL &
      sleep 1 # Wait for scrapy process to remove url this process is working on
    }
  else {
    sleep 1
  }
  fi
done
