# -*- coding: utf-8 -*-
"""
Anything related to the DB.
Includes the classes for Anime and Config.
"""
__author__ = 'Sohhla'


import re
import sqlite3
from log import LoggerManager
import constant
from strings import escape_unicode


class DBManager():
    """
    Controls access to the SQLite DB.
    DB is located at the path defined by constant.DB_PATH.
    """

    def __init__(self):
        self.re_words = re.compile("(\w+)")
        self.number_of_anime_enabled = 0
        self.log = LoggerManager().get_logger("DB Manager")
        self.conn = sqlite3.connect(constant.DB_PATH)
        self.__update_db()

    def __update_db(self):
        """
        Update an old DB to the latest version.
        :return: none
        """
        db = self.__read_table("config")
        try:
            db_version = db[0]["dbVersion"]  # v4 or later
        except KeyError:
            db_version = db[0]["dbversion"]  # v3 or earlier
        if db_version==3:
            """
            Update to 4 (Nov 06 2014):
                - config: added column "preferRss" (type=numeric, default=1)
            """
            c = self.conn.cursor()
            c.execute("ALTER TABLE config ADD COLUMN preferRss NUMERIC")
            c.execute("UPDATE config SET preferRss=1")
            c.execute("UPDATE config SET dbversion=4")
            self.conn.commit()
            c.close()
        if db_version==4:
            """
            Update to 5 (Mar 30 2015):
                - config: removed some columns, renamed others
            """
            c = self.conn.cursor()
            c.execute("START TRANSACTION")
            c.execute("ALTER TABLE config RENAME TO old_config")
            c.execute("CREATE TABLE config (showNotification INT,sleepTime INT,preferRss INT,useDefaultApp INT,appPath TEXT,"
                      "animeFolder TEXT,firstUse INT,dbVersion INT )")
            c.execute("INSERT INTO config (showNotification,sleepTime,preferRss,appPath,animeFolder,firstUse) "
                      "SELECT notifyWhenDownloadFile,sleepTime,preferRss,uTorrentPath,uTorrentDefaultContentDownloadFolder,firstUse FROM old_config")
            c.execute("DROP TABLE old_config")
            c.execute("UPDATE config SET useDefaultApp=0")
            c.execute("UPDATE config SET dbVersion=5")
            c.execute("COMMIT")
            self.conn.commit()
            c.close()
        # If the DB is modified again, add another IF here to update previous versions

    def __read_table(self,table):
        """
        Reads all data from the given table.

        :type table: str
        :param table: Name of the table.

        :rtype: dict
        :return:
            Dictionary with all data from the table.
            The dictionary has the following format: dic[line_number (int)][column_name (str)]
        """
        try:
            __c = self.conn.cursor()
            __c.execute("SELECT * FROM %s" % table)
            results = []
            for row in __c:
                results.append(row)
            dic = {}
            for count in range(len(results)):
                temp_dic = {}
                for column in range(len(__c.description)):
                    temp_dic[__c.description[column][0]] = results[count][column]
                dic[count] = temp_dic
            __c.close()
            return dic
        except Exception as error:
            self.log.print_traceback(error,self.log.error)

    def update_registry(self,table,column,new_value,pk_column=None,pk_value=None):
        """
        Update a line from a table.

        :type table: str
        :param table: Name of the table.

        :type column: str
        :param column: Name of the column.

        :type new_value: int or str
        :param new_value: Value the registry will be updated to.

        :type pk_column: str
        :param pk_column: Primary Key column, used to identify a single line from the table.

        :type pk_value: int or str
        :param pk_value: Primary Key column value that uniquely identifies a single line from the table.
        """
        __c = self.conn.cursor()
        try:  #if OK, then new_value is an integer
            int(new_value)
            value = "%d" % new_value
        except ValueError:  #otherwise it's text
            value = "'%s'" % new_value
        if pk_column is None:
            __c.execute("UPDATE %s SET %s=%s" % (table,column,value))
        else:
            __c.execute("UPDATE %s SET %s=%s WHERE %s='%s'" % (table,column,value,pk_column,pk_value))
        self.conn.commit()

    def get_config(self):
        """
        Reads 'config' table from DB.

        :rtype: Config
        :return: All config data.
        """
        db = self.__read_table("config")
        config = Config(show_notification = bool(db[0]["showNotification"]),
                        sleep_time        = db[0]["sleepTime"],
                        prefer_rss        = bool(db[0]["preferRss"]),
                        use_default_app   = bool(db[0]["useDefaultApp"]),
                        app_path          = db[0]["appPath"],
                        anime_folder      = db[0]["animeFolder"],
                        first_use         = bool(db[0]["firstUse"]),
                        db_version        = db[0]["dbVersion"])
        return config

    def get_anime_list(self):
        """
        Reads 'anime' table from DB, generates a list with all data.

        :rtype: list[Anime]
        :return: All data from all anime on the DB.
        """
        anime_list = []
        self.number_of_anime_enabled = 0
        db = self.__read_table("anime")
        for result in db:
            anime_list.append(Anime(enabled=             bool(db[result]["enabled"]),
                                    name=                db[result]["name"],
                                    episode=             db[result]["episodeNumber"],
                                    version=             db[result]["versionNumber"],
                                    search_terms=        db[result]["search"],
                                    last_file_downloaded=db[result]["lastFileDownloaded"],
                                    download_folder=     db[result]["downloadFolder"],
                                    check_anime_index=   db[result]["checkAnimeIndex"],
                                    check_anime_tosho=   db[result]["checkAnimeTosho"],
                                    check_anirena=       db[result]["checkAnirena"],
                                    check_nyaa=          db[result]["checkNyaa"],
                                    check_tokyotosho=    db[result]["checkTokyotosho"]))
            if db[result]["enabled"]:
                self.number_of_anime_enabled+=1
        return anime_list

    def insert_anime(self,anime):
        """
        Inserts anime in the DB.

        :type anime: Anime
        :param anime: ...

        :rtype: bool
        :return: If the anime was added successfully to the DB or not.
        """
        success = False
        try:
            __c = self.conn.cursor()
            enabled = int(anime.enabled)
            check_anime_index = int(anime.check_anime_index)
            check_anime_tosho = int(anime.check_anime_tosho)
            check_anirena = int(anime.check_anirena)
            check_nyaa = int(anime.check_nyaa)
            check_tokyotosho = int(anime.check_tokyotosho)
            __c.execute("INSERT INTO anime ({0:s}) VALUES ({1:d}, \"{2:s}\", {3:d}, {4:d}, \"{5:s}\", \"{6:s}\", \"{7:s}\", {8:d}, {9:d}, {10:d}, {11:d}, {12:d})".format(
                        "enabled,name,episodeNumber,versionNumber,search,lastFileDownloaded,downloadFolder,checkAnimeIndex,checkAnimeTosho,checkAnirena,checkNyaa,checkTokyotosho",
                        enabled,
                        anime.name,
                        anime.episode,
                        anime.version,
                        anime.search_terms,
                        anime.last_file_downloaded,
                        anime.download_folder,
                        check_anime_index,
                        check_anime_tosho,
                        check_anirena,
                        check_nyaa,
                        check_tokyotosho))
            self.conn.commit()
            success = True
        except Exception as error:
            self.log.error("ERROR while inserting [%s] into table 'anime'" % escape_unicode(anime.name))
            self.log.print_traceback(error,self.log.error)
        return success

    def remove_anime(self,anime_name):
        """
        Removes anime from the DB.

        :type anime_name: str or unicode
        :param anime_name: ...

        :rtype: bool
        :return: If the anime was successfully removed or not.
        """
        success = False
        try:
            __c = self.conn.cursor()
            __c.execute("DELETE FROM anime WHERE name='%s'" % anime_name)
            self.conn.commit()
            success = True
        except Exception as error:
            self.log.error("ERROR while removing [%s] into table 'anime'" % escape_unicode(anime_name))
            self.log.print_traceback(error,self.log.error)
        return success


