import scrapy
from ..items import TutorialItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

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

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)