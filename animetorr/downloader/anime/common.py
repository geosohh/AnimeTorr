# -*- coding: utf-8 -*-
"""
Functions common to more than one site.
"""
__author__ = 'Sohhla'


def terms_match(title,terms):
    """
    Check if all terms are present (or not, in case of '-term') in the search result.

    :type title: str or unicode
    :param title: Search result.

    :type terms: list[str or unicode]
    :param terms: List of search terms

    :rtype: bool
    :return: If the title matches the search terms or not.
    """
    success = True
    title = title.lower()
    for term in terms:
        term = term.strip().lower()
        if term.startswith('-'):
            if term[1:] in title:
                success = False
                break
        else:
            if term not in title:
                success = False
                break
    return success