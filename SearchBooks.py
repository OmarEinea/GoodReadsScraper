#!/usr/bin/env python


# import needed libraries
import mechanize


# A class to Search then Scrape lists and books from GoodReads.com
class SearchBooks:
    def __init__(self, keyword=None):
        self.site_url = "https://www.goodreads.com"
        self.keyword = None
        self.set_keyword(keyword)
        # Instantiate mechanize browser
        self.br = mechanize.Browser()
        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Keyword setter
    def set_keyword(self, keyword):
        self.keyword = str(keyword).replace(' ', '+')
