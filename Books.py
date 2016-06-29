#!/usr/bin/env python

# import needed libraries
from Browser import Browser
from Writer import Writer


# A class to Search then Scrape lists and books from GoodReads.com
class Books:
    def __init__(self):
        # Browsing and writing managers
        self.br = Browser()
        self.wr = Writer()
        # An array for scrapped books
        self._books_ids = []

    # Append an external books ids array to local array
    def append_books(self, books_ids):
        # Loop through sent books ids
        for book_id in books_ids:
            # Only append id if it's not stored already
            if book_id not in self._books_ids:
                self._books_ids.append(book_id)

    # Scrape books and write them to a file (browse is: list, lists, author or shelf)
    def output_books(self, keyword=None, browse="list", file_name="books"):
        self.wr.open(file_name)
        # Get books if keyword is provided, otherwise output stored books
        books_ids = self.get_books(keyword, browse) if keyword else self._books_ids
        # Loop through book ids and write them
        for book_id in books_ids:
            self.wr.write(book_id)
        self.wr.close()

    # Main function to scrape books ids
    def get_books(self, keyword, browse="list"):
        # Replace spaces with '+' for a valid url
        keyword = str(keyword).replace(' ', '+')
        # Get lists in search list if searching
        if browse == "lists":
            keywords = self._get_lists(keyword)
            browse = "list"
        # Otherwise, it's a single "list" or "shelf"
        else:
            keywords = [keyword]
        # Loop through all lists
        for keyword in keywords:
            # Open each list url
            self.br.open_page(keyword, browse)
            # Scrape pages until there's no next page
            while True:
                self._scrape_list("book", self._books_ids)
                if not self.br.goto_next_page():
                    break
        return self._books_ids

    # Main function to scrape lists ids
    def _get_lists(self, keyword):
        lists = []
        # Open GoodReads' lists search url
        self.br.open_list_search(keyword)
        # Scrape all result pages
        while True:
            self._scrape_list("list", lists)
            # Go to next page if there's one, otherwise break
            if not self.br.goto_next_page():
                break
        return lists

    # Scrape a single search results page
    def _scrape_list(self, title, array):
        # Loop through all link that start with sub_url
        for link in self.br.links(title):
            try:
                # Get id from url
                id_ = link.get_attribute("href")[36:].split('.')[0].split('-')[0]
            except:
                continue
            # Extract and store unique id from link
            if id_ not in array:
                array.append(id_)
                print(title + '\t' + "%-12s" % id_ + "count:\t" + str(len(array)))
