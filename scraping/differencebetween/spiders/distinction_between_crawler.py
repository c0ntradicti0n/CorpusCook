import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.parse
import os
import shutil
import logging
logging.getLogger().setLevel(logging.INFO)


output_dir = './data/'

class difference_between_crawler(CrawlSpider):
    def __init__(self):
        super().__init__()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            shutil.rmtree(output_dir)  # removes all the subdirectories!
            os.makedirs(output_dir)

    name = 'differencebetween'
    allowed_domains = ['www.differencebetween.net']
    start_urls = ['http://www.differencebetween.net']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        filedir = os.path.expanduser(output_dir)
        filename = urllib.parse.quote(response.url, '') + '.html'
        filepath = os.path.join(filedir, filename)

        if not os.path.exists(filepath):
            with open(filepath, 'wb') as f:
                f.write(response.body)
                logging.info('path: %s' % (filepath))

            #soup =  BeautifulSoup(response.body, features="lxml")

            #tabular_image_urls = soup.find_all('img', src=re.compile(".+cdn.+\.jpg$"))
            #for url in tabular_image_urls:
            #    url = url["src"]
            #    self.download_image(url)

    def download_image(self, tabular_image_url):
        if tabular_image_url:

            logging.info('image path: %s' % tabular_image_url)
            fname = os.path.basename(tabular_image_url)
            if not os.path.exists(fname):
                try:
                    urlopener = urllib.request.Request(tabular_image_url, headers={'User-Agent': 'Mozilla/5.0'})

                    with urllib.request.urlopen(urlopener) as response, open(output_dir + fname, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                except:
                    with open ('failedpictures.txt', 'a') as fp:
                        fp.write(tabular_image_url +'\n')
                    logging.info ('picture download failed! appending to the failure list.')


