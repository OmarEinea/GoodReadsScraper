#!/usr/bin/env python

# Download link: https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from Tools import write_books, read_books, id_from_url


class Browser(Chrome):
    OPTIONS = {"goog:chromeOptions": {
        # Disable images loading
        "prefs": {"profile.managed_default_content_settings.images": 2},
        # Disable Chrome's GUI
        "args": ["--headless", "--disable-gpu"]
    }}

    def __init__(self):
        Chrome.__init__(self, desired_capabilities=self.OPTIONS)
        # Set page loading timeout to 30 seconds
        self.set_page_load_timeout(30)
        # Initialize browsing counters
        self.rating = self.sort = self.fails = None

    # Starts browser window
    def start(self):
        self.start_session(self.OPTIONS)

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
        # Get book id from URL
        url_id = id_from_url.match(self.current_url).group(1)
        # If a book id redirect happened
        if book_id != url_id:
            # Update new book id in books.txt
            ids = read_books()
            ids[ids.index(book_id)] = url_id
            write_books(ids)
            raise ConnectionResetError(f"Redirect book id from {book_id} to {url_id}")
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
            return False
        # Return none if there isn't one
        except Exception as error:
            print(error)
            return None

    def switch_reviews_mode(self, book_id, only_default=False):
        self.sort += 1
        if self.sort > 2 or only_default:
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
    def titles_links(self, title):
        return self.find_elements_by_class_name(title + "Title")

    _SORTS = ["default", "newest", "oldest"]
