import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
import json

class ReutersArticleSpider(CrawlSpider):
    name = 'reuters_article'
    handle_httpstatus_list = [401]
    
    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        "USER_AGENT": 'OOTL',
    }
    
    with open("/home/eshaan/Projects/OOtL/scraping/reuters_article_selector.json") as f:
        selectors = json.load(f)
        
    def start_requests(self):
        url = getattr(self, 'start_url', None)
        if url:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response, **kwargs):
        title = response.css(self.selectors["title"]).get()
        paragraphs = response.css(self.selectors["paragraphs"]).getall()
        text = " ".join([paragraph for paragraph in paragraphs])
        date = response.css(self.selectors["date"]).get()
        author = response.css(self.selectors["author"]).get()

        print({
            "title": title,
            "date": date,
            "author": author,
            "text": text,
        })

if __name__ == "__main__":
    process = CrawlerProcess()
    
    test_url = 'https://www.reuters.com/world/asia-pacific/india-races-build-power-plants-region-claimed-by-china-sources-say-2024-07-09/?n=@'

    process.crawl(ReutersArticleSpider, start_url=test_url)
    process.start()