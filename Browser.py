#!/usr/bin/env python

# import needed libraries
from selenium.webdriver import PhantomJS
from selenium.common.exceptions import NoSuchElementException


# A GoodReads specific PhantomJS browser class
class GoodReadsBrowser(PhantomJS):
    # Store GoodReads.com root url
    site_url = "https://www.goodreads.com"

    def __init__(self):
        # Call super class constructor
        PhantomJS.__init__(self, "./phantomjs")
        self.next_page = None

    # Shortcut to open GoodReads books list
    def open_book(self, book_id):
        self.get(self.site_url + "/book/show/" + str(book_id))

    # Shortcut to open GoodReads books list
    def open_list(self, list_id):
        self.get(self.site_url + "/list/show/" + str(list_id))

    # Shortcut to open a GoodReads search page for books lists
    def open_list_search(self, keyword):
        self.get(self.site_url + "/search?search_type=lists&q=" + str(keyword))

    def has_next_page(self):
        try:
            self.next_page = self.find_element_by_class_name("next_page")
        except NoSuchElementException:
            return False
        return self.next_page.tag_name == 'a'

    def goto_next_page(self, repeated=False):
        if not repeated:
            self.next_page.click()
            return True
        return False

    def links(self, title):
        return self.find_elements_by_class_name(title + "Title")
