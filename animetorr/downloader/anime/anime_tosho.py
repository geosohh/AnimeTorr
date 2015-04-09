# -*- coding: utf-8 -*-
"""
Search on Anime Tosho using HTML.
"""
__author__ = 'Sohhla'


import sgmllib
from shared.log import LoggerManager


class AnimeTosho():
    """
    Search on Anime Tosho using HTML.
    """
    def __init__(self,network):
        self.log = LoggerManager().get_logger("AnimeTosho")
        self.network = network

    def search(self,text="",dic=None):
        """
        Returned dictionary struct:
        dict[RESULT_NUMBER]["title"] = str
        dict[RESULT_NUMBER]["link"] = str
        dict[RESULT_NUMBER]["date"] = datetime

        :type text: str
        :param text: search_terms

        :type dic: dict
        :param dic: where the data will be stored. If None, a new dict is created.
        """
        if dic is None:
            dic = {}
        url = self.__get_url(text)
        html = self.network.get_data(url)
        return self.__parse_html(html, dic, text)

    @staticmethod
    def __get_url(text):
        url = ""
        if text!="":
            positive_words = [word for word in text.split(" ") if not word.startswith("-")]
            positive_text = "+".join(positive_words)
            url = "https://animetosho.org/search?q=%s" % positive_text
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
        self.cont = 0
        self.dict = {}
        self.searching_div_title = True
        self.search_a_title = False
        self.get_title = False
        self.searching_link = False
        self.confirmTorrent = False

    def start_div(self, data):
        if self.searching_div_title:
            for atrib,value in data:
                if atrib=="class" and value=="link":
                    self.searching_div_title = False
                    self.search_a_title = True
                elif atrib=="id" and value=="topbar_c":
                    raise CleanExit

    def start_a(self, data):
        if self.search_a_title:
            self.search_a_title = False
            self.get_title = True
        elif self.searching_link:
            for atrib,value in data:
                if atrib=="class" and value=="dllink":
                    for atrib2,value2 in data:
                        if atrib2=="href":
                            self.link = value2
                            self.confirmTorrent = True
                            break
                    break

    def handle_data(self, data):
        if self.get_title:
            self.title = data
            self.get_title = False
            self.searching_link = True
        elif self.confirmTorrent:
            temp = data
            if temp=="Torrent":
                self.searching_link = False
                self.confirmTorrent = False

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
                    self.dict["at"+str(self.cont)] = {}
                    self.dict["at"+str(self.cont)]["title"] = self.title
                    self.dict["at"+str(self.cont)]["link"] = self.link
                    self.dict["at"+str(self.cont)]["date"] = None
                    self.cont+=1
                self.title = ""
                self.link = ""
                self.searching_div_title = True


class CleanExit(Exception):
    """
    Used to gracefully finish the parsing.
    """
    pass
