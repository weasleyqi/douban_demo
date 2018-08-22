import scrapy

from douban.items import DoubanMovie

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector


class Douban(CrawlSpider):
    name = "douban"
    redis_key = "douban:start_urls"
    start_urls = ['https://movie.douban.com/top250']

    url = 'https://movie.douban.com/top250'

    def parse(self, response):
        # print response.body
        item = DoubanMovie()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            title = eachMovie.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                fullTitle += each.strip()

            print fullTitle
            movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
            fullInfo = ''
            for info in movieInfo:
                fullInfo += info.strip()

            star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span/text()').extract()[0].strip()
            quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0].strip()
            else:
                quote = ''
            item['title'] = fullTitle
            item['movieInfo'] = fullInfo
            item['star'] = star
            item['quote']= quote
            yield item

        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            yield Request(self.url+nextLink  , callback = self.parse)


