# -*- coding: utf-8 -*-
import scrapy
from pixiv.items import PixivPicItem

class PixivSearchSpider(scrapy.Spider):
    name = "search_spider"
    allowed_domains = ["pixiv.net"]
    start_urls = (
        'http://www.pixiv.net/',
    )

    def start_requests(self):
        #print 'start'
        setting =self.settings
        return [
                scrapy.FormRequest( url = 'https://www.secure.pixiv.net/login.php',
                                    formdata = {
                                        'pixiv_id':setting['PIXIV_USER_NAME'],
                                        'pass':setting['PIXIV_USER_PASS'],
                                        'skip':'1',
                                        'mode':'login'
                                        },
                                    callback = self.logged_in)
                 ]

    def logged_in(self,response):
        #print 'sign in'
	setting =self.settings
	for page in range(setting['PIXIV_SEARCH_PAGES']):
            yield scrapy.Request('http://www.pixiv.net/search.php?order=date_d&word={0}&p={1}'.format(setting['PIXIV_SEARCH_KEYWORD'],page+1),callback=self.parse)

    def parse(self, response):
        pics = response.xpath('//ul/li[@class="image-item "]')
        for pic in pics:
            item = PixivPicItem()
            item['title'] = pic.xpath('a/h1[@class="title"]/@title').extract()
            item['user_id'] = pic.xpath('a[@class="user ui-profile-popup"]/@data-user_id').extract()
            item['user_name'] = pic.xpath('a[@class="user ui-profile-popup"]/@data-user_name').extract()
            detail_urls = pic.xpath('a[@class="work  _work "]/@href').extract()
            detail_url = ''
            for url in detail_urls:
                detail_url = url
            yield scrapy.Request(
                self.generate_detail_url(detail_url),
                callback=self.parse_detail,
                meta={'item':item}, 
                headers={
                    'referer':response.url,
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
                    }
                )

    def parse_detail(self,response):
        item = response.meta['item']
        item['url'] = response.url
        img_url = response.xpath('//img[@class="original-image"]/@data-src').extract()
        if (len(img_url) > 0):
            item['img_urls'] = img_url
        yield item
        
        
    def generate_detail_url(self,detail_url):
        return 'http://www.pixiv.net{0}'.format(detail_url)
