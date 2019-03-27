# -*- coding: utf-8 -*-
import scrapy

from recruit_51job.items import Recruit51JobItem


class CompanyLpSpider(scrapy.Spider):
    name = 'robot'
    def start_requests(self):
        url = 'http://www.robot-china.com/exhibit/search-htm-year-2019-catid-32.html'
        yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):

        uls = response.xpath('//div[@class="xieceinfolbao"]/dl[@class="xieceinfoldl"]/dd/div[@class="xieceinfosp"]/b/a/@href').extract()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        if uls is not None:
            for ul in uls:
                # print(ul)
                # from scrapy.shell import inspect_response
                # inspect_response(response, self)
                yield scrapy.Request(url=str(ul),callback=self.nextParse,meta={'ul':ul})
        nextUrl = str(response.xpath('//div[@class="xieceinfolbao"]/div[@class="pages"]/a[@class="next"]/@href').extract_first())
        if nextUrl.find('page-1.html') != 1:
            nextUrl = 'http://www.robot-china.com' + nextUrl
            yield scrapy.Request(url=nextUrl, callback=self.parse)
    def nextParse(self,response):
        url = response.meta['ul']
        title = response.xpath('//div[@class="xieceinfodmp"]/span[@class="xieceinfodmpt"]').xpath('string(.)').extract_first()
        time = response.xpath('//div[@class="xieceinfodm"]/ul/li')[0].xpath('string(.)').extract_first().split('：')[1]
        content = response.xpath('//div[@id="content"]').xpath('string(.)').extract_first()
        robot = Recruit51JobItem()
        robot['link'] = url
        robot['title'] = title
        robot['fbDate'] = time
        robot['content'] = content
        robot['source'] = '中国机器人网'
        yield robot