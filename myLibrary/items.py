# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class myLibraryItem(scrapy.Item):
        genre = scrapy.Field()
        title = scrapy.Field()
        isbn = scrapy.Field()
        author = scrapy.Field()
        publisher = scrapy.Field()
        brn = scrapy.Field()
