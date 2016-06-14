#!/usr/bin/env python

# import needed libraries
from Browser import GoodReadsBrowser


# A class to Search then Scrape lists and books from GoodReads.com
class Books:
    keyword = None

    def __init__(self, keyword=None):
        self.br = GoodReadsBrowser()
        self.set_keyword(keyword)
        # An array for scrapped lists and books
        self.lists = set()
        self.books = set()

    # Scrape books and write them to a file
    def write_books(self, file_name="books.txt"):
        books = open(file_name, 'w')
        # Loop through book ids and write them
        for book_id in self.get_books():
            books.write(book_id + '\n')
        books.close()

    # Read already scraped books to the array
    def read_books(self, file_name="books.txt"):
        books = open(file_name, 'r')
        # Loop through all books ids from file
        for book_id in books:
            # Add book id to array without new line
            self.books.add(book_id.replace('\n', ''))
        books.close()
        return self.books

    # Main function to scrape books ids
    def get_books(self):
        # Return books array if it's not empty
        if self.books != set():
            return self.books
        # Loop through all lists
        for list_id in self.get_lists():
            # Open each list url
            self.br.open_list(list_id)
            # Scrape pages until there's no next page
            while True:
                self.__scrape_list("book", self.books)
                if self.br.has_next_page():
                    self.br.goto_next_page()
                else:
                    break
        return self.books

    # Main function to scrape lists ids
    def get_lists(self):
        # Return lists array if it's not empty
        if self.lists != set():
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
            # Extract and store unique id from link
            array.add(link.get_attribute("href")[36:].split('.')[0].split('-')[0])
            print(title + ' ' + str(len(array)))
