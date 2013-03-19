DELIMITER $$
DROP TRIGGER IF EXISTS `UserCreateADDDefaultFeeds`;
CREATE TRIGGER `UserCreateADDDefaultFeeds` AFTER INSERT ON `rss_users`
FOR EACH ROW BEGIN
INSERT INTO `rss_user_feeds` VALUES 
(NEW.id, "http://www.xiami.com/collect/feed",  "虾米", "音乐", NULL, NULL),
(NEW.id, "http://feed.36kr.com/c/33346/f/566026/index.rss",  "果壳", "科技", NULL, NULL),
(NEW.id, "http://www.alibuybuy.com/feed", "互联网的那点事", "科技",  NULL, NULL),
(NEW.id, "http://rss.jiaren.org/", "佳人", "其他", NULL, NULL),
(NEW.id, "http://feed.feedsky.com/yeeyan", "译言", "其他",  NULL, NULL),
(NEW.id, "http://www.ppurl.com/feed", "皮皮书屋", "其他",  NULL, NULL),
(NEW.id, "http://www.infzm.com/rss/home/rss2.0.xml",  "南方周末", NULL, NULL, NULL);
END$$
DELIMITER ;

INSERT INTO `rss_user_feeds` 
VALUES(1, "http://www.xiami.com/collect/feed",  "虾米", "音乐", NULL, NULL),
(1, "http://feed.36kr.com/c/33346/f/566026/index.rss",  "果壳", "科技", NULL, NULL),
(1, "http://www.alibuybuy.com/feed", "互联网的那点事", "科技",  NULL, NULL),
(1, "http://rss.jiaren.org/", "佳人", "其他", NULL, NULL),
(1, "http://feed.feedsky.com/yeeyan", "译言", "其他",  NULL, NULL),
(1, "http://www.ppurl.com/feed", "皮皮书屋", "其他",  NULL, NULL),
(1, "http://www.infzm.com/rss/home/rss2.0.xml",  "南方周末", NULL, NULL, NULL);


insert into rss_db.rss_sites values
("http://www.alibuybuy.com/feed", crc32("http://www.alibuybuy.com/feed"), "互联网的那点事", "d41d8cd98f00b204e9800998ecf8427e"),
("http://rss.jiaren.org/", crc32("http://rss.jiaren.org/"), "佳人", "d41d8cd98f00b204e9800998ecf8427e"),
("http://feed.feedsky.com/yeeyan",crc32("http://feed.feedsky.com/yeeyan"), "译言", "d41d8cd98f00b204e9800998ecf8427e"),
("http://www.ppurl.com/feed", crc32("http://www.ppurl.com/feed"), "皮皮书屋", "d41d8cd98f00b204e9800998ecf8427e");

delete from `rss_user_sites` ;

SELECT  `rss_user_entries`.`entry_id`, `title`, `link`, `description`, `created_at` , `read`, `love`
FROM `rss_user_entries` INNER JOIN `rss_site_entries` ON `rss_user_entries`.`entry_id` = `rss_site_entries`.`id`
WHERE user_id = 1 and `rss_user_entries`.`site_url` = "http://feed.36kr.com/c/33346/f/566026/index.rss"
ORDER BY `rss_site_entries`.`created_at` DESC
LIMIT 0, 20;

SELECT  `rss_user_entries`.`entry_id`, `title`, `link`, `description`, `created_at` , `read`, `love`
FROM `rss_user_entries` INNER JOIN `rss_site_entries` ON `rss_user_entries`.`entry_id` = `rss_site_entries`.`id`
WHERE user_id = 1 AND `rss_user_entries`.`love` = 1
ORDER BY `rss_site_entries`.`created_at` DESC
LIMIT 0, 20;


SELECT  `rss_user_entries`.`entry_id`, `title`, `link`, `description`, `created_at` , `read`, `love` 
                           FROM `rss_user_entries` INNER JOIN `rss_site_entries` ON `rss_user_entries`.`entry_id` = `rss_site_entries`.`id` 
                           WHERE user_id = 1  AND `rss_user_entries`.`love`= 1 
                           ORDER BY `rss_site_entries`.`created_at` DESC 
                           LIMIT 0, 20












