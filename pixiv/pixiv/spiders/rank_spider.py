# -*- coding: utf-8 -*-
import scrapy
import datetime
from pixiv.items import PixivPicItem

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
                                        'skip':'1',
                                        'mode':'login'
                                    },
                                    callback=self.logged_in)
                ]

    def logged_in(self,response):
        setting = self.settings
        for page in range(setting['PIXIV_RANK_PAGES']):
            yield scrapy.Request(self.generate_rank_url(page+1),callback=self.parse)

    def parse(self, response):
        pics = response.xpath('//div[@class="ranking-items adjust"]/section[@class="ranking-item"]')
        for pic in pics:
            item = PixivPicItem()
            item['title'] = pic.xpath('@data-title').extract()
            item['user_id'] = pic.xpath('@data-user-name').extract()
            item['user_name'] = pic.xpath('a[@class="user-container ui-profile-popup"]/@data-user_id').extract()
            detail_urls = pic.xpath('div[@class="ranking-image-item"]/a[@class="work  _work "]/@href').extract()
            detail_url = ''
            for url in detail_urls:
                detail_url = url
            yield scrapy.Request(
                    self.generate_detail_url(detail_url),
                    callback=self.parse_detail,
                    meta={'item':item},
                    headers={
                        'referer':response.url,
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
                        }
                    )

    def parse_detail(self,response):
        item = response.meta['item']
        item['url'] = response.url
        img_url = response.xpath('//img[@class="original-image"]/@data-src').extract()
        if(len(img_url)>0):
            item['img_urls'] = img_url
        yield item

    def generate_detail_url(self,detail_url):
        return 'http://www.pixiv.net/{0}'.format(detail_url)

    def generate_rank_url(self,page=1,date=datetime.date.today(),mode='daily'):
        rank_url = 'http://www.pixiv.net/ranking.php?mode={mode}&date={date}&p={page}'
        #if(isinstance(date,datetime.date)):
            
        return rank_url.format(date=date,page=page,mode=mode) 
