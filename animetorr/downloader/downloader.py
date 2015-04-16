# -*- coding: utf-8 -*-
"""
Main script of the downloader.
"""
__author__ = 'Sohhla'


import re
from PyQt4 import QtCore
from data.network import Network
from anime.anime_index import AnimeIndex
from anime.anime_tosho import AnimeTosho
from anime.anirena import Anirena
from anime.nyaa import Nyaa
from anime.nyaa_rss import NyaaRSS
from anime.tokyotosho import Tokyotosho
from shared.db import DBManager
from shared.log import LoggerManager
from shared import constant
from shared.strings import escape_unicode


class Downloader(QtCore.QObject):
    """
    Processes the search requests from the [Add anime window].
    Also responsible for actually searching for new episodes automatically according to the frequency chosen by the user.
    """

    running = QtCore.pyqtSignal()
    finish = QtCore.pyqtSignal()
    restart = QtCore.pyqtSignal()
    showMessage = QtCore.pyqtSignal(str)
    update_ui = QtCore.pyqtSignal(str)

    runningSearch = QtCore.pyqtSignal()
    searchResult = QtCore.pyqtSignal(object)  #Might be dict or None

    def __init__(self, parent=None):
        super(Downloader, self).__init__(parent)
        self.log = None
        self.dbManager = None
        self.animeList = None
        self.config = None
        self.network = None
        self.anime_index = None
        self.anime_tosho = None
        self.anirena = None
        self.nyaa = None
        self.tokyotosho = None
        self.stopping_thread = None
        self.timer = None

    @QtCore.pyqtSlot()
    def execute_once(self):
        """
        Initializes variables necessary to search for new episodes.
        """
        self.log = LoggerManager().get_logger("Downloader")
        self.log.debug("#####################")

        self.dbManager = DBManager()
        self.animeList = self.dbManager.get_anime_list()
        self.config = self.dbManager.get_config()

        self.network = Network()
        self.anime_index = AnimeIndex(self.network)
        self.anime_tosho = AnimeTosho(self.network)
        self.anirena = Anirena(self.network)
        if self.config.prefer_rss:
            self.nyaa = NyaaRSS(self.network)
        else:
            self.nyaa = Nyaa(self.network)
        self.tokyotosho = Tokyotosho(self.network)

        self.stopping_thread = False

        self.timer = QtCore.QTimer()

        self.running.emit()

        self.log.debug("****************************")
        number_of_downloaded_episodes = self.__search_new_episodes()
        msg = "No" if number_of_downloaded_episodes==0 else str(number_of_downloaded_episodes)
        if not self.stopping_thread:
            self.log.info("%s episodes downloaded, sleeping for %s seconds" % (msg, self.config.sleep_time))
            self.restart.emit()
        else:
            self.log.info("%s episodes downloaded, stopping downloader" % msg)
            self.finish.emit()

    def __search_new_episodes(self):
        """
        Searches for new episodes for all enabled anime.
        """
        downloaded_episodes = 0
        current_anime = 0
        for anime in self.animeList:
            if anime.enabled and not self.stopping_thread:
                current_anime += 1
                self.log.info("(%d/%d) searching for episode %s of '%s'" %
                              (current_anime, self.dbManager.number_of_anime_enabled, anime.episode, escape_unicode(anime.name)))
                dict_anime_index,dict_anime_tosho,dict_anirena,dict_nyaa,dict_tokyotosho = self.search(anime)
                anime_dictionary = {}
                if dict_anime_index is not None:
                    anime_dictionary = dict(anime_dictionary.items()+dict_anime_index.items())
                if dict_anime_tosho is not None:
                    anime_dictionary = dict(anime_dictionary.items()+dict_anime_tosho.items())
                if dict_anirena is not None:
                    anime_dictionary = dict(anime_dictionary.items()+dict_anirena.items())
                if dict_nyaa is not None:
                    anime_dictionary = dict(anime_dictionary.items()+dict_nyaa.items())
                if dict_tokyotosho is not None:
                    anime_dictionary = dict(anime_dictionary.items()+dict_tokyotosho.items())
                title = "ERROR(No value)"
                if not self.stopping_thread:
                    try:
                        for key in anime_dictionary.keys():
                            self.log.debug("'%s' is a match, checking episode number" % (escape_unicode(anime_dictionary[key]["title"])))
                            title = anime_dictionary[key]["title"]
                            if (".mkv" or ".mp4") in title:
                                regex_episode_and_version_number = re.compile("[\s|_]*(%02d)[\s|_|~|\-]*(\d*)[\s|_]*v?(\d)?[\s|\w]*[\[|\(]" % anime.episode)
                            else:
                                regex_episode_and_version_number = re.compile("[\s|_]*(%02d)[\s|_|~|\-]*(\d*)[\s|_]*v?(\d)?" % anime.episode)
                            result = regex_episode_and_version_number.findall(title)
                            #self.log.debug("REGEX result = '%s' (len(result)>0: %s)" % (result, len(result)>0))
                            if len(result)>0:
                                self.log.info("A torrent has been found")
                                try:
                                    last_episode_number = int(result[0][1])
                                    self.log.info("It's a double episode! The last episode was number %d" % last_episode_number)
                                except (TypeError,IndexError,ValueError):
                                    last_episode_number = int(result[0][0])
                                    self.log.info("It's a normal episode")
                                try:
                                    last_version_number = int(result[0][2])
                                    self.log.info("It's version %d" % last_version_number)
                                except (TypeError,IndexError,ValueError):
                                    last_version_number = 1
                                if not self.stopping_thread:
                                    result = False
                                    try:
                                        result = self.network.download_torrent(anime_dictionary[key]["link"],
                                                                              "%s %d" % (anime.name,anime.episode),
                                                                              constant.DEFAULT_TORRENTS_PATH,
                                                                              anime.download_folder)
                                    except Exception as error:
                                        self.showMessage.emit("Error: %s (%s - %s)" % (type(error).__name__,anime.name,anime.episode))
                                    if result:
                                        downloaded_episodes+=1
                                        #self.log.debug("Updating EpisodeNumber")
                                        anime.update_episode(last_episode_number+1)
                                        #self.log.debug("Updating LastVersionNumber")
                                        anime.update_version(last_version_number)
                                        #self.log.debug("Updating LastFileDownloaded")
                                        anime.update_last_file_downloaded(anime_dictionary[key]["title"])
                                        self.log.debug("Notifying user")
                                        self.update_ui.emit("Found: %s - %s" % (anime.name, anime.episode-1))
                                        break
                    except Exception as error:
                        self.log.error("ERROR while analysing '%s'" % escape_unicode(title))
                        self.log.print_traceback(error,self.log.error)
            if self.stopping_thread:
                break
        return downloaded_episodes

    def search(self,anime):
        """
        Searches for new episodes of a given anime.

        :type anime: db.Anime
        :param anime: Anime to search for new episode.

        :rtype: dict or None,dict or None,dict or None,dict or None,dict or None
        :return: results for each site: Anime Index, Anime Tosho, Anirena, Nyaa and Tokyotosho
        """
        text = "%s %02d" % (anime.search_terms,anime.episode)
        dict_anime_index = None
        dict_anime_tosho = None
        dict_anirena = None
        dict_nyaa = None
        dict_tokyotosho = None
        if anime.check_anime_index and not self.stopping_thread:
            dict_anime_index = self.anime_index.search(text)
        if anime.check_anime_tosho and not self.stopping_thread:
            dict_anime_tosho = self.anime_tosho.search(text)
        if anime.check_anirena and not self.stopping_thread:
            dict_anirena = self.anirena.search(text)
        if anime.check_nyaa and not self.stopping_thread:
            dict_nyaa = self.nyaa.search(text)
        if anime.check_tokyotosho and not self.stopping_thread:
            dict_tokyotosho = self.tokyotosho.search(text)
        return dict_anime_index,dict_anime_tosho,dict_anirena,dict_nyaa,dict_tokyotosho

    def execute_once_search_anime_index(self,anime):
        """
        Executes search on this site.

        :type anime: db.Anime
        :param anime: Contains search terms.
        """
        self.log = LoggerManager().get_logger("Downloader-Once-AI")
        self.network = Network()
        anime_index = AnimeIndex(self.network)
        self.stopping_thread = False
        self.runningSearch.emit()

        dict_anime_index = None
        if anime.check_anime_index and not self.stopping_thread:
            dict_anime_index = anime_index.search(anime.search_terms)
        self.searchResult.emit(dict_anime_index)
        self.finish.emit()

    def execute_once_search_anime_tosho(self,anime):
        """
        Executes search on this site.

        :type anime: db.Anime
        :param anime: Contains search terms.
        """
        self.log = LoggerManager().get_logger("Downloader-Once-AT")
        self.network = Network()
        anime_tosho = AnimeTosho(self.network)
        self.stopping_thread = False
        self.runningSearch.emit()

        dict_anime_tosho = None
        if anime.check_anime_tosho and not self.stopping_thread:
            dict_anime_tosho = anime_tosho.search(anime.search_terms)
        self.searchResult.emit(dict_anime_tosho)
        self.finish.emit()

    def execute_once_search_anirena(self,anime):
        """
        Executes search on this site.

        :type anime: db.Anime
        :param anime: Contains search terms.
        """
        self.log = LoggerManager().get_logger("Downloader-Once-AR")
        self.network = Network()
        anirena = Anirena(self.network)
        self.stopping_thread = False
        self.runningSearch.emit()

        dict_anirena = None
        if anime.check_anirena and not self.stopping_thread:
            dict_anirena = anirena.search(anime.search_terms)
        self.searchResult.emit(dict_anirena)
        self.finish.emit()

    def execute_once_search_nyaa(self,anime):
        """
        Executes search on this site.

        :type anime: db.Anime
        :param anime: Contains search terms.
        """
        self.log = LoggerManager().get_logger("Downloader-Once-NY")
        self.network = Network()
        if DBManager().get_config().prefer_rss:
            nyaa = NyaaRSS(self.network)
        else:
            nyaa = Nyaa(self.network)
        self.stopping_thread = False
        self.runningSearch.emit()

        dict_nyaa = None
        if anime.check_nyaa and not self.stopping_thread:
            dict_nyaa = nyaa.search(anime.search_terms)
        self.searchResult.emit(dict_nyaa)
        self.finish.emit()

    def execute_once_search_tokyotosho(self,anime):
        """
        Executes search on this site.

        :type anime: db.Anime
        :param anime: Contains search terms.
        """
        self.log = LoggerManager().get_logger("Downloader-Once-TT")
        self.network = Network()
        tokyotosho = Tokyotosho(self.network)
        self.stopping_thread = False
        self.runningSearch.emit()

        dict_tokyotosho = None
        if anime.check_tokyotosho and not self.stopping_thread:
            dict_tokyotosho = tokyotosho.search(anime.search_terms)
        self.searchResult.emit(dict_tokyotosho)
        self.finish.emit()

    def stop_thread(self):
        """
        Stops requests being executed to allow thread to finish gracefully.
        """
        self.log.info("STOPPING DOWNLOADER THREAD")
        self.stopping_thread = True
        self.network.stop_thread()