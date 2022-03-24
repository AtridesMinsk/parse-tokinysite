import scrapy


class TokinyMenuSpider(scrapy.Spider):
    name = 'tokiny_menu'
    allowed_domains = ['parse_tokiny.by']
    start_urls = ['http://tokiny.by/']

    def parse(self, response):
        pass
