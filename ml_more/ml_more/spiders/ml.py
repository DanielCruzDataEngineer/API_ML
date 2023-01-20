import scrapy
import os

class MlSpider(scrapy.Spider):
    name = 'ml'
    item = os.environ.get('VAR1')
    start_urls = [f'https://lista.mercadolivre.com.br/{item}']

    def parse(self, response, **kwargs):
        for i in response.xpath('//li[@class="ui-search-layout__item shops__layout-item"]'):
            price = i.xpath(".//span[@class='price-tag-fraction']//text()").get()
            title = i.xpath(".//h2[@class='ui-search-item__title shops__item-title']/text()").get()
            link = i.xpath(".//a[@class='ui-search-item__group__element shops__items-group-details ui-search-link']/@href").get()

            yield {
                'price': price,
                'title': title,
                'link': link
            }

        next_page = response.xpath('//a[contains(@title, "Seguinte")]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)