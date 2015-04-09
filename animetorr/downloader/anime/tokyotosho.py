# -*- coding: utf-8 -*-
"""
Search on Tokyotosho using HTML.
"""
__author__ = 'Sohhla'

import sgmllib
import datetime
from shared.log import LoggerManager


class Tokyotosho():
    """
    Search on Tokyotosho using HTML.
    """
    def __init__(self,network):
        self.log = LoggerManager().get_logger("Tokyotosho")
        self.network = network

    def search(self,text="",dic=None,category=1):
        """
        Returned dictionary struct:
        dict[RESULT_NUMBER]["title"] = str
        dict[RESULT_NUMBER]["link"] = str
        dict[RESULT_NUMBER]["date"] = datetime

        :type text: str
        :param text: search_terms

        :type dic: dict
        :param dic: where the data will be stored. If None, a new dict is created.

        :type category: str
        :param category: site specific filter to search only for anime.
        """
        if dic is None:
            dic = {}
        url = self.__get_url(text,category)
        html = self.network.get_data(url)
        html = html.replace("<span class=\"s\"> </span>","")
        return self.__parse_html(html, dic, text)

    @staticmethod
    def __get_url(text,category):
        url = ""
        if text!="":
            text = text.strip().replace(" ","+")
            url = "www.tokyotosho.info/search.php?terms=%s&type=%s" % (text,str(category))
        return url

    def __parse_html(self,html,dic,text):
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
        self.cont = 0
        self.dict = {}
        self.cleanExit_ok = False
        self.searching_a = False
        self.searching_title = False
        self.searching_descbot = False
        self.searching_size_date = False

    def start_td(self, data):
        for atrib,value in data:
            if atrib=="class" and value=="desc-top":
                self.cleanExit_ok = True
                self.searching_a = True
            elif atrib=="class" and value=="desc-bot" and self.searching_descbot:
                self.searching_descbot = False
                self.searching_size_date = True
    def start_a(self, data):
        for atrib,value in data:
            if self.searching_a and atrib=="type" and value=="application/x-bittorrent":
                for atrib2,value2 in data:
                    if atrib2=="href":
                        self.link = value2
                        if "nyaa.eu" in self.link:
                            self.link = self.link.replace("torrentinfo","download")
                        self.searching_a = False
                        self.searching_title = True
                        self.title = ""
    def end_a(self):
        if self.searching_title:
            self.searching_title = False
            self.searching_descbot = True
    def handle_data(self, data):
        if self.searching_title:
            self.title = data
        elif self.searching_size_date and data.find("Size: ")!=-1:
            temp = data
            date = temp[temp.find("Date: ")+6:]
            date = date[:date.find(" UTC")]
            self.date_year = int(date[:date.find("-")])
            date = date[date.find("-")+1:]
            self.date_month = int(date[:date.find("-")])
            date = date[date.find("-")+1:]
            self.date_day = int(date[:date.find(" ")])
            date = date[date.find(" ")+1:]
            self.date_hour = int(date[:date.find(":")])
            self.date_minute = int(date[date.find(":")+1:])
            self.searching_size_date = False

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
                self.dict["t"+str(self.cont)] = {}
                self.dict["t"+str(self.cont)]["title"] = self.title
                self.dict["t"+str(self.cont)]["link"] = self.link
                self.dict["t"+str(self.cont)]["date"] = datetime.datetime(self.date_year, self.date_month, self.date_day, self.date_hour, self.date_minute)
                self.cont+=1

            self.title = ""
            self.link = ""
            self.date_year = 0
            self.date_month = 0
            self.date_day = 0
            self.date_hour = 0
            self.date_minute = 0
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
