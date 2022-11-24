from shutil import which

BOT_NAME = 'laz'
SPIDER_MODULES = ['lazada.spiders']
NEWSPIDER_MODULE = 'lazada.spiders'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 20
COOKIES_ENABLED = True
AUTOTHROTTLE_ENABLED = True
HTTPCACHE_ENABLED = True
FEED_EXPORT_ENCODER = 'utf-8'
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('./chromedriver.exe')
SELENIUM_DRIVER_ARGUMENTS=['--headless']  
DOWNLOADER_MIDDLEWARES = {
        'scrapy_selenium.SeleniumMiddleware': 800
        }