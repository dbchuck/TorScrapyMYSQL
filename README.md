# TorScrapyMYSQL
Basic setup of using Scrapy with Tor and storing results in MYSQL database [Python Scrapy Framework](http://scrapy.org/).

Tested with setup with Debian 9.3 64-bit VM, Python 3.x, and Scrapy installed with pip3.

### Setup
##### 1. Execute install script

  ```
  bash setup.sh
  ```

##### 2. Edit how many concurrent sessions:
Edit in ```MAX_INSTANCES``` TorScrapyMYSQL/start_scrapy_instances.sh

### Usage
To see what it does:
  ```
  bash start_scrapy_instances.sh
  ```
Or one session by:
```
scrapy crawl TorScrapyMYSQL
```

### View results

On the same computer, go to http://localhost/phpmyadmin in a browser, login and look at the TorScrapyMYSQL database.
