# -*- coding: utf-8 -*-
"""
Search on Anirena using HTML.
"""
__author__ = 'Sohhla'

import sgmllib
from shared.log import LoggerManager


class Anirena():
    """
    Search on Anirena using HTML.
    """
    def __init__(self,network):
        self.log = LoggerManager().get_logger("Anirena")
        self.network = network

    def search(self,text="",dic=None,category=2):
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
        """
        if dic is None:
            dic = {}
        url = self.__get_url(text,category)
        html = self.network.get_data(url)
        return self.__parse_html(html, dic, text)

    @staticmethod
    def __get_url(text,category):
        url = ""
        if text!="":
            positive_words = [word for word in text.split(" ") if not word.startswith("-")]
            positive_text = "+".join(positive_words)
            url = "www.anirena.com/?s=%s&t=%s" % (positive_text,str(category))
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
        self.downloads = 0
        self.cont = 0
        self.dict = {}
        self.searching_td_title = True
        self.search_a_title = False
        self.ignore_next_a = False
        self.searching_td_link = False
        self.search_a_link = False
        self.searching_td_downloads = False
        self.get_downloads = False

    def start_td(self, data):
        if self.searching_td_title:
            for atrib,value in data:
                if atrib=="class" and value=="torrents_small_info_data1":
                    self.searching_td_title = False
                    self.search_a_title = True
        elif self.searching_td_link:
            for atrib,value in data:
                if atrib=="class" and value=="torrents_small_info_data2":
                    self.searching_td_link = False
                    self.search_a_link = True
        elif self.searching_td_downloads:
            for atrib,value in data:
                if atrib=="class" and value=="torrents_small_downloads_data1":
                    self.searching_td_downloads = False
                    self.get_downloads = True

    def start_b(self,_):
        if self.search_a_title:
            self.ignore_next_a = True
    def end_b(self):
        if self.search_a_title and self.ignore_next_a:
            self.ignore_next_a = False

    def start_a(self, data):
        if self.search_a_title and not self.ignore_next_a:
            for atrib,value in data:
                if atrib=="title":
                    self.title = value
                    self.search_a_title = False
                    self.searching_td_link = True
        elif self.search_a_link:
            for atrib,value in data:
                if atrib=="href":
                    self.link = value
                    if self.link.startswith("./"):
                        self.link = self.link.replace("./","www.anirena.com/")
                    self.search_a_link = False
                    self.searching_td_downloads = True

    def handle_data(self, data):
        if self.get_downloads:
            self.downloads = int(data)
            self.get_downloads = False

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
                self.dict["ar"+str(self.cont)] = {}
                self.dict["ar"+str(self.cont)]["title"] = self.title
                self.dict["ar"+str(self.cont)]["link"] = self.link
                self.dict["ar"+str(self.cont)]["date"] = None
                self.dict["ar"+str(self.cont)]["downloads"] = self.downloads
                self.cont+=1
            self.title = ""
            self.link = ""
            self.downloads = 0
            self.searching_td_title = True

    def start_div(self, data):
        if self.searching_td_title:
            for atrib,value in data:
                if atrib=="class" and value=="footer":
                    raise CleanExit


class CleanExit(Exception):
    """
    Used to gracefully finish the parsing.
    """
    pass
