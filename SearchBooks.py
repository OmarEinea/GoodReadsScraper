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
        # An array for scrapped lists
        self.lists = set()

    # Main function to scrape lists ids
    def get_lists(self):
        # Return lists array if it's not empty
        if self.lists != set():
            return self.lists
        # Open GoodReads' lists search url
        self.br.open(self.site_url + "/search?search_type=lists&q=" + self.keyword)
        # Scrape all result pages
        while True:
            self.__scrape_list("^/list/", self.lists)
            if not self.__has_next_page("next"):
                break
        return self.lists

    # Keyword setter
    def set_keyword(self, keyword):
        self.keyword = str(keyword).replace(' ', '+')

    # Check if there's a next page and enter it
    def __has_next_page(self, text):
        # Try to enter next page
        try:
            self.br.follow_link(self.br.find_link(text_regex=text))
        # Return false if there's no next, otherwise return true
        except mechanize._mechanize.LinkNotFoundError:
            return False
        return True

    # Scrape a single search results page
    def __scrape_list(self, sub_url, array):
        # Loop through all link that start with sub_url
        for link in self.br.links(url_regex=sub_url):
            # Extract and store unique id from link
            array.add(link.url[11:].split('.')[0].split('-')[0])