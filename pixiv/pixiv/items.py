# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PixivPicItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    img_urls = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    illust_id = scrapy.Field()
    url = scrapy.Field()
    image_paths = scrapy.Field()
    desc = scrapy.Field()
