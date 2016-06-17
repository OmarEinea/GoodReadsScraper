#!/usr/bin/env python

# import needed libraries
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# A GoodReads specific PhantomJS browser class
class Browser(PhantomJS):
    def __init__(self):
        # Call super class constructor
        PhantomJS.__init__(self, "./phantomjs")
        self.set_page_load_timeout(15)
        self.next_page = None

    # General shortcut to open a GoodReads page
    def open(self, sub_url, keyword, options=''):
        while True:
            try:
                self.get("https://www.goodreads.com" + sub_url + str(keyword) + options)
            except TimeoutException:
                print("Reloading page")
                continue
            break

    # Shortcut to open GoodReads book page
    def open_book_page(self, book_id, sort="newest"):
        self.open("/book/show/", book_id, "?text_only=true&sort=" + sort)

    # Shortcut to open GoodReads books list
    def open_list_page(self, list_id):
        self.open("/list/show/", list_id)

    # Shortcut to open a GoodReads search page for books lists
    def open_list_search(self, keyword):
        self.open("/search?q=", keyword, "&search_type=lists")

    # Check if there's a next page
    def has_next_page(self):
        # Try to find the next button
        try:
            self.next_page = self.find_element_by_class_name("next_page")
        # Return false if there isn't one
        except NoSuchElementException:
            return False
        # Check if button is click-able (i.e. it's anchor tag)
        return self.next_page.tag_name == 'a'

    # Click the next button to go to next page
    def goto_next_page(self):
        # If there's a next button
        if self.next_page:
            self.next_page.click()

    def is_page_loaded(self, page):
        try:
            WebDriverWait(self, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "current"), page))
            return True
        except TimeoutException:
            return False

    # Get all links in page that has css class "XTitle"
    def links(self, title):
        return self.find_elements_by_class_name(title + "Title")
