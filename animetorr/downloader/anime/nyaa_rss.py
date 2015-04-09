# -*- coding: utf-8 -*-
"""
Search on Nyaa using RSS.
"""
__author__ = 'Sohhla'


from shared.log import LoggerManager
import xml.etree.ElementTree as XMLParser
from datetime import datetime


class NyaaRSS():
    """
    Search on Nyaa using RSS.
    """
    def __init__(self, network):
        self.log = LoggerManager().get_logger("NyaaRSS")
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
        xml = self.network.get_data(url)
        return self.__parse_rss(xml, dic, search_terms)

    @staticmethod
    def __get_url(text, category):
        url = ""
        if text!="":
            text = text.strip().replace(" ","+")
            url = "www.nyaa.se/?page=rss&term=%s&cats=%s" % (text,category)
        return url

    @staticmethod
    def __parse_rss(xml, dic, search_terms):
        if xml is not "":
            try:
                cont = 0
                xml = xml.encode("utf8","ignore")
                rss = XMLParser.fromstring(xml)
                channel = rss[0]
                for item in channel.findall('item'):
                    title = item.find('title').text
                    link = item.find('link').text
                    date = item.find('pubDate').text
                    date_parsed = datetime.strptime(date,"%a, %d %b %Y %H:%M:%S +0000")
                    description = item.find('description').text
                    values = [int(s) for s in description.split() if s.isdigit()]
                    # TODO: use seeders/leechers
                    seeders = values[0]  # not yet used...
                    leechers= values[1]  # not yet used...
                    downloads=values[2]

                    success = True
                    for term in search_terms:
                        temp = term.strip().lower()
                        term = temp.encode("utf-8","ignore")
                        if term[0] is "-":
                            if term[1:] in title.lower():
                                success = False
                                break
                        else:
                            if term not in title.lower():
                                success = False
                                break
                    if success:
                        dic["n"+str(cont)] = {}
                        dic["n"+str(cont)]["title"] = title
                        dic["n"+str(cont)]["link"] = link
                        dic["n"+str(cont)]["date"] = date_parsed
                        dic["n"+str(cont)]["downloads"] = downloads
                        cont+=1
            # TODO: check all exceptions possible instead of just "Exception"
            except:
                pass
        return dic