# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//div[@class='desc']/a)[1]"))
    )
    
    def parse_item(self, response):
        yield{
            'title' : response.xpath("normalize-space((//div[@class='title_wrapper']/h1/text())[1])").get(),
            'Year' : response.xpath("//h1/span/a/text()").get(),
            'duration' : response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(),
            'genre' : response.xpath("//div[@class='subtext']/a[contains(@href,'genre')]/text()").getall(),
            'Rating' : response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'Movie_url' : response.url
        }

