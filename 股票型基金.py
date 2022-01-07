# coding=gbk
from selenium import webdriver
import csv
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
driver = webdriver.Chrome()
driver.get('https://www.howbuy.com/fund/manager/')

urls = driver.find_element_by_css_selector('body > div.wraper.main > div.chart-box > div.chart-list.result_list > table > tbody > tr:nth-child(1) > td:nth-child(3) > a').text
print(urls)