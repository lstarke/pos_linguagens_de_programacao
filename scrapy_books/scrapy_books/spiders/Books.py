# -*- coding: utf-8 -*-
import scrapy
import re
from word2number import w2n

from scrapy_books.items import BooksItem


class BooksSpider(scrapy.Spider):
    name = 'Books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):

        for article in response.css("article"):
            book_page = article.css("h3 a::attr(href)").get()
            yield response.follow(book_page, self.parse_book)

        next_page = response.css(".pager .next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(url=next_page)

    def parse_book(self, book):

        name = book.css("h3 a::attr(title)").get()
        category = book.css(".breadcrumb li a ::text").getall()[2]

        keys = book.css("table th ::text").getall()
        values = book.css("table td ::text").getall()
        book_info = dict(zip(keys, values))

        price = float(re.findall('\d+\.\d+', book_info.get("Price (excl. tax)"))[0])
        stars_word = book.css(".star-rating").xpath("@class").extract_first().split(" ")[1]
        stars_number = w2n.word_to_num(stars_word)
        in_stock = int(re.findall('\d+', book_info.get("Availability"))[0])
        availability = True if in_stock > 0 else False

        book = BooksItem(name=name, price=price, stars=stars_number,
                         in_stock=in_stock, availability=availability, upc=book_info.get("UPC"),
                         product_type=book_info.get("Product Type"), category=category)

        yield book