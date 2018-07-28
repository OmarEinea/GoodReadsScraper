# GoodReads Reviews Scraper

This is a python 3 web scraping script to get books reviews from goodreads.com,<br>
using the web browser automation tool Selenium, and BeautifulSoup for pulling data out of HTML.<br>
I used it to scrape around 700k Arabic reviews in 2018 (Arabic reviews are fewer than English ones).

### Contents

- Analyzer.py: A short script to display some statistics about scraped books reviews
- Books.py: A class to scrape books ids from goodreads list or lists search or shelf
- Browser.py: A subclass of Chrome WebDriver class that's specialized for GoodrReads browsing
- Reviews.py: A class to scrape reviews from goodreads books using books ids
- Sample.py: A sample script showing a complete use of the scraper with error handling
- Tools.py: A set of function tools that are used in other scripts
- Writer.py: A class to write scraped reviews to files
- requirements.txt: A list of Required Python modules to be installed

### Requirements

To install requirements listed in requirements.txt, you'll need to run this (depends on your os):
```bash
pip install -r requirements.txt
```
Also, as this is using Selenium to control the Chrome Browser,<br>
so you'll need to download its driver for your specific os from
[here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

### Documentation

- A Books object (from Books.py) represents the books that are needed to be scraped.		<br>
	class Books() doesn't take any arguments

		Notes for the next two methods:
		browse could be one of the following:
		"shelf", "author", "lists" or "list" (by default)
		the keyword could be the id of a "shelf", an "author" or a "list"
		or it could be the search keyword in case you're searching for "lists"

	- Books.get_books(keyword, browse="list")												<br>
		Scrapes books ids an returns an array of them.

	- Books.output_books(keyword=None, browse="list", file_name="books")					<br>
		Scrapes books ids an writes them to a file set by									<br>
		sending file_name value without extension if none									<br>
		is sent, it'll write them to books.txt file by default

	- Books.append_books(books_ids)															<br>
		Append an external books ids array to class storage									<br>
		(Hint: it accepts what Books.get_books() returns)

- A Reviews object (from Reviews.py) represents the scraped reviews.						<br>
	class Reviews(lang="ar")																<br>
	lang is the language of reviews to look for / scrape, it could be: ([ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes))

		af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he,
		hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl,
		pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw

	- Reviews.output_book_reviews(book_id)													<br>
	Scrapes a book reviews and writes them to a file.

	- Reviews.output_books_reviews(self, books_ids, consider_previous=True)					<br>
	Scrapes reviews of an array of books and writes them to a file.							<br>
	consider_previous is set to whether to consider the books that have						<br>
	been already scraped or whether to delete them an start over

	- Reviews.wr.read_books(file_name="books")												<br>
	Reads books ids from file and returns them.

- Tools module methods:
	- Manager.count_files_lines()															<br>
	Returns and prints the total sum of scraped books lines

	- Manager.delete_repeated_reviews()														<br>
	Returns unique reviews ids and delete all repeated ones and prints info

	- Manager.combine_reviews()																<br>
	Writes a single "reviews.txt" file containing all reviews

	- Manager.split_reviews(n)																<br>
	splits the combined "reviews.txt" file into n smaller files

**Browser and Writer classes are only for implementation inside Books and Reviews Classes**

### Demo

Import needed modules:
```python
from Books import Books
from Reviews import Reviews
from Tools import *
```

Scrape books ids from books shelved as "arabic":
```python
b = Books()
books_ids = b.get_books("arabic", "shelf")
```

Scrape books reviews and write them to a file:
```python
r = Reviews("ar")
r.output_books_reviews(books_ids)
```

Filter Reviews then combine them:
```python
delete_repeated_reviews()
combine_reviews()
```

**A more comprehensive example can be found in Sample.py**

### Resources

> - [Selenium](http://www.seleniumhq.org/)
> - [LangDetect](https://github.com/Mimino666/langdetect)
> - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

### Reference

Omar Einea <eineao@gmail.com>

Supervised by Dr. Ashraf Elnagar.

University of Sharjah, United Arab Emarites, July 2016

### License

Copyright (C) 2018 by Omar Einea.

This is an open source tool licensed under GPL v3.0. Copy of the license can be found
[here](https://github.com/OmarEinea/GoodReads/blob/master/LICENSE.md).
