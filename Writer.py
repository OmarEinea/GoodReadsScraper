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
        self._empty = None

    # Path setter
    def set_path(self, path):
        self._path = path

    # Counter for total lines written
    def count_files_lines(self):
        total = 0
        # Loop through all files in path
        for file in os.listdir(self._path):
            # Only count completed files
            if file[0] == 'C':
                # Open file as read only
                self.open(file[:-4], 'r', self._path)
                # Add numbers of lines in file to total
                total += len(self._file.readlines()) - 1
        # Display and return total count
        print("Total Count:\t" + str(total))
        return total

    # Discard empty and complete files
    def consider_written_files(self, array):
        self.prepare_path()
        # Loop through files in the chosen path
        for file in os.listdir(self._path):
            # If file starts with C_ or E_
            if not file[0].isdigit():
                # Try to remove it from array
                try:
                    array.remove(file[2:-4])
                except:
                    pass

    # Create folder if it isn't already there
    def prepare_path(self):
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    # General shortcut to open a file for writing
    def open(self, name, key='w', path="./"):
        self._file = codecs.open(path + name + self._format, key, "utf-8")

    # Open file to write book reviews
    def open_book_file(self, name):
        self.prepare_path()
        # Delete file if it already exists
        if os.path.exists(self._path + str(name) + self._format):
            os.remove(self._path + str(name) + self._format)
        # Open the book reviews file with utf-8 encoding
        self.open(str(name), "a+", self._path)
        # File is empty once you open it
        self._empty = True

    # General shortcut to write a string to file
    def write(self, string):
        self._file.write(string + '\n')

    # Write review to file
    def write_review(self, id_, date, stars, comment):
        self.write(id_ + '\t' + date + '\t' + str(stars) + '\t' + comment)
        # If a review is written, file isn't empty anymore
        if self._empty:
            self._empty = False

    # Write book meta data to file
    def write_book_meta(self, book_id, title, rating, id_, name):
        self.write(str(book_id) + '\t' + title + '\t' + rating + '\t' + id_ + '\t' + name)

    # General shortcut to close the file
    def close(self):
        self._file.close()

    # Flag file as empty or complete and close it
    def close_book_file(self):
        # If no reviews were added mark file as empty, otherwise mark it as complete
        os.rename(self._file.name, self._path + ("C_", "E_")[self._empty] + self._file.name.split(self._path)[1])
        # Close file
        self.close()

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
