import scrapy


class GetRedditLinksSpider(scrapy.Spider):
    name = 'get_reddit_links'
    start_urls = ['https://www.reddit.com/r/webscraping/']

    def parse(self, response):
        title_divs = response.xpath('//a[@data-click-id=$val]', val='body')

        for title_div in title_divs:
            title_info = {
                "title": title_div.css('h2::text').get(),
                "link": response.urljoin(title_div.css('a::attr(href)').get())
            }

            yield title_info
