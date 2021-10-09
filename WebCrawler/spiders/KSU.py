# August 2021 - Used with text_stats.py
# Web Crawler that starts at three kennesaw.edu urls and visits all other kennesaw.edu urls that are connected to these initial three by employing a breadth-first search using a queue. Settings, such as time between web page crawling, which algorithm to crawl web pages, and web crawl max count, are specified in the settings.py file. The website data is then parsed into a dictionary a stored in a JSON file that is statistically analyzed in the text_stats.py file.
import scrapy
import re
import string
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from WebCrawler.items import WebcrawlerItem
from bs4 import BeautifulSoup

class Spider(CrawlSpider):
    name = 'KSU'
    allowed_domains = ['kennesaw.edu']
    start_urls = [
        'http://kennesaw.edu/',
        'http://ccse.kennesaw.edu',
        'https://registrar.kennesaw.edu/'
    ]

    # only allow kennesaw.edu web addresses and use parse_items to store elements of web page
    rules = (
        Rule(LinkExtractor(allow_domains=('kennesaw.edu', )), callback='parse_items', follow=True),
    )
    
    def parse_items(self, response):
        entry = dict.fromkeys(['pageid', 'url', 'title', 'body', 'emails'])
        entry['pageid'] = str(hash(response.request.url))
        entry['url'] = response.request.url
        entry['title'] = response.xpath('//title/text()').get()
        soup = BeautifulSoup(str(response.text), 'html.parser')
        entry['body'] = soup.get_text().strip().replace('\n', ' ').replace('\xa0', ' ').replace('.', ' . ')
        entry['emails'] = re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', response.text, re.I)

        yield entry

