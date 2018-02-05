#!/usr/bin/env python

# import needed libraries
from bs4 import BeautifulSoup
from langdetect import detect
from Browser import Browser
from Writer import Writer


# A class to Scrape books Reviews from GoodReads.com
class Reviews:
    def __init__(self, lang="ar"):
        # Language of reviews to be scraped
        self.lang = lang
        # Browsing and writing managers
        self.br = Browser()
        self.wr = Writer()
        # Counter for reviews from different languages
        self._invalid = None
        # Counter for current page number
        self._page = None
        # Array for possible 10th page ids
        self._reviews_ids = set()

    # Scrape and write books' reviews to separate files
    def output_books_reviews(self, books_ids, consider_previous=True):
        if consider_previous:
            # Don't loop through already scraped books
            self.wr.consider_written_files(books_ids)
        # Show how many books are going to be scraped
        print(f"Scraping {len(books_ids)} Books")
        # Loop through book ids in array and scrape books
        for book_id in books_ids:
            self.output_book_reviews(book_id)

    # Scrape and write one book's reviews to a file
    def output_book_reviews(self, book_id):
        # Open book file and page by its Id
        self.wr.open_book_file(book_id)
        self.br.open_book_page(book_id)
        # Reset invalid reviews counter and page counter
        self._invalid = 0
        self._page = 0
        # Scrape book meta data in first line
        self._scrape_book_meta(book_id, self.br.page_source)
        # Scrape first page of the book anyway
        self._scrape_book_page(self.br.page_source)
        # Scrape the remaining pages
        while self._invalid < 60:
            # Go to next page if there's one
            if not self.br.goto_next_page():
                # If there's a 10th page
                if 1 + self._page == 10:
                    # Order reviews from oldest and loop again
                    # self.br.open_book_page(book_id)
                    # TODO: Implement switch_to function
                    print("Switching to order by oldest")
                # Break if there's no next page
                else:
                    break
            # Moved to next page
            self._page += 1
            # Wait until next page is loaded
            if self.br.is_page_loaded(1 + self._page % 10):
                # Scrape book and break if it's completely done
                if not self._scrape_book_page(self.br.page_source):
                    break
        # Finalize file name and close it
        self.wr.close_book_file()

    # Scrape and write book and author data
    def _scrape_book_meta(self, book_id, html):
        # Create soup object from page html
        soup = BeautifulSoup(html, "lxml")
        # Store book meta section of the page in soup unless book not available
        soup = soup.find(id="metacol") or soup.find(class_="errorBox").get_text().strip()
        # If book is not found
        if soup == "Could not find this book.":
            print(f"*Book ID:\t{book_id:<15}Not Found!")
            # Close file and raise an error
            self.wr.close_book_file()
            raise FileNotFoundError
        # Get book title and remove spaces from it
        title = soup.find(id="bookTitle").get_text(". ", strip=True)
        # Get average rating of the book out of five
        rating = soup.find(class_="average").get_text()
        # Store author data section
        author = soup.find(class_="authorName")
        # Get author id from url
        id_ = author.get("href")[38:].split(".")[0]
        # Get author name
        name = author.find().get_text()
        # Write scraped meta data to file's first line
        self.wr.write_book_meta(book_id, title, rating, id_, name)
        # Display book id and title
        print(f"*Book ID:\t{book_id:<15}Title:\t{title}")

    # Scrape a single page's reviews
    def _scrape_book_page(self, html):
        # Store reviews section of the page in soup
        soup = BeautifulSoup(html, "lxml").find(id="bookReviews")
        # Loop through reviews individually
        for review in soup.find_all(class_="review"):
            try:
                # Get user / reviewer id
                user_id = review.find(class_="user").get("href")[11:].split("-")[0]
                # Get rating out of five stars
                stars = len(review.find(class_="staticStars").find_all(class_="p10"))
                # Get full review text even the hidden parts, and remove spaces and newlines
                comment = review.find(class_="readable").find_all("span")[-1].get_text(". ", strip=True)
                # Detect which language the review is in
                if detect(comment) != self.lang:
                    # Count it as a different language review
                    self._invalid += 1
                    continue
                # Get review date
                date = review.find(class_="reviewDate").get_text()
            # Skip the rest if one of the above is missing
            except Exception:
                # Count it as an invalid review
                self._invalid += 2
                continue
            # If it's not a strike, reset the counter
            self._invalid = 0
            # Get review ID
            review_id = review.get("id")[7:]
            # If it's the 10th page or passed it
            if 1 + self._page >= 10:
                # Store the 10th page reviews ids
                if 1 + self._page == 10:
                    self._reviews_ids.add(review_id)
                # Check that reviews aren't repeating
                elif review_id in self._reviews_ids:
                    self._reviews_ids.clear()
                    return False
            # Write the scraped review to the file
            self.wr.write_review(review_id, user_id, date, stars, comment)
            # Add review id to ids
            print(f"Added ID:\t{review_id}")
        return True

    def __del__(self):
        self.br.close()
        print("Closed browser")
