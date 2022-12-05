import scrapy


class FirstspiderSpider(scrapy.Spider):
    name = 'firstSpider'
    allowed_domains = ['qutes.toscrape.com']
    start_urls = ['http://qutes.toscrape.com/']

    def parse(self, response):
        xpath_parse = response.xpath('/html/body/div[1]/div[2]/div[1]/div')
        for xpath in xpath_parse:
            item={}
            item['text'] = xpath.xpath('./span[1]/text()').extract_first().replace('“','').replace('”','')
            item['author']=xpath.xpath('./span[2]/small/text()').extract_first()
            print(item)
        pass
