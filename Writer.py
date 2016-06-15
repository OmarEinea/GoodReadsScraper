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

    # Path setter
    def set_path(self, path):
        self.path = path

    # Discard already written files and delete incomplete ones
    def consider_written_files(self, array):
        # Loop through files in the chosen path
        for file in os.listdir(self.path):
            # If file starts with digit (so not with C_ or E_)
            if file[0].isdigit():
                # Then program was interrupted, delete file
                os.remove(self.path + file)
            else:
                # Otherwise, remove it from array
                try:
                    array.remove(file[2:-4])
                except: pass

    # General shortcut to open a file for writing
    def open(self, file, key='w', path="./"):
        self.file = codecs.open(path + file + self.format, key, "utf-8")

    # Open file to write book reviews
    def open_book_file(self, name):
        # Create folder if it isn't already there
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # Open the book reviews file with utf-8 encoding
        self.open(str(name), "a+", self.path)

    # General shortcut to write a string to file
    def write(self, string):
        self.file.write(string + '\n')

    # Write review to file
    def write_review(self, name, stars, comment):
        self.write(name + '\t' + str(stars) + '\t' + comment)

    # General shortcut to close the file
    def close(self):
        self.file.close()

    # Flag file as empty or complete and close it
    def close_book_file(self, length):
        # If no reviews were added
        if length == 0:
            # Rename as an empty file
            os.rename(self.file.name, self.path + "E_" + self.file.name.split(self.path)[1])
        else:
            # Otherwise, rename as a complete file
            os.rename(self.file.name, self.path + "C_" + self.file.name.split(self.path)[1])
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

