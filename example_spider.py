# spider to scrap data from l'office des spectacles
# need to update the 'start_url' each month

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
            theme = selector.xpath('.//a/text()').extract()
            theme_link = selector.xpath('.//a/@href').extract()
            self.log(theme)
            self.log(theme_link)

            if theme_link[0].startswith('http://www.poesie-francaise.fr/poemes-'):
                request_details = scrapy.Request(theme_link[0], self.parse_theme)
                request_details.meta['data'] = {
                    'theme': theme[0],
                    'link_theme': theme_link[0]
                }
                self.log('new request')
                yield request_details

    def parse_theme(self, response):
        data = response.meta['data']
        self.log('Scraping poems from theme' + data['theme'])
        answer = response.xpath('.//div[@class="poemes-auteurs"]/ul/li')

        for selector in answer:
            poem_links = selector.xpath('.//a/@href').extract()
            for link in poem_links:
                if not link.startswith('http://poesie-francaise.fr/poemes'):
                    poem_link = link
                    self.log(poem_link)
                    break
            poem_infos = selector.xpath('.//a/text()').extract()
            poem_title = ''
            for info in poem_infos:
                if not info.startswith('.'):
                    poem_title = info
                    self.log(poem_title)
                    break

            data['title'] = poem_title
            data['link_poem'] = poem_link
            request_details = scrapy.Request(poem_link, self.parse_poem)
            request_details.meta['data'] = data
            self.log('new request theme')
            yield request_details

    def parse_poem(self, response):
        data = response.meta['data']
        self.log('Scraping ' + data['title'])
        author = response.xpath('//h3[contains(@class,"titrepoeme")]/a/text()').extract()
        book = response.xpath('//p[contains(@class,"soustitre")]/a/text()').extract()
        text = response.xpath('//div[contains(@class,"postpoetique")]/p/text()').extract()
        self.log(author)
        self.log(book)
        self.log(text)
        data['author'] = author[0]
        data['book'] = book[0]
        data['text'] = text

        yield data
