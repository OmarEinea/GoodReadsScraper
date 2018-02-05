#!/usr/bin/env python

# Import needed libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
# Download link: https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium.webdriver import Chrome, ChromeOptions


class Browser(Chrome):
    def __init__(self):
        options = ChromeOptions()
        # Disable Chrome's GUI
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        Chrome.__init__(self, "./chromedriver.exe", chrome_options=options)
        # Set page loading timeout to 25 seconds '''
        self.set_page_load_timeout(25)

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
        # Try to open url until it succeeds
        while True:
            try:
                self.get(f"https://www.goodreads.com{sub_url}{keyword}{options}")
                break
            # On connection timeout, loop again
            except TimeoutException:
                print("Reloading page")

    # Shortcut to open GoodReads book page
    def open_book_page(self, book_id):
        self.open("/book/show/", book_id, "?text_only=true")

    # Shortcut to open GoodReads books list or shelf
    def open_page(self, keyword, browse):
        # URL contains "show" unless it's an author page
        method = "show" if browse != "author" else "list"
        self.open(f"/{browse}/{method}/{keyword}")

    # Shortcut to open a GoodReads search page for books lists
    def open_list_search(self, keyword):
        self.open("/search?q=", keyword, "&search_type=lists")

    # Check if there's a next page
    def goto_next_page(self):
        try:
            # Try to find the next button
            next_page = self.find_element_by_class_name("next_page")
            # Check if button is click-able (i.e. it's anchor tag)
            if next_page.tag_name == "a":
                # Click the next page button
                next_page.click()
                return True
        # Return false if there isn't one
        except (NoSuchElementException, TimeoutException, WebDriverException):
            return False

    # Return if next page is loaded
    def is_page_loaded(self, page):
        try:
            # Let the driver wait until the current page indicator is active
            WebDriverWait(self, 10).until(ec.text_to_be_present_in_element((By.CLASS_NAME, "current"), str(page)))
            return True
        except TimeoutException:
            return False

    # Get all links in page that has css class "XTitle"
    def links(self, title):
        return self.find_elements_by_class_name(title + "Title")
