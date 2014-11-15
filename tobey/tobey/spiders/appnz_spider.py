#-*- coding=utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log as LOG

from tobey.items import AppItem


class AppnzSpider(BaseSpider):
    name = "appnz"
    allowed_domains = ["appnz.com"]
    start_urls = [
        'http://www.appnz.com/',
    ]

    def parse(self, response):
        LOG.msg('[AppnzSpider] parse response url: %s' % response.url)
        sel = HtmlXPathSelector(response)
        sites = sel.select('//article[@id="post-home"]'
                           '//h3[@class="classic-list-title"]')
        for site in sites:
            item = AppItem()
            title = site.select('a/text()').extract()[0]
            link = site.select('a/@href').extract()[0]
            item['title'] = title
            item['link'] = link
            yield Request(url=link, meta={'item': item}, callback=self.parse_detail)

        pagination = sel.select('//nav[@id="nav-below"]//div[1]//a')
        for p in pagination:
            link = p.select('@href').extract()[0]
            yield Request(url=link, meta={}, callback=self.parse)

    def parse_detail(self, response):
        sel = HtmlXPathSelector(response)
        item = response.meta['item']
        LOG.msg('[AppnzSpider] parse detail url: %s' % item['link'])
        content = sel.select('//div[@class="post-body clearfix"]'
                             '//p[not(ancestor::div[@style="display:none;"])]').extract()
        publish_date = sel.select("//header[@class='single-header clearfix']"
                                  "//div[@class='light-post-meta']"
                                  "/span[@class='con_1']/a/text()").extract()[0]
        publish_time = sel.select("//header[@class='single-header clearfix']"
                                  "//div[@class='light-post-meta']"
                                  "/span[@class='con_1']/a/@title").extract()[0]
        category = sel.select("//div[@class='post-details-right']"
                              "/h1[@class='single-title']//img/@src").extract()
        tag_list = sel.select("//div[@class='post-tags']//a/text()").extract()
        thumbnail_src = sel.select("//section[@id='articles']/article/div[@class='post-body clearfix']/img/@src").extract()[0]

        category_list = [category_img[category_img.rindex('/')+1:
                        category_img.rindex('.')]  for category_img in category
                        if category_img.endswith('.png')]
        item['content'] = ''.join(content)
        item['publish_date'] = "%(date)s %(time)s" % \
                {"date": publish_date, "time": publish_time}
        item['category'] = category_list
        item['tag'] = tag_list
        item['thumbnail_src'] = thumbnail_src
        return item
