CREATE USER IF NOT EXISTS 'tsm'@'localhost' IDENTIFIED BY 'tsm';
GRANT ALL PRIVILEGES ON *.* TO 'tsm'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE DATABASE tsm DEFAULT CHARACTER SET 'utf8';
USE tsm;

CREATE TABLE `main` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `redirectURL` TEXT NOT NULL,
   `url` TEXT NOT NULL,
   `urlsFound` MEDIUMTEXT NOT NULL,
   `domain` TEXT NOT NULL,
   `title` TEXT NOT NULL,
   `h1` TEXT NOT NULL,
   `h2` TEXT NOT NULL,
   `timeFound` TEXT NOT NULL,
   PRIMARY KEY (`id`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` TEXT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO queue (id, url) VALUES (NULL, "http://mijpsrtgf54l7um6.onion/");
INSERT INTO queue (id, url) VALUES (NULL, "http://dirnxxdraygbifgc.onion/");
INSERT INTO queue (id, url) VALUES (NULL, "http://torlinkbgs6aabns.onion/");
INSERT INTO queue (id, url) VALUES (NULL, "http://gxamjbnu7uknahng.onion/");

CREATE TABLE `in_progress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` TEXT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `finished` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` TEXT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
