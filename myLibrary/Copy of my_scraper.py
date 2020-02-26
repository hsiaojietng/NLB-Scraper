import scrapy
import requests
from myLibrary.items import myLibraryItem
from datetime import datetime
import re
import urllib.parse
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from scrapy.http import HtmlResponse
from scrapy import signals



class myLibrary(scrapy.Spider):
        name = "my_scraper"
        start_urls= ["https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/MSGTRN/WPAC/COMB"]

        def __init__(self):
                headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
                self.driver = webdriver.Chrome()
                
                
        def parse(self, response):
                self.driver.get(response.url)
                #English language value
                doc = self.driver.find_elements_by_xpath("//div[contains(@class, 'col-sm-8 col-md-7')]//select[contains(@name, 'CGS')]//option[contains(@value, 'E*English')]")[0]
                doc.click()
                #Pasir ris library
                doc = self.driver.find_elements_by_xpath("//div//select//option[contains(@value, '50641*Pasir Ris Public Library')]")[0]
                doc.click()
                #Adult Collection
                doc = self.driver.find_elements_by_xpath("//select//option[contains(@value, '001|002|046*Adult Lending')]")[0]
                doc.click()
                #Click on Search button
                doc = self.driver.find_elements_by_xpath("//button[contains(@id, 'submitButton')]")[0]
                doc.click()
                item = myLibraryItem()
                try:
                        myEle = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-body')))
                        item['bookTitle'] = self.driver.current_url #correct url
                except TimeoutException:
                        item['bookTitle'] = "Not the correct browser"
                '''if(self.driver.get(response.url) == "https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/MSGTRN/WPAC/COMB"):   
                        check = response.xpath("//div[contains(@class, 'card-body')]//h5//a[contains(@data-toggle, 'tooltip')]//span/descendant::text()")
                        item['bookTitle'] = check.extract()  
                else:
                        item['bookTitle'] = self.driver.current_url'''
                yield item
                self.driver.close()

                
