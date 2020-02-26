# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)


class MylibrarySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
        

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MylibraryDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        #request.meta["proxy"] = "http://139.180.129.160:8888"
        #request.headers["Proxy-Authorization"] = basic_auth_header("
        if request.url != 'https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/MSGTRN/WPAC/COMB':
            return None
        driver.get(request.url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id, 'submitButton')]")))
        #English language value
        doc = driver.find_elements_by_xpath("//option[contains(@value, 'ENG*English')]")[0]
        doc.click()
        #Pasir ris library
        doc = driver.find_elements_by_xpath("//option[contains(@value, '50641*Pasir Ris Public Library')]")[0]
        doc.click()
        #Adult Collection
        doc = driver.find_elements_by_xpath("//option[contains(@value, '001|002|046*Adult Lending')]")[0]
        doc.click()
        #Click on Book Material
        doc = driver.find_elements_by_xpath("//select[contains(@id, 'MTYP')]//option[contains(@value,'BOOK*Book')]")[0]
        doc.click()
        #Click on How many records
        doc = driver.find_elements_by_xpath("//div//select[contains(@id,'NRECS')]//option[contains(@value,'100')]")[0]
        doc.click()
        #Click on sorting fuction
        doc = driver.find_elements_by_xpath("(//div//select[contains(@id, 'SORTS')]//option)[2]")[0]
        doc.click()
        #Click on Search button
        doc = driver.find_elements_by_xpath("//button[contains(@id, 'submitButton')]")[0]

        driver.execute_script("arguments[0].click();", doc)

        WebDriverWait(driver, 20)
        #Click on first book
        Firstbook = driver.find_element_by_xpath("(//div[contains(@class, 'card card-grid')]//div//h5//a//span)[1]")
        Firstbook.click()


        #get response
        body = driver.page_source
            #HtmlResponse
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
