#!/usr/bin/env python

# import needed libraries
import codecs
import os


# A class to Write Books and Reviews from GoodReads.com to files
class Writer:
    def __init__(self):
        # File to write book reviews in
        self._file = None
        # Path to write files in
        self._path = "./BooksReviews/"
        # Output file format
        self._format = ".txt"
        # Flag whether file is empty
        self._empty = True

    # Path setter
    def set_path(self, path):
        self._path = path

    # File format setter
    def set_format(self, format_):
        self._format = format_

    # Discard empty and complete files
    def consider_written_files(self, array):
        self._prepare_path()
        # Loop through files in the chosen path
        for file in os.listdir(self._path):
            # If file starts with C_ or E_
            if not file[0].isdigit():
                # Try to remove it from array
                if file[2:-4] in array:
                    array.remove(file[2:-4])
        if os.path.exists("empty.txt"):
            for file in open("empty.txt", "r").readlines():
                if file in array:
                    array.remove(file)

    # Create folder if it isn't already there
    def _prepare_path(self):
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    # General shortcut to open a file for writing
    def open(self, name, key="w", path="./"):
        self._file = codecs.open(path + name + self._format, key, "utf-8")

    # Open file to write book reviews
    def open_book_file(self, name):
        self._prepare_path()
        # Delete file if it already exists
        if os.path.exists(self._path + str(name) + self._format):
            os.remove(self._path + str(name) + self._format)
        # Open the book reviews file with utf-8 encoding
        self.open(str(name), "a+", self._path)

    # General shortcut to write a string to file
    def write(self, string):
        self._file.write(string + "\n")

    # Write review to file
    def write_review(self, review_id, user_id, date, stars, comment):
        self.write("\t".join([review_id, user_id, date, str(stars), comment]))
        # File isn't empty anymore
        self._empty = False

    # Write book meta data to file
    def write_book_meta(self, book_id, title, rating, author_id, name):
        self.write("\t".join([str(book_id), title, rating, author_id, name]))

    # General shortcut to close the file
    def close(self):
        self._file.close()

    # Flag file as empty or complete and close it
    def close_book_file(self):
        # Close file
        self.close()
        # If no reviews were added mark file as empty, otherwise mark it as complete
        os.replace(self._file.name, self._path + ("C_", "E_")[self._empty] + self._file.name.split(self._path)[1])

