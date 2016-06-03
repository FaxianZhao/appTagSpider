#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy.spiders import Spider
from bs4 import BeautifulSoup
from scrapy.http import Request
from appSpider.items import AppspiderItem

class mySpider(Spider):
    name = "appspider"
    allowed_domains = ["zhushou.360.cn"]
    start_urls = []


    game_type = 2
    app_type = 1

    index = 0

    for i in xrange(1,51,1):
        start_urls.append("http://zhushou.360.cn/list/index/cid/%d?page=%d" % (app_type, i))

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        for link in soup.find("ul",{"id":"iconList"}).findAll("h3"):
            url = response.urljoin(link.a.get('href'))
            yield Request(url, self.parse_app)

    def parse_app(self, response):
        item = AppspiderItem()
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        details = soup.find("body",{"class":"index"}).find_previous_sibling("script").get_text().encode('utf-8')
        infos = details[details.find("'") : details.rfind("'")+1].replace('\r\n','').split(',')
        item['name'] = infos[1].split(':')[1].strip().replace("'",'')
        item['pkg'] = infos[5].split(':')[1].strip().replace('"','')
        tags = set()
        try:
            for tag in soup.find("div", {"class", "app-tags"}).findAll("a"):
                tags.add(tag.get_text().encode('utf-8'))
        except AttributeError as e:
            self.logger.info('There is no app-tags: %s' % e)
        item['tags'] = tags
        return item
