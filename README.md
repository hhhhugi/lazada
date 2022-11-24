www.lazada.co.id Item Review Crawler

This python based crawler collects comments from individual selling products on ecommerce website www.lazada.co.id
Change 'ItemNumber' in spider to any product number from lazada store and run:

scrapy crawl LazadaCrawler -o reviews.csv

I recommend to use Indonesian VPN to prevent bot detection and vendor blockage



First time Scrappy Installation steps:
(This project was built on Windows 10x environment)

1. Install python3 from following link.
https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe

2. Install Visual studio build tools 2022
https://aka.ms/vs/17/release/vs_BuildTools.exe

3. Define python path.
	- Go to Settings -> System -> About -> Advanced system settings -> Environment variables 
	- On the system variables mini window clock on Path and click edit button
	- Append python.exe path in the end. for example enter C:\Program Files (x86)\Python311-32

4. Install pip
	- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	- python get-pip.py
	
5. Install lxml library from http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml 
	- python -m pip install C:\path\to\downloaded\file\lxml-4.9.0-cp311-cp311-win32.whl
	
6. Install scrapy
	- python -m pip install scrapy
	if you can't run scrapy from cmd, make sure you defined scrapy path in windows environment paths like in step 3. for example append new path like C:\Users\hugi9\AppData\Roaming\Python\Python311-32\Scripts

7. Start new project
	- scrapy startproject lazadaCrawler

8. Generate spider
	- scrapy genspider lazadaspider www.lazada.co.id

9. Install scrapy-selenium. Some javascript framework websites need to rendered first for crawling.
	- pip install scrapy-selenium

10. Download preferred chromedriver from https://chromedriver.chromium.org/downloads and copy it in scrappy project directory.

11. Update Our Spiders To Use Scrapy Selenium
	- Add following code in settings.py
	
		from shutil import which
		  
		SELENIUM_DRIVER_NAME = 'chrome'
		SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
		SELENIUM_DRIVER_ARGUMENTS=['--headless']  
		DOWNLOADER_MIDDLEWARES = {
			 'scrapy_selenium.SeleniumMiddleware': 800
			 }

12. All Done!

	
