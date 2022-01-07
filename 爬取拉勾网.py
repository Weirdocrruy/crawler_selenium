# coding=gbk
import re
import time
import  pymongo
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
import csv
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


# client = pymongo.MongoClient('localhost', 27017)
# mydb = client['mydb']
# lagouwang = mydb['拉勾网']
fp = open(r'C:\Users\Lenovo-PC\Desktop\拉勾网.csv', 'wt', newline='',encoding='utf-8-sig')
writer = csv.writer(fp)
writer.writerow(('name', 'company_name','salary','city','work_years','education','desc'))
class lagouSpider(object):
    driver_path = r'E:\Users\Lenovo-PC\PycharmProjects\untitled2\chromedriver.exe'

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=lagouSpider.driver_path)
        self.url = 'https://www.lagou.com/jobs/list_%E5%B8%82%E5%9C%BA%E8%90%A5%E9%94%80/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='#https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=
        self.positions = []

    def run(self):
        self.driver.get(self.url)
        while True: #死循环
            source = self.driver.page_source
            WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='pager_container']/span[last()]")))
            self.pares_list_page(source)
            try:
                next_btn=self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
                if "pager_next pager_next_disabled" in next_btn.get_attribute("class"):
                    break
                else:
                    self.driver.execute_script("arguments[0].click();", next_btn)
            except:
                print(source)
            time.sleep(1)
    def pares_list_page(self, source):
        html = etree.HTML(source)
        links = html.xpath("//a[@class='position_link']/@href")
        for link in links:
            self.requests_detail_page(link)
            time.sleep(1)

    def requests_detail_page(self, url):
        #self.driver.get(url)
        # 切换页面
        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='name']")))
        source = self.driver.page_source
        self.parse_detail_page(source)
        #关闭详情页
        self.driver.close()
        #继续切换到职位列表业
        self.driver.switch_to.window(self.driver.window_handles[0])

    def parse_detail_page(self, source):
        html = etree.HTML(source)
        position_name=html.xpath("//span[@class='name']/text()")[0]
        job_request_spans = html.xpath("//dd[@class='job_request']//span")
        salary = job_request_spans[0].xpath('.//text()')[0].strip()
        city = job_request_spans[1].xpath('.//text()')[0].strip()
        city = re.sub(r"[\s/]", '', city)
        work_years = job_request_spans[2].xpath('.//text()')[0].strip()
        work_years = re.sub(r"[\s/]", '', work_years)
        education = job_request_spans[3].xpath('.//text()')[0].strip()
        education = re.sub(r"[\s/]", '', education)
        desc = ''.join(html.xpath("//dd[@class='job_bt']//text()")).strip()
        company_name=html.xpath("//h4[@class='company']/text()")[0].strip()
        position = {
            'name': position_name,
            'company_name':company_name,
            'salary': salary,
            'city': city,
            'work_years': work_years,
            'education': education,
            'desc': desc
        }
        self.positions.append(position)
        #lagouwang.insert_one(position)
        print(position)
        name=position['name']
        company_name=position['company_name']
        salary=position['salary']
        city=position['city']
        work_years=position['work_years']
        education=position['education']
        desc=position['desc']

        writer.writerow((name, company_name, salary,city,work_years,education,desc))

if __name__ == '__main__':
    spider = lagouSpider()
    spider.run()
