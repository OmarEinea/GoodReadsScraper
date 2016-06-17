#!/usr/bin/env python

# import needed libraries
from Browser import Browser
from Writer import Writer


# A class to Search then Scrape lists and books from GoodReads.com
class Books:
    keyword = None

    def __init__(self, keyword=None):
        # Browsing and writing managers
        self.br = Browser()
        self.wr = Writer()
        self.set_keyword(keyword)
        # An array for scrapped lists and books
        self.lists = []
        self.books = []

    # Scrape books and write them to a file
    def output_books(self, list_=None, file_name="books"):
        self.wr.open(file_name)
        # Loop through book ids and write them
        for book_id in self.get_books(list_):
            self.wr.write(book_id)
        self.wr.close()

    # Main function to scrape books ids
    def get_books(self, list_=None):
        # Return books array if it's not empty
        if not self.books == []:
            return self.books
        # Loop through all lists
        for list_id in self.get_lists(list_):
            # Open each list url
            self.br.open_list_page(list_id)
            # Scrape pages until there's no next page
            while True:
                self.__scrape_list("book", self.books)
                if self.br.has_next_page():
                    self.br.goto_next_page()
                else:
                    break
        return self.books

    # Main function to scrape lists ids
    def get_lists(self, list_=None):
        if list_:
            return [list_]
        # Return lists array if it's not empty
        if not self.lists == []:
            return self.lists
        # Open GoodReads' lists search url
        self.br.open_list_search(self.keyword)
        # Scrape all result pages
        while True:
            self.__scrape_list("list", self.lists)
            if self.br.has_next_page():
                self.br.goto_next_page()
            else:
                break
        return self.lists

    # Keyword setter
    def set_keyword(self, keyword):
        self.keyword = str(keyword).replace(' ', '+')

    # Scrape a single search results page
    def __scrape_list(self, title, array):
        # Loop through all link that start with sub_url
        for link in self.br.links(title):
            # Get id from url
            id_ = link.get_attribute("href")[36:].split('.')[0].split('-')[0]
            # Extract and store unique id from link
            if id_ not in array:
                array.append(id_)
                print(title + '\t' + id_ + '\t\t count: ' + str(len(array)))
