#!/usr/bin/env python

# import needed libraries
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# A GoodReads specific PhantomJS browser class
class Browser(PhantomJS):
    def __init__(self):
        """
        Download the PhantomJS driver for your OS
        from here: http://phantomjs.org/download.html
        Extract it then point to it in the superclass
        call below (instead of "./phantomjs")
        """
        PhantomJS.__init__(self, "./phantomjs")
        # Set page loading timeout to 15 seconds
        self.set_page_load_timeout(15)
        self._next_page = None

    # Login to Goodreads.com
    def login(self, email, password):
        # Open goodreads.com main page
        self.open()
        # Fill login form and submit it
        self.find_element_by_id("userSignInFormEmail").send_keys(email)
        self.find_element_by_id("user_password").send_keys(password)
        self.find_element_by_class_name("gr-button--signIn").click()

    # General shortcut to open a GoodReads page
    def open(self, sub_url='', keyword='', options=''):
        while True:
            try:
                self.get("https://www.goodreads.com" + sub_url + str(keyword) + options)
                break
            except TimeoutException:
                print("Reloading page")

    # Shortcut to open GoodReads book page
    def open_book_page(self, book_id, sort="newest"):
        self.open("/book/show/", book_id, "?text_only=true&sort=" + sort)

    # Shortcut to open GoodReads books list or shelf
    def open_page(self, keyword, browse):
        self.open("/" + browse + "/show/", keyword)

    # Shortcut to open a GoodReads search page for books lists
    def open_list_search(self, keyword):
        self.open("/search?q=", keyword, "&search_type=lists")

    # Check if there's a next page
    def has_next_page(self):
        # Try to find the next button
        try:
            self._next_page = self.find_element_by_class_name("next_page")
        # Return false if there isn't one
        except NoSuchElementException:
            return False
        # Check if button is click-able (i.e. it's anchor tag)
        return self._next_page.tag_name == 'a'

    # Click the next button to go to next page
    def goto_next_page(self):
        # If there's a next button
        if self._next_page:
            self._next_page.click()

    # Return if next page is loaded
    def is_page_loaded(self, page):
        try:
            # Let the driver wait until the current page indicator is active
            WebDriverWait(self, 10).until(ec.text_to_be_present_in_element((By.CLASS_NAME, "current"), page))
            return True
        except TimeoutException:
            return False

    # Get all links in page that has css class "XTitle"
    def links(self, title):
        return self.find_elements_by_class_name(title + "Title")
