# -*- coding: utf-8 -*-
"""
Network communication to request data from all sites.
"""
__author__ = 'Sohhla'


import os
import requests
from requests.exceptions import ReadTimeout,ConnectTimeout
from PyQt4 import QtCore
from shared.log import LoggerManager
from shared import strings
from shared import constant
from shared import torrent_application
#from HTMLParser import HTMLParser


class Network():
    """
    Controls data requests.
    """

    def __init__(self):
        self.log = LoggerManager().get_logger("Network")
        self.stopping_thread = False

    def stop_thread(self):
        """
        Data requests can't be stopped immediatelly, so this method warns the Network instance to stop as soon as possible.
        """
        self.stopping_thread = True

    def get_data(self,url,is_binary=False):
        """
        Requests data, be it the html/rss of a site or a torrent file.

        :type url: str
        :param url: Link to the data to be downloaded.

        :type is_binary: bool
        :param is_binary: If the data is binary (torrent files) or not.

        :rtype: str
        :return: the data requested
        """
        if url=="":
            self.log.error("No link has been received (aka empty URL)!")
            return None
        resp = ""
        if url.find("://")==-1:
            url = "http://"+url
        self.log.debug("link: %s" % url)
        timeout = True
        tries = 0
        while timeout and not self.stopping_thread:
            try:
                if url.startswith("https"):
                    response = requests.get(url, timeout=10, verify=constant.CACERT_PATH)
                else:
                    response = requests.get(url, timeout=10)
                timeout=False
                if is_binary:
                    resp = response.content
                else:
                    resp = response.text
                    #resp = HTMLParser().unescape(response.text)
            except (ReadTimeout,ConnectTimeout):
                tries+=1
                if tries==3:
                    self.log.warning("Retried 3 times... Will try again later.")
                    return ""
                self.log.debug("Retrying (%i)" % tries)
            except Exception as error:
                self.log.print_traceback(error,self.log.error)
        return resp

    def download_torrent(self,url,file_name,torrent_path,anime_folder):
        """
        Requests download of the torrent file, saves it, and opens it with torrent application.

        :type url: str
        :param url: Link to the torrent file.

        :type file_name: str
        :param file_name: The name with which the torrent file will be saved.

        :type torrent_path: str
        :param torrent_path: The folder where the torrent file will be saved.

        :type anime_folder: str
        :param anime_folder: The folder where the torrent application should save the episode (uTorrent only).

        :rtype: bool
        :return: if the torrent was sent to the torrent application or not.
        """
        if os.path.isdir(torrent_path):
            try:
                data = self.get_data(url, is_binary=True)
                if self.__is_torrent(data):
                    self.__save_torrent(data,file_name,torrent_path,anime_folder)
                    return True
                return False
            except Exception as error:
                raise error
        else:
            self.log.error("The .torrent was NOT downloaded (does the specified folder (%s) exists?)" % torrent_path)
            return False

    @staticmethod
    def __is_torrent(file_data):
        """
        Makes sure the file downloaded is indeed a ".torrent".

        :param file_data: The file.

        :rtype: bool
        :return: If it's a torrent file or not.
        """
        # seems like torrent files start with this. So yeah, it's POG, but for now it's working ^^
        return str(file_data).find("d8:announce")==0

    def __save_torrent(self,data,file_name,torrent_path,anime_folder=""):
        """
        Saves the torrent file and opens it with the torrent application selected.

        :param data: The file data.

        :type file_name: str or unicode
        :param file_name: The name with which the torrent file will be saved.

        :type torrent_path: str
        :param torrent_path: The folder where the torrent file will be saved.

        :type anime_folder: str
        :param anime_folder: The folder where the torrent application should save the episode (uTorrent only).
        """
        if os.path.isdir(torrent_path):
            title = strings.remove_special_chars(file_name)
            torrent_file_path = "%s\\%s.torrent" % (torrent_path,title)
            with open(torrent_file_path,"wb") as torrent:
                torrent.write(data)
            self.log.info(".torrent saved")
            try:
                application_fullpath = torrent_application.fullpath()
                self.log.debug("Opening '%s' with '%s'" % (torrent_file_path,application_fullpath))
                if torrent_application.is_utorrent() and os.path.isdir(anime_folder):
                    self.log.debug("Using uTorrent, save in folder '%s'" % strings.escape_unicode(anime_folder))
                    params = ['/DIRECTORY',anime_folder,torrent_file_path]
                else:
                    params = [torrent_file_path]
                # http://stackoverflow.com/questions/1910275/unicode-filenames-on-windows-with-python-subprocess-popen
                # TLDR: Python 2.X's subprocess.Popen doesn't work well with unicode
                QtCore.QProcess().startDetached(application_fullpath,params)
                self.log.info(".torrent opened")
            except Exception as error:
                self.log.error("Error opening torrent application")
                self.log.print_traceback(error,self.log.error)
                raise error
        else:
            self.log.error("The .torrent was NOT saved. Apparently the specified folder (%s) does NOT exist." % torrent_path)