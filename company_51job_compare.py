# -*- coding: utf-8 -*-
import scrapy
from recruit_51job.items import Recruit51JobItem
import datetime


class CompanyLpSpider(scrapy.Spider):
    name = 'company_51job_compare'
    # allowed_domains = ['search.51job.com']
    starturl = 'https://search.51job.com'

    def start_requests(self):
        #读取company_name中公司的名称
        f = open('../company_name.txt', 'r', encoding='utf-8-sig')
        f1 = open('jobPlaces.txt', 'r', encoding='utf-8-sig')
        words = f.readlines()
        places = f1.readlines()
        #遍历读取到的公司的名称
        for place in places:
            place = place.strip('\n')
            for word in words:
                word = word.strip('\n')
                url = 'https://search.51job.com/list/'+str(place)+',000000,0100%252C2500%252C2600%252C2700%252C2800,01%252C38%252C32%252C31%252C40,0,99,'+str(word)+',1,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
                yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        #职位列表的获取对应职位的url集合
        zwListDivs = response.xpath('//div[@class="dw_table"]/div[@class="el"]')
        for zwDiv in zwListDivs:
            zwUrl = zwDiv.xpath('p/span/a/@href').extract_first()
            time = zwDiv.xpath('span[@class="t5"]').xpath('text()').extract_first()
            if str(time) == '12-31':
                year = datetime.datetime.today().year - 1
                fbDate = str(year) + '-' + str(time)
            else:
                year = datetime.datetime.today().year
                fbDate = str(year) + '-' + str(time)
            yesterdayComapre = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
            if  datetime.datetime.strptime(fbDate,'%Y-%m-%d') == datetime.datetime.strptime(yesterdayComapre, '%Y-%m-%d'):
                yield scrapy.Request(url=zwUrl, callback=self.parse_company_item, meta={'fbDate': fbDate})

        #下一页连接获取
        urls = response.xpath('//div[@class="p_in"]/ul/li[@class="bk"]/a')
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for urlNext in urls:
            # print(urlNext.xpath('text()').extract_first())
            # print(urlNext.xpath('@href').extract_first())
            # from scrapy.shell import inspect_response
            # inspect_response(response, self)
            if urlNext.xpath('text()').extract_first()=='下一页':
                #获取下一页的url
                nexturl = urlNext.xpath('@href')
                if nexturl.extract() is not None:
                    url = nexturl.extract_first()
                    # print(url)
                    # from scrapy.shell import inspect_response
                    # inspect_response(response, self)
                    yield scrapy.Request(url=url,callback=self.parse)

    def parse_company_item(self,response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        recruit51JobItem = Recruit51JobItem()
        jobName = response.xpath('//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]/h1').xpath(
            'text()').extract_first()
        recruit51JobItem['jobName'] = str(jobName).strip()
        jobSalary = response.xpath('//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]/strong').xpath(
            'text()').extract_first()
        recruit51JobItem['jobSalary'] = jobSalary
        if str(jobSalary).find('-') != -1:
            a = jobSalary[str(jobSalary).find('/') - 1:str(jobSalary).find('/')]
            recruit51JobItem['minSalary'] = str(jobSalary).split('-')[0] + a
            recruit51JobItem['maxSalary'] = str(jobSalary).split('-')[1].split('/')[0]
        else:
            recruit51JobItem['minSalary'] = ''
            recruit51JobItem['maxSalary'] = ''
        companyName = response.xpath(
            '//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]/p[@class="cname"]/a[@class="catn"]').xpath(
            'text()').extract_first()
        recruit51JobItem['companyName'] = str(companyName).strip()
        resultList = response.xpath('//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]/p[@class="msg ltype"]').xpath(
            'string(.)').extract_first().split('发布')[0].split('|')
        jobPosition = response.xpath(
            '//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]/p[@class="msg ltype"]').xpath(
            'text()').extract_first()
        recruit51JobItem['jobPosition'] = str(jobPosition).strip()
        for i in range(len(resultList)):
            if resultList[i].find('经验') != -1:
                recruit51JobItem['jobExperience'] = str(resultList[i]).strip()
            elif resultList[i].find('招') != -1 and resultList[i].find('人') != -1:
                recruit51JobItem['jobNeedNum'] = resultList[i].split('招')[1].split('人')[0]
            elif resultList[i].find('专科') != -1 or resultList[i].find('大专') != -1 or resultList[i].find('本科') != -1 or \
                    resultList[i].find('硕士') != -1 or resultList[i].find('博士') != -1:
                recruit51JobItem['jobEducation'] = str(resultList[i]).strip()

        recruit51JobItem['jobDetail'] = response.xpath('//div[@class="tCompany_main"]/div[1]').xpath('string(.)').extract_first()
        recruit51JobItem['companyInfo'] = response.xpath('//div[@class="tCompany_main"]/div[3]').xpath('string(.)').extract_first()
        recruit51JobItem['link'] = response.url
        recruit51JobItem['industry'] = response.xpath('//div[@class="com_tag"]/p[3]/@title').extract_first()
        recruit51JobItem['companyNature'] = response.xpath('//div[@class="com_tag"]/p[1]/@title').extract_first()
        recruit51JobItem['companyScale'] = response.xpath('//div[@class="com_tag"]/p[2]/@title').extract_first()
        recruit51JobItem['companyLink'] = response.xpath('//div[@class="com_msg"]/a/@href').extract_first()
        recruit51JobItem['companyPosition'] = response.xpath('//div[@class="tCompany_main"]/div[2]/div[@class="bmsg inbox"]/p').xpath('string(.)').extract_first()
        if response.xpath('//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]/div[@class="jtag"]/div[@class="t1"]') is not None:
            recruit51JobItem['welfare'] = response.xpath('//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]/div[@class="jtag"]/div[@class="t1"]').xpath('string(.)').extract_first()
        else:
            recruit51JobItem['welfare'] = ''
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if response.meta['fbDate'] is not None:
            recruit51JobItem['fbDate'] = response.meta['fbDate']
        else:
            recruit51JobItem['fbDate'] = now
        # recruit51JobItem['fbDate'] = now
        recruit51JobItem['pqDate'] = now
        recruit51JobItem['source'] = '51job'
        yield recruit51JobItem