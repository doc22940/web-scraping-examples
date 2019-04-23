# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonBookItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_number = 2
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff&qid=1553871812&rnid=1250225011&ref=lp_283155_nr_p_n_publication_date_0'
    ]

    def parse(self, response):
        items = AmazonBookItem()
        products_div = response.css(".s-result-list.sg-row .a-section.a-spacing-medium")

        for product_div in products_div:
            items["title"] = product_div.css(".a-color-base.a-text-normal::text").get()
            items["author"] = product_div.css(".a-color-secondary .a-size-base+ .a-size-base::text").get().replace("\n","").strip()
            if product_div.css(".a-offscreen::text").get() is not None:
                items["new_price"] = float(product_div.css(".a-offscreen::text").get().replace("$",""))
            if len(product_div.css(".a-offscreen::text").getall()) > 1:
                items["old_price"] = float(product_div.css(".a-offscreen::text").getall()[1].replace("$",""))
            items["image_link"] = product_div.css(".s-image::attr(src)").get()
        
            yield items

        next_page = response.css("li.a-last a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)