class Anime():
    """
    Anime class.
    """

    def __init__(self,enabled=False,name="",episode=0,version=0,search_terms="",last_file_downloaded="",download_folder="",
                 check_anime_index=True,check_anime_tosho=True,check_anirena=True,check_nyaa=True,check_tokyotosho=True):
        """
        :type enabled: bool
        :param enabled: search for new episodes or not

        :type name: str or unicode
        :param name: ...

        :type episode: int
        :param episode: ...

        :type version: int
        :param version: v0,v1,v2,....

        :type search_terms: str or unicode
        :param search_terms: ...

        :type last_file_downloaded: str or unicode
        :param last_file_downloaded: used to search for v2,v3,etc.

        :type download_folder: str or unicode
        :param download_folder: where the torrent application should save the episode

        :type check_anime_index: bool
        :param check_anime_index: ...

        :type check_anime_tosho: bool
        :param check_anime_tosho: ...

        :type check_anirena: bool
        :param check_anirena: ...

        :type check_nyaa: bool
        :param check_nyaa: ...

        :type check_tokyotosho: bool
        :param check_tokyotosho: ...
        """
        self.enabled = enabled
        self.name = name
        self.episode = episode
        self.version = version
        self.search_terms = search_terms
        self.last_file_downloaded = last_file_downloaded
        self.download_folder = download_folder
        self.check_anime_index = check_anime_index
        self.check_anime_tosho = check_anime_tosho
        self.check_anirena = check_anirena
        self.check_nyaa = check_nyaa
        self.check_tokyotosho = check_tokyotosho

    def update_enabled(self,new_enabled):
        """
        Updates "enabled" status.

        :type new_enabled: bool
        :param new_enabled: ...
        """
        DBManager().update_registry("anime","enabled",new_enabled,"name",self.name)
        self.enabled = new_enabled

    def update_name(self,new_name):
        """
        Changes anime name.

        :type new_name: str or unicode
        :param new_name: ...
        """
        DBManager().update_registry("anime","name",new_name,"name",self.name)
        self.name = new_name

    def update_episode(self,new_episode):
        """
        Updates episode number.

        :type new_episode: int
        :param new_episode: ...
        """
        DBManager().update_registry("anime","episodeNumber",new_episode,"name",self.name)
        self.episode = new_episode

    def update_version(self,new_version):
        """
        Updates version number.

        :type new_version: int
        :param new_version: ...
        """
        DBManager().update_registry("anime","versionNumber",new_version,"name",self.name)
        self.version = new_version

    def update_search_terms(self,new_search_terms):
        """
        Updates search terms.

        :type new_search_terms: str or unicode
        :param new_search_terms: ...
        """
        DBManager().update_registry("anime","search",new_search_terms,"name",self.name)
        self.search_terms = new_search_terms

    def update_last_file_downloaded(self,new_last_file_downloaded):
        """
        Updates last file downloaded.

        :type new_last_file_downloaded: str or unicode
        :param new_last_file_downloaded: ...
        """
        DBManager().update_registry("anime","lastFileDownloaded",new_last_file_downloaded,"name",self.name)
        self.last_file_downloaded = new_last_file_downloaded

    def update_download_folder(self,new_download_folder):
        """
        Updates download folder.

        :type new_download_folder: str or unicode
        :param new_download_folder: ...
        """
        DBManager().update_registry("anime","downloadFolder",new_download_folder,"name",self.name)
        self.download_folder = new_download_folder

    def update_check_anime_index(self,new_check_anime_index):
        """
        Updates "check_anime_index" status.

        :type new_check_anime_index: bool
        :param new_check_anime_index: ...
        """
        DBManager().update_registry("anime","checkAnimeIndex",new_check_anime_index,"name",self.name)
        self.check_anime_index = new_check_anime_index

    def update_check_anime_tosho(self,new_check_anime_tosho):
        """
        Updates "check_anime_tosho" status.

        :type new_check_anime_tosho: bool
        :param new_check_anime_tosho: ...
        """
        DBManager().update_registry("anime","checkAnimeTosho",new_check_anime_tosho,"name",self.name)
        self.check_anime_tosho = new_check_anime_tosho

    def update_check_anirena(self,new_check_anirena):
        """
        Updates "check_anirena" status.

        :type new_check_anirena: bool
        :param new_check_anirena: ...
        """
        DBManager().update_registry("anime","checkAnirena",new_check_anirena,"name",self.name)
        self.check_anirena = new_check_anirena

    def update_check_nyaa(self,new_check_nyaa):
        """
        Updates "check_nyaa" status.

        :type new_check_nyaa: bool
        :param new_check_nyaa: ...
        """
        DBManager().update_registry("anime","checkNyaa",new_check_nyaa,"name",self.name)
        self.check_nyaa = new_check_nyaa

    def update_check_tokyotosho(self,new_check_tokyotosho):
        """
        Updates "check_tokyotosho" status.

        :type new_check_tokyotosho: bool
        :param new_check_tokyotosho: ...
        """
        DBManager().update_registry("anime","checkTokyotosho",new_check_tokyotosho,"name",self.name)
        self.check_tokyotosho = new_check_tokyotosho


