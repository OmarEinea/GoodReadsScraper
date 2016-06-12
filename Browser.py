#!/usr/bin/env python

# import needed libraries
from mechanize import Browser, HTTPRefreshProcessor, LinkNotFoundError


# A GoodReads specific Mechanize browser class
class GoodReadsBrowser(Browser):
    # Store GoodReads.com root url
    site_url = "https://www.goodreads.com"

    def __init__(self):
        # Call super class constructor
        Browser.__init__(self)
        # Browser options
        self.set_handle_equiv(True)
        self.set_handle_robots(False)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_refresh(HTTPRefreshProcessor(), max_time=1)

    # Shortcut to open GoodReads books list
    def open_list(self, list_id):
        self.open(self.site_url + "/list/show/" + list_id)

    # Shortcut to open a GoodReads search page for books lists
    def open_list_search(self, keyword):
        self.open(self.site_url + "/search?search_type=lists&q=" + keyword)

    # Check if there's a next page and open it
    def has_next_page(self, text):
        # Try to enter next page
        try:
            self.follow_link(self.find_link(text_regex=text))
        # Return false if there's no next, otherwise return true
        except LinkNotFoundError:
            return False
        return True
