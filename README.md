# TorScrapyMYSQL (TSM)
Basic setup of using Scrapy with Tor and storing results in MYSQL database [Python Scrapy Framework](http://scrapy.org/).

Tested with setup with Debian 9.4 64-bit VM, Python 3.x, and Scrapy installed with pip3.

### Setup
##### 1. Execute install script

  ```
  bash setup.sh
  ```
  If you install everything the setup script asks for, you can start crawling Tor webpages immediately.

### Usage

Start crawling by typing:
```
scrapy crawl tsm
```

### View results

On the same computer, go to http://localhost/phpmyadmin in a browser, login and look at the tsm database.
The table *main* will contain information about the webpages scraped, but will not save the webpages by default. Light modification to the TSM/spiders/tsm.py file can allow you to save the webpage.
