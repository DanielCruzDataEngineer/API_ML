import scrapy
import os
import regex as re
class MlSpider(scrapy.Spider):
    name = 'ml'
    item = os.environ.get('VAR1')
    start_urls = [f'https://lista.mercadolivre.com.br/{item}']

    def parse(self, response, **kwargs):
        for i in response.xpath('//li[@class="ui-search-layout__item shops__layout-item"]'):
            price = i.xpath(".//span[@class='price-tag-fraction']//text()").get()
            title = i.xpath(".//h2[@class='ui-search-item__title shops__item-title']/text()").get()
            link = i.xpath(".//a[@class='ui-search-item__group__element shops__items-group-details ui-search-link']/@href").get()
            desconto = i.xpath(".//span[@class='ui-search-price__discount shops__price-discount']/text()").get()
            valor_parcelado = i.xpath(".//span[@class='price-tag-text-sr-only']/text()").get()
            
            if desconto == None:
                desconto = 'Sem desconto'
            if valor_parcelado.__contains__('con'):
                valor_parcelado = re.sub(re.compile("(\d+)\s*reais\s*con\s*(\d+)\s*centavos\s*"),r"\1,\2",valor_parcelado)
            elif valor_parcelado.__contains__('Antes:'):
                valor_parcelado = valor_parcelado.replace('Antes:','')
            elif valor_parcelado.__contains__('\''):
                valor_parcelado = valor_parcelado.replace('\'','')
            elif valor_parcelado.__contains__('reais'):
                valor_parcelado = valor_parcelado.replace(' reais ',',00')
            
            yield {
                'price': price,
                'title': title,
                'link': link,
                'desconto':desconto,
                'valor_com_parcelas':valor_parcelado
            }

        next_page = response.xpath('//a[contains(@title, "Seguinte")]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)