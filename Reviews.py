#!/usr/bin/env python

# import needed libraries
from bs4 import BeautifulSoup
from langdetect import detect
from Browser import Browser
from Writer import Writer


# A class to Scrape books Reviews from GoodReads.com
class Reviews:
    def __init__(self):
        # Browsing and writing managers
        self.br = Browser()
        self.wr = Writer()
        # Counter for reviews from different languages
        self.invalid = None
        # Counter for current page number
        self.page = None
        # Array for possible 100th page ids
        self.ids = []

    # Scrape and write books' reviews to separate files
    def output_books_reviews(self, books_ids, consider_previous=True):
        if consider_previous:
            # Don't loop through already scraped books
            self.wr.consider_written_files(books_ids)
        # Loop through book ids in array and scrape books
        for book_id in books_ids:
            self.output_book_reviews(book_id)

    # Scrape and write one book's reviews to a file
    def output_book_reviews(self, book_id):
        # Open book file and page by its Id
        self.wr.open_book_file(book_id)
        self.br.open_book_page(book_id)
        # Reset invalid reviews counter and page counter
        self.invalid = 0
        self.page = 0
        # Scrape book meta data in first line
        self._scrape_book_meta(book_id, self.br.page_source)
        # Scrape first page of the book anyway
        self._scrape_book_page(self.br.page_source)
        # Scrape the remaining pages
        while self.invalid < 30:
            # Go to next page if there's one
            if self.br.has_next_page():
                self.br.goto_next_page()
            # If there's a 100th page
            elif 1 + self.page == 100:
                # Order reviews from oldest and loop again
                self.br.open_book_page(book_id, "oldest")
                print("Switching to order by oldest")
            # Break if there's no next page
            else:
                break
            # Moved to next page
            self.page += 1
            # Wait until next page is loaded
            if self.br.is_page_loaded(str(1 + self.page % 100)):
                # Scrape book and break if it's completely done
                if not self._scrape_book_page(self.br.page_source):
                    break
        # Finalize file name and close it
        self.wr.close_book_file()

    # Scrape and write book and author data
    def _scrape_book_meta(self, book_id, html):
        # Store book meta section of the page in soup
        soup = BeautifulSoup(html, "lxml").find(id="metacol")
        # Get book title and remove spaces from it
        title = soup.find(id="bookTitle").get_text(". ", strip=True)
        # Get average rating of the book out of five
        rating = soup.find(class_="average").text
        # Store author data section
        author = soup.find(class_="authorName")
        # Get author id from url
        id_ = author.get("href")[38:].split('.')[0]
        # Get author name
        name = author.find().text
        # Write scraped meta data to file's first line
        self.wr.write_book_meta(book_id, title, rating, id_, name)
        # Display book id and title
        print("*Book ID:\t" + str(book_id) + "\t\tTitle:\t" + title)

    # Scrape a single page's reviews
    def _scrape_book_page(self, html):
        # Store reviews section of the page in soup
        soup = BeautifulSoup(html, "lxml").find(id="bookReviews")
        # Loop through reviews individually
        for review in soup.find_all(class_="review"):
            try:
                # Get rating out of five stars
                stars = self.SWITCH[review.find(class_="staticStars").find().text]
                # Get full review text even the hidden parts, and remove spaces and newlines
                comment = review.find(class_="readable").find_all("span")[-1].get_text(". ", strip=True)
                # Detect which language the review is in
                if detect(comment) != "ar":
                    # Count it as a different language review
                    self.invalid += 1
                    continue
                # Get review date
                date = review.find(class_="reviewDate").text
            # Skip the rest if one of the above is missing
            except:
                continue
            # If it's not a strike, reset the counter
            self.invalid = 0
            # Get review ID
            id_ = review.get("id")[7:]
            # If it's the 100th page or passed it
            if 1 + self.page >= 100:
                # Store the 100th page reviews ids
                if 1 + self.page == 100:
                    self.ids.append(id_)
                # Check that reviews aren't repeating
                elif id_ in self.ids:
                    return False
            # Write the scraped review to the file
            self.wr.write_review(id_, date, stars, comment)
            # Add review id to ids
            print("Added ID:\t" + id_)
        return True

    # Switch reviews ratings to stars from 1 to 5
    SWITCH = {"it was amazing": 5, "really liked it": 4, "liked it": 3, "it was ok": 2, "did not like it": 1}
