# coding=gbk
from selenium import webdriver
import csv
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
fp = open(r'C:\Users\Lenovo-PC\Desktop\京东.csv', 'wt', newline='', encoding='utf-8-sig')
writer = csv.writer(fp)
writer.writerow(('name', 'price', 'deal', 'title'))


def get_product(keyword):
    driver.find_element_by_css_selector('#key').send_keys(keyword)
    driver.find_element_by_css_selector('#search > div > div.form > button').click()
    driver.implicitly_wait(10)
    driver.maximize_window()


def drop_down():
    for x in range(1, 11, 2):
        j = x / 10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)


def parse_data():
    lis = driver.find_elements_by_css_selector('.gl-item')

    for li in lis:
        try:
            name = li.find_element_by_css_selector('div.p-name a em').text
            price = li.find_element_by_css_selector('div.p-price strong i').text
            deal = li.find_element_by_css_selector('div.p-commit strong a').text
            title = li.find_element_by_css_selector('span.J_im_icon a').text
            print(name, price, deal, title)

            writer.writerow((name, price, deal, title))
        except Exception as e:
            pass


def get_next():
    driver.find_element_by_class_name('pn-next').click()


word = input('请输入你要搜索的商品：')
driver = webdriver.Chrome()
driver.get('https://www.jd.com/')
get_product(word)

for page in range(1, 5):
    drop_down()
    parse_data()
    get_next()
