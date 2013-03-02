SET @saved_cs_client = @@character_set_client;
SET character_set_client = utf8;

CREATE DATABASE `rss_db` ;

USE `rss_db`;

DROP TABLE IF EXISTS `rss_users`;
CREATE TABLE `rss_users` (
	`id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
	`email` varchar(80) NOT NULL,
	`encrypted_password` CHAR(56) NOT NULL,
	`password_salt` CHAR(56) NOT NULL,
	`updated_at` TIMESTAMP,
	`created_at` TIMESTAMP,
	`actived` tinyint(1) unsigned NOT NULL DEFAULT 0,

	PRIMARY KEY (`id`),

	UNIQUE KEY (`email`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;







SET @@character_set_client = @saved_cs_clien8;


