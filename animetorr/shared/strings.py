# -*- coding: utf-8 -*-
"""
Functions to take care of str/unicode/QString strings.
"""
__author__ = 'Sohhla'


import re
import unicodedata


def read_qt_text(text):
    """
    In Python 2.X, <str> and <unicode> are different classes.
    Besides that, PyQT returns strings using <QString> objects.
    This function converts a <QString> to <unicode>.

    :type text: QtCore.QString
    :param text: text read from a QT widget

    :rtype: unicode
    :return: text converted
    """
    temp_byte_array = text.toUtf8()
    text_read = "".join(temp_byte_array)
    text_read = text_read.decode("utf-8")
    return text_read


def escape_unicode(text):
    """
    Escapes unicodes characters so that the text can be correctly printed.

    :type text: str or unicode
    :param text: ...

    :rtype: str
    :return: Text with unicode characters escaped.
    """
    return text.encode('unicode-escape')


def remove_special_chars(text):
    """
    Removes special characters/letters with diacritical marks.
    I.E. removes any character that is not [a-zA-Z], [0-9] or space.
    Used to generate search terms from the anime's name or the torrent filename.

    :type text: unicode
    :param text: search terms

    :rtype: unicode
    :return: string with characters replaced
    """
    text = re.sub(u'\u014d',"o ",text)   # could be 'o' or 'ou'; the extra space allows results with both writing
    text = re.sub(u'\u00d7'," x ",text)  # × (http://en.wikipedia.org/wiki/List_of_Unicode_characters)
    text = re.sub(u'\u2062'," x ",text)  # × (apparently there's two codes for the same symbol?)
    # Remove accents: http://stackoverflow.com/a/518232
    text = "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub("[^a-zA-Z0-9 \-]+"," ",text)
    text = re.sub("\s{2,}"," ",text)
    return text.strip()