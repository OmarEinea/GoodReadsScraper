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
        # Backup for write_review()
        self._write_review = self.write_review

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
            for file in open("empty.txt", 'r').readlines():
                if file in array:
                    array.remove(file)

    # Create folder if it isn't already there
    def _prepare_path(self):
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    # General shortcut to open a file for writing
    def open(self, name, key='w', path="./"):
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
        self._file.write(string + '\n')

    # Write first review to file
    def write_review(self, review_id, user_id, date, stars, comment):
        # Write the review to the opened file
        self.write_review_to_file(review_id, user_id, date, stars, comment)
        # Change method to indicate that file isn't empty
        self.write_review = self.write_review_to_file

    # Write review to file
    def write_review_to_file(self, review_id, user_id, date, stars, comment):
        self.write('\t'.join([review_id, user_id, date, str(stars), comment]))

    # Write book meta data to file
    def write_book_meta(self, book_id, title, rating, author_id, name):
        self.write('\t'.join([str(book_id), title, rating, author_id, name]))

    # General shortcut to close the file
    def close(self):
        self._file.close()

    # Flag file as empty or complete and close it
    def close_book_file(self):
        # If write_review() is still equal to its backup, then file is empty
        empty = self._write_review == self.write_review
        # Restore write_review() from backup
        self.write_review = self._write_review
        # Close file
        self.close()
        # If no reviews were added mark file as empty, otherwise mark it as complete
        os.rename(self._file.name, self._path + ("C_", "E_")[empty] + self._file.name.split(self._path)[1])

    # Read already scraped books to the array
    def read_books(self, file_name="books"):
        books = []
        if os.path.exists("./" + file_name + self._format):
            self.open(file_name, 'r')
            # Loop through all books ids from file
            for book_id in self._file:
                # Add book id to array without new line
                books.append(book_id.replace('\n', ''))
            self.close()
        else:
            print("Can't find file to read from!")
        return books
