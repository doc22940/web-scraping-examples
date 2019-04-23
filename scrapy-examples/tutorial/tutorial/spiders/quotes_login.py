import scrapy
from ..items import TutorialItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class QuoteSpider(scrapy.Spider):
    name = 'quotes_login'
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):
        token =  response.css("form input::attr(value)").get()
        return FormRequest.from_response(response, formdata={
            "csrf_token" : token,
            "username" : "test@gmail.com",
            "password" : "123456"
        }, callback = self.start_scraping)

    def start_scraping(self, response):
        open_in_browser(response)
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