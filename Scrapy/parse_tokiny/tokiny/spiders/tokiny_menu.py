import scrapy
import requests

from bs4 import BeautifulSoup
from scrapy import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tokiny.items import Product


class MenuSpider(CrawlSpider):
    name = 'tokiny_menu'
    allowed_domains = ['tokiny.by']
    start_urls = ['https://tokiny.by/']

    rules = (
        Rule(LinkExtractor(allow=('/menyu/',),
                           deny=('index.php', 'search', 'tag', 'revblog_blog', 'jpg', 'png', 'page',
                                 'uploads', 'autor', 'simpleregister', 'my_account',)),
             callback='parse', follow=True),

    )

    def parse(self, response, **kwargs):
        item = Product()
        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('//div[@class="price"]//span/text()').get()
        item['description'] = response.xpath('//div[@class="item-popup-description"]/text()').get()
        item['product_url'] = response.url
        item['images'] = response.xpath('//div[@class="big-img-holder"]//url/@src').get()
        yield item
