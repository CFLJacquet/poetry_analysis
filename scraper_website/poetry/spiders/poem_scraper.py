import os
from unicodedata import normalize
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime as dt


class PoemSpider(scrapy.Spider):
    name = "poems"
    
    start_urls = [
        'http://www.poesie-francaise.fr/poemes-themes/'
    ]

    def parse(self, response):

        answer = response.xpath('.//div[@class="menu-centrale"]/ul/li')
        for selector in answer:
            theme = selector.xpath('.//a/text()').extract_first()
            theme_link = selector.xpath('.//a/@href').extract_first()
            self.log(theme)
            self.log(theme_link)

            if theme_link.startswith('http://www.poesie-francaise.fr/poemes-'):
                request_details = scrapy.Request(theme_link, self.parse_theme)
                request_details.meta['data'] = {
                    'theme': theme,
                    'link_theme': theme_link
                }
                self.log('new request')
                yield request_details

    def parse_theme(self, response):
        data = response.meta['data']
        self.log('Scraping poems from theme' + data['theme'])
        answer = response.xpath('.//div[@class="poemes-auteurs"]/ul/li')

        for selector in answer:
            poem_link = selector.xpath('.//a/@href').extract_first()
            
            request_details = scrapy.Request(poem_link, self.parse_poem)
            request_details.meta['data'] = data
            self.log('new request theme')
            yield request_details

    def parse_poem(self, response):
        data = response.meta['data']

        poem_link = response.url
        poem_title = response.xpath('//h2[contains(@class,"titrepoeme")]/text()').extract_first().replace('Titre : ','')
        author = response.xpath('//h3[contains(@class,"titrepoeme")]/a/text()').extract_first()
        book = response.xpath('//p[contains(@class,"soustitre")]/a/text()').extract_first()
        text = response.xpath('//div[contains(@class,"postpoetique")]/p/text()').extract()

        data['link_poem'] = poem_link
        data['title'] = poem_title
        data['author'] = author
        data['book'] = book
        data['text'] = "\n".join(text)

        yield data



process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'data/poems_extract2.json',
    'FEED_EXPORT_ENCODING': 'utf-8'
})

process.crawl(PoemSpider)
process.start() # the script will block here until the crawling is finished