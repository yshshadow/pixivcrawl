# -*- coding: utf-8 -*-
import scrapy


class RankSpiderSpider(scrapy.Spider):
    name = "rank_spider"
    allowed_domains = ["pixiv.net"]
    start_urls = (
        'http://www.pixiv.net/',
    )

    def start_requests(self):
        setting = self.settings
        return [
                scrapy.FormRequest( url = 'https://www.secure.pixiv.net/login.php',
                                    formdata = {
                                        'pixiv_id':setting['PIXIV_USER_NAME'],
                                        'pass':setting['PIXIV_USER_PASS'],
                                        'skip':'1'
                                        'mode':'login'
                                    },
                                    callback=self.logged_in)
                ]

    def logged_in(self,response):
        pass

    def parse(self, response):
        pass
