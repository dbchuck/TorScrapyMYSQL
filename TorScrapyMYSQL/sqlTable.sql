CREATE USER 'TorScrapyMYSQL'@'localhost' IDENTIFIED BY 'torScr4pingwith$crapy';
GRANT ALL PRIVILEGES ON *.* TO 'TorScrapyMYSQL'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE DATABASE TorScrapyMYSQL DEFAULT CHARACTER SET 'utf8';
USE TorScrapyMYSQL;

CREATE TABLE `main` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `redirectURL` TEXT NOT NULL,
   `url` TEXT NOT NULL,
   `urlsFound` MEDIUMTEXT NOT NULL,
   `domain` TEXT NOT NULL,
   `title` TEXT NOT NULL,
   `h1` TEXT NOT NULL,
   `h2` TEXT NOT NULL,
   `html_page` LONGTEXT NOT NULL,
   `words` MEDIUMTEXT NOT NULL,
   `dateFound` TEXT NOT NULL,
   PRIMARY KEY (`id`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

 CREATE TABLE `domain_stats` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `domain` TEXT NOT NULL,
   `num_pages` TEXT NOT NULL,
   PRIMARY KEY (`id`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `url_queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` TEXT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO url_queue (id, url) VALUES (NULL, "http://gxamjbnu7uknahng.onion/");
INSERT INTO url_queue (id, url) VALUES (NULL, "http://mijpsrtgf54l7um6.onion/");
INSERT INTO url_queue (id, url) VALUES (NULL, "http://dirnxxdraygbifgc.onion/");
INSERT INTO url_queue (id, url) VALUES (NULL, "http://torlinkbgs6aabns.onion/");

CREATE TABLE `url_in_progress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` TEXT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `url_finished` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` TEXT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
