import scrapy
import requests
from myLibrary.items import myLibraryItem
from datetime import datetime
import re
import urllib.parse
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
from scrapy.http import HtmlResponse
from scrapy import signals
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#For writing in excel
import requests
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest


class myLibrary(scrapy.Spider):                
        name = "my_scraper"
        start_urls = ["https://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/MSGTRN/WPAC/COMB"]
        count = 0

        '''def __init__(self):
                self.driver = webdriver.Chrome()'''

                
        def parse(self, response):
                
                nextClick = True
                number = 0
                while(nextClick):
                        time.sleep(30)
                                        
                        items = myLibraryItem()

                        #Getting genre for first page
                        items['genre'] = response.xpath("(//div//div[contains(@class, 'col pl-sm-0')]//span[contains(@class, 'd-block')]//span)[4]/text()").extract()
                                
                        #Getting booktitle
                        items['title'] = response.xpath("(//div//div[contains(@class, 'col pl-sm-0')]//span[contains(@class, 'd-block')]//span)[1]/text()").extract()
                                        
                        if(self.count == 0):
                                #Getting isbn for first page
                                items['isbn'] = response.xpath("(//div//div[contains(@class, 'col pl-sm-0')]//span[contains(@class, 'd-block')])[9]/text()").extract()
                                #Getting brn for first page
                                items['brn'] = response.xpath("(//div//div[contains(@class, 'col pl-sm-0')]//span[contains(@class, 'd-block')])[26]/text()").extract()
                        else:
                                #getting isbn for pages after 1st
                                items['isbn'] = response.xpath("(//div//div[contains(@class, 'col pl-sm-0')]//span[contains(@class, 'd-block')])[7]/text()").extract()
                                #getting brn for pages after 1st
                                items['brn'] = response.xpath("(//div//div[contains(@class, 'col pl-sm-0')]//span[contains(@class, 'd-block')])[19]/text()").extract()

                                                
                        #Getting author
                        items['author'] = response.xpath("(//div//div[contains(@class, 'col pl-sm-0')]//span[contains(@class, 'd-block')])[2]//span/text()").extract()

                        #Getting publisher
                        items['publisher'] = response.xpath("(//div//div[contains(@class, 'col pl-sm-0')]//span[contains(@class, 'd-block')])[3]/text()").extract()
                                        
                        yield items

                        #Writing data into file Works fine
                        filename = "C:\\Users\\Ng Hsiao Jiet\\Desktop\\myLibrary\\myLibrary\\bookTitle.csv"
                        fields = ["genre", "title", "isbn", "author", "publisher", "brn"]
                        with open(filename, "w") as f:
                                f.write("{}\n".format('\t'.join(str(field)for field in fields))) #write the header

                                for item in items:
                                        f.write("{}\n".format('\t'.join(str(items[field]) 
                                                for field in fields)))

                        if(self.count == 0):
                                next_page = response.xpath("(//ul[contains(@class, 'list-inline mb-0 d-flex justify-content-between')]//li//a/@href)[3]").extract()
                                self.count += 1
                        else:
                             next_page = response.xpath("(//a[starts-with(@href, '/cgi-bin/spydus.exe/')])[14]").extract_first()
                             self.count += 1
                             self.log("Page no: " + str(self.count))
                        if next_page is not None:
                                new_page = "https://catalogue.nlb.gov.sg" + next_page[0]
                                
                                yield SeleniumRequest(url= new_page, callback = self.parse)
                        else:
                                self.log("Scrapy did not load the next page")
                        if(self.count == 31605):
                                nextClick = false
                        else:
                                number += 1
                        
                        


                        

        


                
                      

