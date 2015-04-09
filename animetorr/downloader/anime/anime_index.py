# -*- coding: utf-8 -*-
"""
Search on Anime Index using HTML.
"""
__author__ = 'Sohhla'


import sgmllib
import datetime
from shared.log import LoggerManager


class AnimeIndex():
    """
    Search on Anime Index using HTML.
    """
    def __init__(self,network):
        self.log = LoggerManager().get_logger("AnimeIndex")
        self.network = network

    def search(self,text="",dic=None,category=5,active=1):
        """
        Returned dictionary struct:
        dict[RESULT_NUMBER]["title"] = str
        dict[RESULT_NUMBER]["link"] = str
        dict[RESULT_NUMBER]["date"] = datetime
        dict[RESULT_NUMBER]["downloads"] = int

        :type text: str
        :param text: search_terms

        :type dic: dict
        :param dic: where the data will be stored. If None, a new dict is created.

        :type category: int
        :param category: site specific filter to search only for anime.

        :type active: int
        :param active: site specific filter to search only for active downloads.
        """
        if dic is None:
            dic = {}
        url = self.__get_url(text,category,active)
        html = self.network.get_data(url)
        return self.__parse_html(html, dic, text)

    @staticmethod
    def __get_url(text,category,active):
        url = ""
        if text!="":
            positive_words = [word for word in text.split(" ") if not word.startswith("-")]
            positive_text = "+".join(positive_words)
            url = "tracker.anime-index.org/index.php?page=torrents&search=%s&category=%s&active=%s" % (positive_text,str(category),str(active))
        return url

    def __parse_html(self,html, dic, text):
        parser = HTMLparser()
        parser.dict = dic
        parser.cont = len(dic)
        parser.search_terms = text.strip().split(" ")
        try:
            parser.feed(html)
            parser.close()
        except CleanExit:
            self.log.info("HTML successfully parsed (%i results)" % (len(parser.dict)))
            return parser.dict
        except Exception as error:
            self.log.print_traceback(error,self.log.error)
        else:
            self.log.info("HTML successfully parsed (%i results)" % (len(parser.dict)))
        #return dic
        return parser.dict


# noinspection PyDocstring
# ^ No need for these methods
class HTMLparser(sgmllib.SGMLParser):
    """
    Receives HTML code, parses it.
    """
    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.search_terms = []
        self.title = ""
        self.link = ""
        self.date_year = 0
        self.date_month = 0
        self.date_day = 0
        self.date_hour = 0
        self.date_minute = 0
        self.downloads = 0
        self.cont = 0
        self.dict = {}
        self.cleanExit_ok = False
        self.searching_tr = False
        self.searching_td_image = False
        self.searching_td_title = False
        self.get_title = False
        self.searching_td_link = False
        self.get_link = False
        self.searching_td_date = False
        self.get_date = False
        self.searching_td_seeds = False
        self.searching_td_leechs = False
        self.searching_td_downloads = False
        self.search_downloads = False
        self.get_downloads = False

        self.searching_title = False
        self.searching_descbot = False
        self.searching_size_date = False

    def start_td(self, data):
        if not self.cleanExit_ok:
            for atrib,value in data:
                if atrib=="class" and value=="header":
                    self.cleanExit_ok = True
                    self.searching_tr = True
        elif self.searching_td_image:
            self.searching_td_image = False
            self.searching_td_title = True
        elif self.searching_td_title:
            self.searching_td_title = False
            self.get_title = True
        elif self.searching_td_link:
            self.searching_td_link = False
            self.get_link = True
        elif self.searching_td_date:
            self.searching_td_date = False
            self.get_date = True
        elif self.searching_td_seeds:
            self.searching_td_seeds = False
            #not needed, might change in a future version
            self.searching_td_leechs = True
        elif self.searching_td_leechs:
            self.searching_td_leechs = False
            #not needed, might change in a future version
            self.searching_td_downloads = True
        elif self.searching_td_downloads:
            self.searching_td_downloads = False
            self.search_downloads = True

    def start_tr(self,_):
        if self.searching_tr:
            self.searching_td_image = True
            self.searching_tr = False

    def start_a(self, data):
        if self.get_title:
            for atrib,value in data:
                if atrib=="title":
                    self.title = value.replace("View details: ","")
                    self.get_title = False
                    self.searching_td_link = True
        elif self.get_link:
            for atrib,value in data:
                if atrib=="href":
                    self.link = value
                    if self.link.startswith("download.php"):
                        self.link = "tracker.anime-index.org/"+self.link
                    self.get_link = False
                    self.searching_td_date = True
        elif self.search_downloads:
            self.search_downloads = False
            self.get_downloads = True

    def handle_data(self, data):
        if self.get_date:
            temp = data
            temp = temp.replace("/"," ")
            temp = temp.replace(":"," ")
            values = temp.split(" ")
            self.date_day = int(values[0])
            self.date_month = int(values[1])
            self.date_year = int(values[2])
            self.date_hour = int(values[3])
            self.date_minute = int(values[4])
            self.get_date = False
            self.searching_td_seeds = True
        elif self.get_downloads or self.search_downloads:
            self.downloads = int(data)
            self.get_downloads = False
            self.search_downloads = False
            self.searching_tr = True

            success = True
            for term in self.search_terms:
                term = term.strip()
                if term[0] is "-":
                    if term[1:].lower() in self.title.lower():
                        success = False
                        break
                else:
                    if term.lower() not in self.title.lower():
                        success = False
                        break
            if success:
                self.dict["ai"+str(self.cont)] = {}
                self.dict["ai"+str(self.cont)]["title"] = self.title
                self.dict["ai"+str(self.cont)]["link"] = self.link
                self.dict["ai"+str(self.cont)]["date"] = datetime.datetime(self.date_year, self.date_month, self.date_day, self.date_hour, self.date_minute)
                self.dict["ai"+str(self.cont)]["downloads"] = self.downloads
                self.cont+=1
            self.title = ""
            self.link = ""
            self.date_year = 0
            self.date_month = 0
            self.date_day = 0
            self.date_hour = 0
            self.date_minute = 0
            self.downloads = 0

    def start_table(self, data):
        pass
    def end_table(self):
        if self.cleanExit_ok:
            raise CleanExit


class CleanExit(Exception):
    """
    Used to gracefully finish the parsing.
    """
    pass
