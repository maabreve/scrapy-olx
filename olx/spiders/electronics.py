# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from olx.items import OlxItem


class ElectronicsSpider(CrawlSpider):
    name = "electronics"
    allowed_domains = ["www.olx.com.pk"]
    start_urls = [
        'https://www.olx.com.pk/agriculture/',
        # 'https://www.olx.com.pk/tv-video-audio/',
        # 'https://www.olx.com.pk/games-entertainment/'
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pageNextPrev',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        item_links = response.css('.lpv-item-link::attr(href)').extract()
        for a in item_links:
            print('----------->', a)
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        print('--******__ entrou no detalhe')
        title = response.css('h1::text').extract()[0].strip()
        price = response.css('.pricelabel > .xxxx-large').extract()[0]

        item = OlxItem()
        item['title'] = title
        item['price'] = price
        item['url'] = response.url
        print('ah caraio')
        yield item

