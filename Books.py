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
        # An array for scrapped lists and books
        self.lists = []
        self.books = []

    # Scrape books and write them to a file (browse is: list, lists or shelf)
    def output_books(self, keyword, browse="list", file_name="books"):
        self.wr.open(file_name)
        # Loop through book ids and write them
        for book_id in self.get_books(keyword, browse):
            self.wr.write(book_id)
        self.wr.close()

    # Main function to scrape books ids
    def get_books(self, keyword, browse="list"):
        # Replace spaces with '+' for a valid url
        keyword = str(keyword).replace(' ', '+')
        # Get lists in search list if searching
        if browse == "lists":
            keywords = self.get_lists(keyword)
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
                self._scrape_list("book", self.books)
                if self.br.has_next_page():
                    self.br.goto_next_page()
                else:
                    break
        return self.books

    # Main function to scrape lists ids
    def get_lists(self, keyword):
        # Open GoodReads' lists search url
        self.br.open_list_search(keyword)
        # Scrape all result pages
        while True:
            self._scrape_list("list", self.lists)
            if self.br.has_next_page():
                self.br.goto_next_page()
            else:
                break
        return self.lists

    # Scrape a single search results page
    def _scrape_list(self, title, array):
        # Loop through all link that start with sub_url
        for link in self.br.links(title):
            # Get id from url
            id_ = link.get_attribute("href")[36:].split('.')[0].split('-')[0]
            # Extract and store unique id from link
            if id_ not in array:
                array.append(id_)
                print(title + '\t' + "%-10s" % id_ + "count: " + str(len(array)))
