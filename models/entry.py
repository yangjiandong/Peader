#-*-coding:utf-8 -*-
#!/usr/bin/python


from model import Model
import hashlib
import MySQLdb
import logging

from time import strftime, gmtime


class Entry(Model):
    def __init__(self):

        Model.__init__(self)

    def _create(self, rss_entry, site_url):

        cursor = self.cursor()
        try:
            cursor.execute("INSERT INTO `rss_site_entries` VALUES(NULL, %s, %s, %s, %s, %s, %s, NULL, NULL)",
                           (site_url, rss_entry.title, rss_entry.author, rss_entry.link, rss_entry.description,
                            rss_entry.entry_md5 ))
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("Insert entry Failed error : %s", e.args[1])
            return False

        finally:
            cursor.close()

        return True

    @staticmethod
    def get_new_entries(site_url, created_at):

        entry = Entry()

        entries = entry.query("SELECT * FROM `rss_site_entries` WHERE `site_url` = %s AND `created_at` > %s", site_url,
                              created_at)

        return entries

    def _get_entry_md5(self):

        return hashlib.md5(self["title"] + self["description"]).hexdigest()

    def save(self):

        self.entry_md5 = self._get_entry_md5()
        cursor = self.cursor()
        try:
            cursor.execute("UPDATE `rss_site_entries` \
                        SET `title` = %s, `description` = %s, `entry_md5` = %s \
                        WHERE `id` = %s",
                           (self['title'], self['description'], self.entry_md5, self['id']))
            self.commit()
        except MySQLdb.Error, e:
            self.rollback()
            logging.error("Insert entry Failed error : %s", e.args[1])
            return False

        finally:
            cursor.close()

        return True


    @property
    def entry_md5(self):

        return self['entry_md5']

    @staticmethod
    def find_by_link(link):

        entry = Entry()
        cursor = entry.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, site_url, title, author, link, description, entry_md5 \
                           FROM `rss_site_entries`\
                           WHERE `link` = %s",
                           (link))
            entry._data = cursor.fetchone()
        except MySQLdb.Error, e:
            logging.error("find by link entry Failed error : %s", e.args[1])

        finally:
            cursor.close()

        return entry

    @staticmethod
    def create(rss_entry, site_url):

        entry = Entry()
        return entry._create(rss_entry, site_url)
        
        
        
        