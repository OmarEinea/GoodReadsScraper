#!/usr/bin/env python

# import needed libraries
import os
# Root path of reviews
path = "./BooksReviews/"
# A set of methods to manage scraped reviews from goodreads.com


# Combine all scraped reviews in one file
def combine_reviews():
    files = []
    append = files.append
    # Loop through all files in path
    for file in os.listdir(path):
        # If file is complete
        if file[0] == 'C':
            # Read file lines and store them
            lines = open(path + file, 'r').readlines()
            append((len(lines) - 1, lines))
    # Combine books titles in this file
    books = open("books.txt", "w+").write
    # Combine reviews in this file
    reviews = open("reviews.txt", "w+").write
    # Sort files from largest to smallest and loop through them
    for file in sorted(files, reverse=True):
        # Write first line to books.txt
        books(file[1][0])
        # Loop through the reset of the lines
        for line in file[1][1:]:
            # Write the reset of line to reviews.txt
            reviews(line.replace("\u2028", ". "))


# Split the reviews from one file into n files
def split_reviews(n):
    # Store lines from reviews file
    lines = open("reviews.txt", 'r').readlines()
    # Make n number of steps in loop
    n = int(len(lines) / n)
    # Loop n times
    for i in range(0, len(lines), n):
        write = open("reviews" + str(i / n + 1) + ".txt", "w+").write
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
            length = len(open(path + file, 'r').readlines()) - 1
            total += length
    # Display and return total count
    print("Total Count:\t" + str(total))
    return total


# Delete all repeated reviews
def delete_repeated_reviews():
    count = 0
    ids = set()
    add = ids.add
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
            f.write(lines[0])
            # Loop through all reviews lines
            for line in lines[1:]:
                # Get review id (that's before the first tab)
                id_ = line.split('\t')[0]
                # If id isn't repeated
                if id_ not in ids:
                    # Add it to array and write it to file
                    add(id_)
                    f.write(line)
                # If it's repeated, count it
                else:
                    count += 1
            f.close()
            # If some files became empty after deleting
            if len(open(dir_, 'r').readlines()) < 2:
                # Rename file from "C_" to "E_"
                os.rename(dir_, path + "E_" + file[2:])
    # Display counts and return all reviews ids
    print("Total Non-Repeated:\t" + str(len(ids)))
    print("Total Repeated:\t" + str(count))
    return ids


# Specific method for getting reviews from other source
def get_old_reviews(ids=set()):
    # Output file for old reviews
    f = open("old_reviews.txt", "w+")
    write = f.write
    add = ids.add
    # Open file as read only
    for line in open("reviews.txt", 'r').readlines():
        # Split line cells by tabs and store them
        cells = line.split('\t')
        id_ = cells[1]
        # If id isn't scraped previously
        if id_ not in ids:
            # Add it to array
            add(id_)
            # Write it to output file
            write(id_ + '\t' + "Unknown Date" + '\t' + cells[0] + '\t' + cells[4])
    # Display total count
    print("Total Non-Repeated:\t" + str(len(ids)))
