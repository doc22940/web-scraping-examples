import scrapy


class GetCurrencySpider(scrapy.Spider):
    name = 'get_currency'
    start_urls = ['https://www.bloomberght.com/doviz/']

    def parse(self, response):
        currency_divs = response.css("#HeaderMarkets a")

        yield {
            "BIST 100": currency_divs[0].css(".LastPrice::text").get(),
            "USD/TRY": currency_divs[1].css(".LastPrice::text").get(),
            "EUR/TRY": currency_divs[2].css(".LastPrice::text").get(),
            "EUR/USD": currency_divs[3].css(".LastPrice::text").get(),
            "FAIZ": currency_divs[4].css(".LastPrice::text").get(),
            "ALTIN/ONS": currency_divs[5].css(".LastPrice::text").get(),
            "BRENT": currency_divs[6].css(".LastPrice::text").get()
        }

