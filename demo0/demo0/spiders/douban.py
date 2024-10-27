
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from ..items import MovieItem

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]

    def start_requests(self):
        meta = {'proxy':''}
        
        total = 250
        limit = 25
        for i in range(0,total,limit):
            url = f'https://movie.douban.com/top250?start={i}&filter='
            yield Request(url)


    def parse(self, response:HtmlResponse):
        item = MovieItem()
        blocks = response.css('.item .info')
        for it in blocks:
            try:
                item['title'] = it.css('span.title::text').get()
                item['rank'] = it.css('span.rating_num::text').get()
                item['subject'] = it.css('span.inq::text').get()
                detail_link = it.css('.hd a::attr(href)').get()

                # yield Request(url=detail_link,
                #             callback=self.parse_detail,
                #             meta={'item':item}
                #             )
                yield item

            except Exception as e:
                print(f"Error extracting {e}")

    def parse_detail(self,response:HtmlResponse):
        item = response.meta['item']
        try:
            item['duration'] = response.css('span[property="v:runtime"]::attr(content)').get()
            item['intro'] = response.css('span[property="v:summary"]::text').get().strip()
        except Exception as e:
                print(f"Error extracting {e}")

        yield item



