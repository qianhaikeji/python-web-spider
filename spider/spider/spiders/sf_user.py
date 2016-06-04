#-*- coding: utf-8 -*-
import urllib
from scrapy import Request

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from ..items import SegmentfaultUserItem

from datetime import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SegmentfaultUserSpider(CrawlSpider):
    name = 'sf_user'
    allowed_domains = ['segmentfault.com']

    def __init__(self, uid='miracledan', *args,  **kwargs):
        super(SegmentfaultUserSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://segmentfault.com/u/%s" % uid]

    #在用户主页爬取用户所有信息
    def parse(self, response):
        selector = Selector(response)

        user = SegmentfaultUserItem()
        user['_id']= user['username']=response.url.split('/')[-1]
        user['url']= response.url
        user['update_time'] = str(datetime.now())

        ranks = selector.xpath("//div[@class='profile__heading-info row']//span[@class='h3']/text()").extract()
        user['reputation'] = ranks[0]
        user['agree'] = ranks[1]
        user['follower'] = ranks[2]        

        return user
