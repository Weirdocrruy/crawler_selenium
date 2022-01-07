# coding=gbk
from selenium import webdriver
import time


def get_content():
    shops = driver.find_elements_by_xpath("//div[@class='info']/p[@class='shopName']/span[1]")
    prices = driver.find_elements_by_xpath("//div[@class='info']/p/span/strong")
    for shop, price in zip(shops, prices):
        data = {
            'shop': shop.text,
            'price': str(price.text) + 'Ԫ'
        }
        print(data)


if __name__ == '__main__':
    #driver = webdriver.Chrome()
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=option)
    urls = [
        'https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=c3011824b1d47be13a4877b964632e28&keyword=python&page={}'.format(
            i)
        for i in range(5)]
    for url in urls:
        driver.get(url)

    get_content()
    time.sleep(3)
