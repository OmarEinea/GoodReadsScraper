#!/usr/bin/env python

# import needed libraries
import os, codecs


# A class to Write Books and Reviews from GoodReads.com to files
class Writer:
    def __init__(self):
        # File to write book reviews in
        self.file = None
        # Path to write files in
        self.path = "./BooksReviews/"
        # Output file format
        self.format = ".txt"
        self.empty = None

    # Path setter
    def set_path(self, path):
        self.path = path

    # Discard empty and complete files
    def consider_written_files(self, array):
        self.prepare_path()
        # Loop through files in the chosen path
        for file in os.listdir(self.path):
            # If file starts with C_ or E_
            if not file[0].isdigit():
                # Try to remove it from array
                try:
                    array.remove(file[2:-4])
                except: pass

    # Create folder if it isn't already there
    def prepare_path(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    # General shortcut to open a file for writing
    def open(self, name, key='w', path="./"):
        self.file = codecs.open(path + name + self.format, key, "utf-8")

    # Open file to write book reviews
    def open_book_file(self, name):
        self.prepare_path()
        # Delete file if it already exists
        if os.path.exists(self.path + str(name) + self.format):
            os.remove(self.path + str(name) + self.format)
        # Open the book reviews file with utf-8 encoding
        self.open(str(name), "a+", self.path)
        # File is empty once you open it
        self.empty = True

    # General shortcut to write a string to file
    def write(self, string):
        self.file.write(string + '\n')

    # Write review to file
    def write_review(self, id_, date, stars, comment):
        self.write(id_ + '\t' + date + '\t' + str(stars) + '\t' + comment)
        # If a review is written, file isn't empty anymore
        if self.empty:
            self.empty = False

    # Write book meta data to file
    def write_book_meta(self, book_id, title, rating, id_, name):
        self.write(str(book_id) + '\t' + title + '\t' + rating + '\t' + id_ + '\t' + name)

    # General shortcut to close the file
    def close(self):
        self.file.close()

    # Flag file as empty or complete and close it
    def close_book_file(self):
        # If no reviews were added mark file as empty, otherwise mark it as complete
        os.rename(self.file.name, self.path + ("C_", "E_")[self.empty] + self.file.name.split(self.path)[1])
        # Close file
        self.close()

    # Read already scraped books to the array
    def read_books(self, file_name="books"):
        books = []
        if os.path.exists("./" + file_name + self.format):
            self.open(file_name, 'r')
            # Loop through all books ids from file
            for book_id in self.file:
                # Add book id to array without new line
                books.append(book_id.replace('\n', ''))
            self.close()
        else:
            print("Can't find file to read from!")
        return books

