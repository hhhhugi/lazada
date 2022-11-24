import time
import hashlib
import re
from urllib import parse
import json
import sys
import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LazSpider(scrapy.Spider):
    
    # Scrapy configs
    name = 'LazadaCrawler'
    allowed_domains = ['my.lazada.co.id']
    
    # Scraper starting page
    page = 1
    
    # Lazada Store Mobile App Key
    LazadaStoreAppKey = 24677475
    
    # Product number
    ItemNumber = 6562360210
    
    # Selenium user agent and cookies
    User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    user_cookies_obj = {}
    user_cookies_str = ''
    
    def start_requests(self):
        
        # Selenium web - Chrome initialization
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument("--no-sandbox")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('w3c', True)
        browser = webdriver.Chrome(options=options)
        
        # Launch product review page on Chrome sandbox browser to prevent bot detection and vendor blockage
        browser.get(f'https://my-m.lazada.co.id/review/product-reviews?itemId={self.ItemNumber}')

        # Product review page params
        itemParams = {"itemId":f"{self.ItemNumber}","isHidden":0}
        
        # Get cookies from sandbox Chrome browser
        for i in range(len(browser.get_cookies())):
            self.user_cookies_str += browser.get_cookies()[i].get('name') + '=' + browser.get_cookies()[i].get('value') + ';'
            self.user_cookies_obj[browser.get_cookies()[i].get('name')] = browser.get_cookies()[i].get('value')

        # Lazada Store uses taobao backend which uses per cookie signs. 
        # To generate this sign, get token from previous response cookie and add params, time, appkey then md5hex convert.
        # Thanks to author of this post https://mp.weixin.qq.com/s?__biz=MzIwNjUxMTQyMA==&mid=2247484423&idx=1&sn=f33283ba799d0c48c65aef317a7966d1&chksm=9721c854a0564142664701b4602dc87927ae3e32fc7493afe7b911aca7a8744aa4d1b2cc3e23&token=205497283&lang=zh_CN#rd
        _m_h5_tk = re.findall(r"_m_h5_tk=([^;]*)", str(self.user_cookies_str))[0]
        t = str(int(time.time() * 1000))
        token = _m_h5_tk.split('_')[0]
        str_sign = '&'.join([token, t, f'{self.LazadaStoreAppKey}', str(json.dumps(itemParams,separators=(',', ':')))])
        sign = hashlib.md5(str_sign.encode('utf-8')).hexdigest()
        
        # Set header
        headers = {
            "Accept": 'application/json',
            "Origin": 'https://www.lazada.co.id',
            "User-Agent": self.User_Agent,
            "Content-type": 'application/x-www-form-urlencoded',
            "Cookie": self.user_cookies_str,
        }
        
        # Set Api parameters
        apiParams = {
            "jsv": "2.6.1",
            "appKey":f'{self.LazadaStoreAppKey}',
            "t":t,
            "sign":sign,
            "api":"mtop.lazada.review.item.getReviewList",
            "v":"1.0",
            "type":"originaljson",
            "isSec":1,
            "AntiCreep":True,
            "timeout":20000,
            "dataType":"json",
            "sessionOption":"AutoLoginOnly",
            "x-i18n-language":"id",
            "x-i18n-regionID":"ID",
            "data":str(json.dumps(itemParams,separators=(',', ':'))),
        }
        
        # Review Api Url
        url='https://acs-m.lazada.co.id/h5/mtop.lazada.review.item.getreviewlist/1.0/?' + parse.urlencode(apiParams)
        
        # Start Scraping
        yield scrapy.Request(url=url,
                              callback=self.parse,
                              headers=headers,
                              cookies=self.user_cookies_obj,
                              dont_filter=True
                              )
        
    def parse(self,response):
        print(f':::::::::::::::::::::::::::::::: PAGE # {self.page} ::::::::::::::::::::::::::::::::')
         
        # Api response outpit
        apiResponse = json.loads(response.body)
        try:
            for item in apiResponse.get('data').get('items'):
                yield {
                'content' : item.get('reviewContent'),
                'star' : item.get('rating'),
                'date' : item.get('reviewTime'),
                'title' : item.get('itemTitle'),
                }
        except TypeError:
            print("NO PAGES LEFT")
            sys.exit(0)
        except AttributeError:
            print(f"VENDOR REFUSED PAGE SCRAPPING #{self.page}")

        # Review page params
        itemParams = {"itemId":f"{self.ItemNumber}","filter":0,"sort":0,"isHidden":0,"pageNo":self.page,"pageSize":10}
        
        # Sign generation
        _m_h5_tk = re.findall(r"_m_h5_tk=([^;]*)", str(self.user_cookies_str))[0]
        t = str(int(time.time() * 1000))
        token = _m_h5_tk.split('_')[0]
        str_sign = '&'.join([token, t, f'{self.LazadaStoreAppKey}', str(json.dumps(itemParams,separators=(',', ':')))])
        sign = hashlib.md5(str_sign.encode('utf-8')).hexdigest()
        
        # Api params
        apiParams = {
            "jsv": "2.6.1",
            "appKey":f'{self.LazadaStoreAppKey}',
            "t":t,
            "sign":sign,
            "api":"mtop.lazada.review.item.getReviewList",
            "v":"1.0",
            "type":"originaljson",
            "isSec":1,
            "AntiCreep":True,
            "timeout":20000,
            "dataType":"json",
            "sessionOption":"AutoLoginOnly",
            "x-i18n-language":"id",
            "x-i18n-regionID":"ID",
            "data":str(json.dumps(itemParams,separators=(',', ':'))),
        }
        
        # Headers
        headers = {
            "Accept": 'application/json',
            "Origin": 'https://www.lazada.co.id',
            "User-Agent": self.User_Agent,
            "Content-type": 'application/x-www-form-urlencoded',
            "Cookie": self.user_cookies_str,
        }
        
        # Increase page number for next scrap
        self.page = self.page + 1
        url='https://acs-m.lazada.co.id/h5/mtop.lazada.review.item.getreviewlist/1.0/?' + parse.urlencode(apiParams)
        yield scrapy.Request(url=url,
                              callback=self.parse, # Loop page after page scrapping.
                              headers=headers,
                              cookies=self.user_cookies_obj,
                              dont_filter=True
                              )