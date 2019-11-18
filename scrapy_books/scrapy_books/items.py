# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stars = scrapy.Field()
    in_stock = scrapy.Field()
    availability = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    category = scrapy.Field()


