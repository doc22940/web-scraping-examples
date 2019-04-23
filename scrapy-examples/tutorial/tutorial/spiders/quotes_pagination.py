import scrapy
from ..items import TutorialItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes_pagination'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]
    page_number = 2

    def parse(self, response):
        items = TutorialItem()
        quote_nodes = response.css("div.quote")

        for node in quote_nodes:
            quote = node.css("span.text::text").getall()
            author = node.css(".author::text").getall()
            tags = node.css(".tag::text").getall()

            items["quote"] = quote
            items["author"] = author
            items["tags"] = tags

            yield items

        next_page = "http://quotes.toscrape.com/page/" + str(QuoteSpider.page_number) + "/"
        if QuoteSpider.page_number < 11:
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)