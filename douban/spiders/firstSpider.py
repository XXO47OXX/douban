import scrapy
from scrapy import Selector,Request
from douban.items import MovieItem
from scrapy.http import HtmlResponse

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    def start_requests(self):
        for page in range(10):
            yield Request(url=f'https://movie.douban.com/top250?start={page*25}&fillter=',
                          meta={'proxy':'http://127.0.0.1:7890/'})
            proxies={
                'http':'http://127.0.0.1:7890/',
                'https':'http://127.0.0.1:7890/',
            }
    def parse(self, response:HtmlResponse,**kwargs):
        sel = Selector(response)
        list_items=sel.css('#content >div >div.article >ol >li')
        for list_item in list_items:
            #sel.css('#content >div >div.article >ol >li:nth-child(1)>div>div.info >div.hd>a')
            detail_url=sel.css('div.info >div.hd>a::attr(href)').extract_first()

            movie_item=MovieItem()
            movie_item['title']=list_item.css('span.title::text').extract_first()
            movie_item['rank']=list_item.css('span.rating_num::text').extract_first()
            movie_item['subject']=list_item.css('span.inq::text').extract_first() or ''
            yield Request(
                url=detail_url,callback=self.parse_detail,
                cb_kwargs = {'item':movie_item}
            )
            #yield movie_item
       # hrefs_list=sel.css('div.paginator>a::attr(href)')
        #for href in hrefs_list:
         #   url =response.urljoin(href.extract())
          #  yield Request(url=url)
    def parse_detail(self,response,**kwargs):
        movie_item=kwargs['item']
        sel= Selector(response)
        movie_item['durartion']=sel.css('span[property="v:runtime"]::attr(content').extract()
        movie_item['intro']=sel.css('span[property=v:summary]::text').extract_first() or''
        yield movie_item