class Config():
    """
    Config class.
    """

    def __init__(self,show_notification=True,sleep_time=3600,prefer_rss=True,use_default_app=True,app_path="",
                 anime_folder="",first_use=True,db_version=5):
        """
        :type show_notification: bool
        :param show_notification: Notify when a new torrent is downloaded or not.

        :type sleep_time: int
        :param sleep_time: How long to wait before searching for new episodes again.

        :type prefer_rss: bool
        :param prefer_rss: Search using RSS instead of HTML (Nyaa only)

        :type use_default_app: bool
        :param use_default_app: Use default torrent application or not.

        :type app_path: str or unicode
        :param app_path: Path to custom torrent application.

        :type anime_folder: str or unicode
        :param anime_folder: uTorrent only - Default folder where the torrent application should save episodes.

        :type first_use: bool
        :param first_use: First time using the app or not.

        :type db_version: int
        :param db_version: ...
        """
        self.show_notification = show_notification
        self.sleep_time = sleep_time
        self.prefer_rss = prefer_rss
        self.use_default_app = use_default_app
        self.app_path = app_path
        self.anime_folder = anime_folder
        self.first_use = first_use
        self.db_version = db_version

    def update_show_notification(self,new_show_notification):
        """
        Updates "show_notification" status.

        :type new_show_notification: bool
        :param new_show_notification: ...
        """
        DBManager().update_registry("config","showNotification",new_show_notification)
        self.show_notification = new_show_notification

    def update_sleep_time(self,new_sleep_time):
        """
        Updates "sleep_time" value.

        :type new_sleep_time: int
        :param new_sleep_time: ...
        """
        DBManager().update_registry("config","sleepTime",new_sleep_time)
        self.sleep_time = new_sleep_time

    def update_prefer_rss(self,new_prefer_rss):
        """
        Updates "prefer_rss" status.

        :type new_prefer_rss: bool
        :param new_prefer_rss: ...
        """
        DBManager().update_registry("config","preferRss",new_prefer_rss)
        self.prefer_rss = new_prefer_rss

    def update_use_default_app(self,new_use_default_app):
        """
        Updates "use_default_app" status.

        :type new_use_default_app: bool
        :param new_use_default_app: ...
        """
        DBManager().update_registry("config","useDefaultApp",new_use_default_app)
        self.use_default_app = new_use_default_app

    def update_app_path(self,new_app_path):
        """
        Updates torrent application path.

        :type new_app_path: str or unicode
        :param new_app_path: ...
        """
        DBManager().update_registry("config","appPath",new_app_path)
        self.app_path = new_app_path

    def update_anime_folder(self,new_anime_folder):
        """
        Updates anime folder.

        :type new_anime_folder: str or unicode
        :param new_anime_folder: ...
        """
        DBManager().update_registry("config","animeFolder",new_anime_folder)
        self.anime_folder = new_anime_folder

    def update_first_use(self,new_first_use):
        """
        Updates "first_use" status.

        :type new_first_use: bool
        :param new_first_use: ...
        """
        DBManager().update_registry("config","firstUse",new_first_use)
        self.first_use = new_first_use