#!/usr/bin/env python

from threading import Thread
import re, os

id_from_url = re.compile(r"^.*/([0-9]+).*$")
# Root path of reviews
path = "./BooksReviews/"


class SafeThread(Thread):
    def run(self):
        try:
            Thread.run(self)
        except AttributeError:
            Thread.join(self)
            raise AttributeError


def read_books(file_name="books"):
    try:  # Try reading the file
        with open(file_name + ".txt") as file:
            return file.read().splitlines()
    # If it's not there, return an empty list
    except FileNotFoundError:
        return []


def write_books(books_ids, file_name="books"):
    with open(file_name + ".txt", "w") as file:
        file.write("\n".join(books_ids))


# Combine all scraped reviews in one file
def combine_reviews():
    # Declare arrays and pointers to their add functions
    files, ids, bodies = [], set(), set()
    append, add_id, add_body = files.append, ids.add, bodies.add
    # Loop through all files in path
    for file in os.listdir(path):
        # If file is complete
        if file[0] == 'C':
            # Read file lines and store them
            lines = open(path + file, encoding='utf-8').readlines()
            append((len(lines) - 1, lines))
    # Combine books titles in this file
    write_books = open(path + "books.csv", "w+", encoding='utf-8').write
    # Combine reviews in this file
    write_reviews = open(path + "reviews.csv", "w+", encoding='utf-8').write
    # Sort files from largest to smallest and loop through them
    for file in sorted(files, reverse=True):
        reviews = file[1]
        # Loop through all file lines
        for i in range(len(reviews)):
            reviews[i] = reviews[i].split('\t', 2)
            # If review is book's description (i.e. third cell is rating not date)
            if reviews[i][2][0].isdigit():
                # Store book description line index
                book_index = i
        # Copy book description line index and write it to books.csv
        book = reviews[book_index][:]
        write_books('\t'.join(book))
        # Split the rest of its cells
        book[2:] = book[2].split('\t')
        book_id, author_id = book[0], book[3]
        # Delete it from file lines (keeping reviews only)
        del reviews[book_index]
        # Loop through the reviews
        for review in reviews:
            # Make sure review id isn't repeated
            id_ = review[0]
            if id_ not in ids:
                # Add it to array and write it to file
                add_id(id_)
                write_reviews('\t'.join([id_, review[1], book_id, author_id, review[2].replace("\u2028", ". ")]))


# Split the reviews from one file into n files
def split_reviews(n):
    # Store lines from reviews file
    lines = open("reviews.csv", 'r').readlines()
    # Make n number of steps in loop
    n = int(len(lines) / n)
    # Loop n times
    for i in range(0, len(lines), n):
        write = open("reviews" + str(int(i / n + 1)) + ".csv", "w+").write
        # Loop through chunks of reviews file
        for line in lines[i:i + n]:
            write(line)


# Counter for total lines written
def count_files_lines(from_file=None):
    total = 0
    # If counting specific set of books
    if from_file:
        files = set()
        # Add specified lines in file to an array
        for file in open("./" + from_file + ".txt").readlines():
            files.add("C_" + file.strip('\n') + ".txt")
    else:
        # Otherwise, store all files in path to array
        files = os.listdir(path)
    # Loop through all files
    for file in files:
        # If file is complete
        if file[0] == 'C':
            # Open file and add numbers of lines in file to total
            total = len(open(path + file, 'r').readlines()) - 1
    # Display and return total count
    print("Total Count:\t" + str(total))
    return total


# Delete all repeated reviews
def delete_repeated_reviews():
    repeated = 0
    invalid = 0
    ids = set()
    add_id = ids.add
    reviews = set()
    add_rev = reviews.add
    # Loop through all files in path
    for file in os.listdir(path):
        dir_ = path + file
        # Only count completed files
        if file[0] == 'C':
            # Read file lines and store them
            f = open(dir_, 'r')
            lines = f.readlines()
            f.close()
            # Write lines to the same file after erasing it
            f = open(dir_, 'w')
            f_write = f.write
            f_write(lines[0])
            # Loop through all reviews lines
            for line in lines[1:]:
                # Get line cells
                cells = line.split('\t')
                if len(cells) != 5:
                    invalid += 1
                    continue
                # Store id
                id_ = cells[0]
                # Review here is "date <tab> rating <tab> text"
                review = '\t'.join(cells[2:])
                # If id isn't repeated
                if id_ not in ids:
                    # Add it to array and write it to file
                    add_id(id_)
                    if review not in reviews:
                        add_rev(review)
                        f_write(line.replace("\u2028", ". "))
                # If it's repeated, count it
                else:
                    repeated += 1
            f.close()
            # If some files became empty after deleting
            if len(open(dir_, 'r').readlines()) < 2:
                # Rename file from "C_" to "E_"
                os.rename(dir_, path + "E_" + file[2:])
    # Display counts and return all reviews ids
    print("Total Non-Repeated:\t" + str(len(reviews)))
    print("Total Invalid By Cells:\t" + str(invalid))
    print("Total Repeated By ID:\t" + str(repeated))
    print("Total Repeated By Text:\t" + str(len(ids) - len(reviews)))
    return ids


def get_empty_files():
    write_empty = open("empty.txt", "w+").write
    for file in os.listdir(path):
        # Only count completed files
        if file[0] == 'E':
            write_empty(file[2:-4] + '\n')


def compare_two_files(file1, file2):
    with open(file1, encoding='utf-8') as file1, open(file2, encoding='utf-8') as file2:
        reviews1 = file1.readlines()
        reviews2 = file2.readlines()
        reviews_ids = set(review.split('\t', 1)[0] for review in reviews1 + reviews2)
        print("Total Reviews:", len(reviews_ids))
        print("Repeated Reviews:", len(reviews1) + len(reviews2) - len(reviews_ids))
        print("Unique Reviews in First File:", len(reviews_ids) - len(reviews2))
        print("Unique Reviews in Second File:", len(reviews_ids) - len(reviews1))
