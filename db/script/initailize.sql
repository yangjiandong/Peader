SET @saved_cs_client = @@character_set_client;
SET character_set_client = utf8;

CREATE DATABASE `rss_db` ;

USE `rss_db`;

DROP TABLE IF EXISTS `rss_users`;
CREATE TABLE `rss_users` (
	`id` MEDIUMINT(8) unsigned NOT NULL AUTO_INCREMENT,
	`email` VARCHAR(80) NOT NULL,
	`encrypted_password` CHAR(56) NOT NULL,
	`password_salt` CHAR(56) NOT NULL,
	`updated_at` TIMESTAMP NOT NULL,
	`created_at` TIMESTAMP NOT NULL,
	`actived` TINYINT(1) UNSIGNED NOT NULL DEFAULT 0,

	PRIMARY KEY (`id`),

	UNIQUE KEY (`email`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DEROP TABLE IF EXISTS `rss_sites`;
CREATE TABLE `rss_sites` (
	`url` VARCHAR(255) NOT NULL,
	`url_crc32` INT UNSIGNED NOT NULL DEFAULT 0,
	`name` VARCHAR(100)  NOT NULL,
	`content_md5` CHAR(32) NOT NULL DEFAULT "d41d8cd98f00b204e9800998ecf8427e",

	PRIMARY KEY (`url`)

)ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `rss_sites` ADD KEY (`url_crc32`);

DROP TABLE IF EXISTS `rss_site_entries`;
CREATE TABLE `rss_site_entries` (
	`id` BIGINT(20) unsigned NOT NULL AUTO_INCREMENT,
	`site_url`  VARCHAR(255) NOT NULL,
	`title` VARCHAR(255) NOT NULL,
	`author` VARCHAR(100) DEFAULT NULL,
	`link` VARCHAR(255) NOT NULL,
	`description` TEXT NOT NULL,
	`entry_md5` CHAR(32) NOT NULL,

	`updated_at` TIMESTAMP NOT NULL,
	`created_at` TIMESTAMP NOT NULL,

	PRIMARY KEY (`id`),
	FOREIGN KEY (`site_url`) REFERENCES `rss_sites` (`url`)
	
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `rss_site_entries` ADD UNIQUE KEY(`link`); 



DROP TABLE IF EXISTS `rss_user_feeds`;
CREATE TABLE `rss_user_feeds` (

	`user_id` MEDIUMINT(8) unsigned NOT NULL,
	`site_url`  VARCHAR(255) NOT NULL,
	`name` VARCHAR(100)  NOT NULL,
	`site_group` VARCHAR(100) DEFAULT NULL,
	
	`updated_at` TIMESTAMP NOT NULL,
	`created_at` TIMESTAMP NOT NULL,

	FOREIGN KEY (`user_id`) REFERENCES `rss_users` (`id`),
	FOREIGN KEY (`site_url`) REFERENCES `rss_sites` (`url`)

)ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `rss_user_feeds` ADD UNIQUE KEY(`user_id`, `site_url`);

DROP TABLE IF EXISTS `rss_user_entries`;
CREATE TABLE `rss_user_entries` (

	`entry_id` BIGINT(20) unsigned NOT NULL,
	`user_id` MEDIUMINT(8) unsigned NOT NULL,
	`site_url`  VARCHAR(255) NOT NULL,
	`read` TINYINT(1)	 UNSIGNED NOT NULL DEFAULT 0,
	`love`	 TINYINT(1)	 UNSIGNED NOT NULL DEFAULT 0,
	`tags` VARCHAR(255),

	FOREIGN KEY (`user_id`) REFERENCES `rss_users` (`id`),
	FOREIGN KEY (`site_url`) REFERENCES `rss_sites` (`url`),
	FOREIGN KEY (`entry_id`) REFERENCES `rss_site_entries` (`id`)
	

)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE  INDEX  id_url_index ON `rss_user_entries` (`user_id`, `site_url`);
CREATE  UNIQUE INDEX  user_entry_index ON `rss_user_entries` (`user_id`, `entry_id`);
ALTER TABLE `rss_user_entries` ADD KEY(`read`);


SET @@character_set_client = @saved_cs_clien8;


