# -*- coding: utf-8 -*-
"""
Search on Nyaa using HTML.
"""
__author__ = 'Sohhla'

import sgmllib
from shared.log import LoggerManager


class Nyaa():
    """
    Search on Nyaa using HTML.
    """
    def __init__(self, network):
        self.log = LoggerManager().get_logger("Nyaa")
        self.network = network

    def search(self, text="", dic=None, category="1_37"):  #"1_37" = English translated anime
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

        :type category: str
        :param category: site specific filter to search only for anime.
        """
        if dic is None:
            dic = {}
        search_terms = text.strip().split(" ")
        url = self.__get_url(text, category)
        html = self.network.get_data(url)
        if "viewtorrentname" in html:
            return self.__parse_html_1_result(html, dic, search_terms)
        else:
            return self.__parse_html(html, dic, search_terms)

    @staticmethod
    def __get_url(text, category):
        url = ""
        if text!="":
            text = text.strip().replace(" ","+")
            url = "www.nyaa.se/?page=search&term=%s&cats=%s" % (text,category)
        return url

    def __parse_html_1_result(self, html, dic, search_terms):
        parser = HTMLparser1Result()
        parser.dict = dic
        parser.cont = len(dic)
        parser.search_terms = search_terms
        parser.debug = self
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

    def __parse_html(self,html, dic, search_terms):
        parser = HTMLparser()
        parser.dict = dic
        parser.cont = len(dic)
        parser.search_terms = search_terms
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
        self.clean_exit_ok = False
        self.searching_a = False
        self.searching_title = False
        self.searching_link = False
        self.searching_downloads = False
        self.get_downloads = False

    def start_td(self, data):
        for atrib,value in data:
            if atrib=="class" and value=="tlistname":
                self.searching_a = True
                self.clean_exit_ok = True
            elif self.searching_downloads and atrib=="class" and value=="tlistdn":
                self.get_downloads = True

    def start_a(self, data):
        if self.searching_a:
            self.searching_a = False
            self.searching_title = True
            self.title = ""
        if self.searching_link:
            for atrib,value in data:
                if atrib=="href":
                    self.link = value.replace("view","download")
                    self.searching_link = False
                    self.searching_downloads = True

    def end_a(self):
        if self.searching_title:
            self.searching_title = False
            self.searching_link = True

    def handle_data(self, data):
        if self.searching_title:
            self.title = data
        elif self.get_downloads:
            self.downloads = int(data)
            self.get_downloads = False

            success = True
            for term in self.search_terms:
                temp = term.strip().lower()
                term = temp.encode("utf-8","ignore")
                if term[0] is "-":
                    if term[1:] in self.title.lower():
                        success = False
                        break
                else:
                    if term not in self.title.lower():
                        success = False
                        break
            if success:
                self.dict["n"+str(self.cont)] = {}
                self.dict["n"+str(self.cont)]["title"] = self.title
                self.dict["n"+str(self.cont)]["link"] = self.link
                self.dict["n"+str(self.cont)]["date"] = None
                self.dict["n"+str(self.cont)]["downloads"] = self.downloads
                self.cont+=1

                self.title = ""
                self.link = ""
                self.downloads = 0

    def start_table(self, data):
        pass
    def end_table(self):
        if self.clean_exit_ok:
            raise CleanExit


# noinspection PyDocstring
# ^ No need for these methods
class HTMLparser1Result(sgmllib.SGMLParser):
    """
    Receives HTML code, parses it.
    When there's only one result the result is different, so a different parser is necessary.
    """
    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.search_terms = []
        self.title = ""
        self.link = ""
        self.downloads = 0
        self.cont = 0
        self.dict = {}
        self.searching_title = False
        self.searching_link = False
        self.get_link = False
        self.searching_downloads = False
        self.get_downloads = False

        self.debug = None

    def start_td(self, data):
        for atrib,value in data:
            if atrib=="class" and value=="viewtorrentname":
                self.searching_title = True
                self.title = ""
    def end_td(self):
        if self.searching_title:
            self.debug.log.debug("HTMLparser1Result - title={{%s}}" % self.title)
            self.searching_title = False
            self.searching_downloads = True
    def start_span(self,data):
        if self.searching_downloads:
            for atrib,value in data:
                if atrib=="class" and value=="viewdn":
                    self.searching_downloads = False
                    self.get_downloads = True
    def end_span(self):
        if self.get_downloads:
            self.get_downloads = False
            self.searching_link = True
    def handle_data(self, data):
        if self.searching_title:
            self.title = data
        elif self.get_downloads:
            self.downloads = int(data)

    def start_div(self, data):
        for atrib,value in data:
            if self.searching_link and atrib=="class" and value=="viewdownloadbutton":
                self.searching_link = False
                self.get_link = True
    def start_a(self, data):
        if self.get_link:
            for atrib,value in data:
                if atrib=="href":
                    self.link = value
                    self.get_link = False

                    success = True
                    for term in self.search_terms:
                        temp = term.strip().lower()
                        term = temp.encode("utf-8","ignore")
                        self.debug.log.debug("HTMLparser1Result - term={{%s}} | startswith '-': %s" % (term, term.startswith('-')))
                        if term.startswith('-'):
                            if term[1:] in self.title.lower():
                                self.debug.log.debug("HTMLparser1Result - {{-%s}} in {{%s}}" % (term[1:], self.title.lower()))
                                success = False
                                break
                        else:
                            if term not in self.title.lower():
                                self.debug.log.debug("HTMLparser1Result - {{%s}} not in {{%s}}" % (term, self.title.lower()))
                                success = False
                                break
                    if success:
                        self.dict["n"+str(self.cont)] = {}
                        self.dict["n"+str(self.cont)]["title"] = self.title
                        self.dict["n"+str(self.cont)]["link"] = self.link
                        self.dict["n"+str(self.cont)]["date"] = None
                        self.dict["n"+str(self.cont)]["downloads"] = self.downloads
                    raise CleanExit


class CleanExit(Exception):
    """
    Used to gracefully finish the parsing.
    """
    pass
