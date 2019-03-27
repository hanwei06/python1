# -*- coding: utf-8 -*-
import scrapy
import pytz
from dzw.items import DzwItem
import datetime


class DzwwwSpider(scrapy.Spider):
    name = 'zzzk'
    allowed_domains = ['gongkong.com']
    start_urls = ['http://www.gongkong.com/Manufacturing/Policy']

    def __init__(self, page=1, *args, **kwargs):
        super(DzwwwSpider, self).__init__(*args, **kwargs)

        self.page = page
        self.tz = pytz.timezone('Asia/Shanghai')

    def start_requests(self):

            url = "http://www.gongkong.com/Manufacturing/Policy"
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse,meta={'i':0})

    #  列表页
    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        i = response.meta['i']
        count = 0
        results = response.xpath('//ul[@class="secpageul"]/li')
        pageSize = int(response.xpath('//span[@class="gk_page_label"]').xpath('string(.)').extract_first().split('/')[1].split('页')[0])

        #  循环获取列表页的每条信息
        for res in results:
            title = res.xpath('./a').xpath('string(.)').extract_first()
            url = 'http://www.gongkong.com'+str(res.xpath('./a/@href').extract_first())
            time = res.xpath('./span[@class="spanr"]')[0].xpath('string(.)').extract_first()
            count = count+1
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_one,
                                 meta={'title': title, 'url': url, 'time': time})

        # 判断页面中符合条件的新闻数量
        # if count == 20:
            # 判断是否包含“下一页”标签
            # for np in nextpage:
            #     pn = np.xpath('string(.)').extract_first()
        if i < pageSize:
            i=i+1
            u_1 = 'http://www.gongkong.com/Manufacturing/Policy?pageindex='
            u_2 = '&institutions=0&time='
            u = u_1+str(i+1)+u_2
            yield scrapy.Request(url=u, dont_filter=True, callback=self.parse,meta={'i':i})

    # 对具体页面进行爬取
    def parse_one(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        url = response.meta['url']
        title = response.meta['title'].strip('r').strip('\n')
        time = response.meta['time']
        content = response.xpath('.//div[@class="content"]').xpath('string(.)').extract_first().strip('rn')

        item = DzwItem()
        item['title'] = title
        item['time'] = time
        item['content'] = content
        item['url'] = url
        item['source'] = '智造智库-产业政策'
        yield item
