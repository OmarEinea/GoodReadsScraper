#!/usr/bin/env python

# import needed libraries
from bs4 import BeautifulSoup
from langdetect import detect
from Browser import GoodReadsBrowser
import time, os, codecs


class Reviews:
    def __init__(self):
        self.br = GoodReadsBrowser()
        self.ids = []
        self.invalid = 0
        self.diff_lang = 0
        self.repeated = False
        self.file = None
        self.dir = "./BooksReviews/"

    def write_book_reviews(self, book_id):
        self.br.open_book(book_id)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.file = codecs.open(self.dir + str(book_id) + ".txt", "a+", "utf-8")
        while True:
            self._scrape_book(self.br.page_source)
            if self.invalid > 5 or self.diff_lang > 10 or not self.br.has_next_page():
                break
            if not self.br.goto_next_page(self.repeated):
                self.repeated = False
            time.sleep(2)

    def _scrape_book(self, html):
        soup = BeautifulSoup(html, "lxml").find(id="bookReviews")
        for review in soup.find_all(class_="bodycol"):
            rating = review.find(class_="staticStars")
            readable = review.find(class_="readable")
            if not rating or not readable:
                self.invalid += 1
                continue
            self.invalid = 0
            comment = (readable.find(style="display:none") or readable.find()).text
            try:
                if detect(comment) != "ar":
                    raise Exception
            except:
                self.diff_lang += 1
                continue
            self.diff_lang = 0
            stars = str(self.SWITCH[rating.find().text])
            self._write_review(stars, comment, readable.get("id")[19:])

    def _write_review(self, stars, comment, review_id):
        if review_id in self.ids:
            print("Repeated ID:", end=" ")
            self.repeated = True
        else:
            self.ids.append(review_id)
            self.file.write(stars + ' ' + comment + '\n')
            print("Added ID:", end=" ")
        print(review_id)

    SWITCH = {"it was amazing": 5, "really liked it": 4, "liked it": 3, "it was ok": 2, "did not like it": 1}
