# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

class SubjectsSpider(Spider):
    name = 'subjects'
    allowed_domains = ['class-central.com']
    start_urls = ['https://www.class-central.com/subjects']
    def __init__(self, subject=None):
        self.subject = subject
    
        
        
    def parse_subject(self, response):
        sub_name = response.xpath('//title/text()').extract_first().split(' | ')[0]
        courses = response.xpath('//*[@class="course-name"]')
        for course in courses:
            url = course.xpath('.//@href').extract_first()
            title = course.xpath('.//@title').extract_first()
            absolute_url = response.urljoin(url)
            
            yield {
                   'subjectName': sub_name,
                   'courseName': title,
                   'url': absolute_url
                   }
        next_page_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        yield Request(response.urljoin(next_page_url), callback=self.parse_subject)
    
    
    def parse(self, response):
        if self.subject:
            sub_url = response.xpath('//*[contains(@title, "'+self.subject+'")]/@href').extract_first()
            yield Request(response.urljoin(sub_url), callback=self.parse_subject)
        else:
            self.logger.info("Scrapping all subjects")
            subs_url = response.xpath('//*[@class="show-all-subjects view-all-courses"]/@href').extract()
            for url in subs_url:
                yield Request(response.urljoin(url), callback=self.parse_subject)
