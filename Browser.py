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
        # Set page loading timeout to 30 seconds
        self.set_page_load_timeout(30)
        # Initialize browsing counters
        self.rating, self.sort, self.fails = None, None, 0

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
        self.sort = 0
        self.rating = 5
        self.open("/book/show/", book_id, f"?text_only=true&rating={self.rating}")
        print(f"Rating: {self.rating} Stars, Sorted: {self._SORTS[self.sort].capitalize()}")

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
        except (NoSuchElementException, TimeoutException, WebDriverException) as error:
            print(error)
            return False

    def switch_reviews_mode(self, book_id):
        self.sort += 1
        if self.sort >= 2:
            self.sort = 0
            self.rating -= 1
            if self.rating < 1:
                return False
        print(f"Rating: {self.rating} Stars, Sorted: {self._SORTS[self.sort].capitalize()}")
        self.execute_script(
            'document.getElementById("reviews").insertAdjacentHTML("beforeend", \'<a class="actionLinkLite'
            ' loadingLink" rel="nofollow" data-keep-on-success="true" data-remote="true" id="switch"'
            f'href="/book/reviews/{book_id}?text_only=true&rating={self.rating}&sort={self._SORTS[self.sort]}">'
            'Switch Mode</a>\');'
        )
        self.find_element_by_id("switch").click()
        return True

    # Return whether reviews were loaded
    def are_reviews_loaded(self):
        try:  # Add a dummy "loading" tag to DOM
            self.execute_script(
                'document.getElementById("reviews").'
                'insertAdjacentHTML("beforeend", \'<p id="load_reviews">loading</p>\');'
            )
            # Let the driver wait until the the dummy tag has disappeared
            WebDriverWait(self, 15).until(ec.invisibility_of_element_located((By.ID, "load_reviews")))
            self.fails = 0
            # Return true if reviews are loaded and they're more that 0, otherwise return false
            return len(self.find_element_by_id("bookReviews").find_elements_by_class_name("review")) > 0
        except Exception as error:
            print("Error:", error)
            # If reviews loading fails 3 times, raise an error
            self.fails += 1
            if self.fails == 3:
                raise ConnectionError
            return False

    # Get all links in page that has css class "XTitle"
    def links(self, title):
        return self.find_elements_by_class_name(title + "Title")

    _SORTS = ["default", "newest", "oldest"]
