# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from time import sleep
import random
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')



#定义一个taobao类
class taobao_infos:

    #对象初始化
    def __init__(self):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.url = url

        options = webdriver.ChromeOptions()
        #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10) #超时时长为10s


    #登录淘宝
    def login(self):

        # 打开网页
        self.browser.get(self.url)

        # 等待 密码登录选项 出现
        password_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login > div.login-content.nc-outer-box > div > div.login-blocks.login-switch-tab > a.password-login-tab-item')))
        password_login.click()

        # 等待 微博登录选项 出现
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()

        # 等待 微博账号 出现
        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        weibo_user.send_keys(weibo_username)

        # 等待 微博密码 出现
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        weibo_pwd.send_keys(weibo_password)

        # 等待 登录按钮 出现
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()

        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # 输出淘宝昵称
        print(taobao_name.text)

    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            # 根据i的值，模拟上下滑动
            if (i % 2 == 0):
                js = "var q=document.documentElement.scrollTop=" + str(300 + 400 * i)
            else:
                js = "var q=document.documentElement.scrollTop=" + str(200 * i)
            self.browser.execute_script(js)
            sleep(0.1)

        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(0.1)

        # 爬取淘宝 我已买到的宝贝商品数据

    def crawl_good_buy_data(self):

        # 对我已买到的宝贝商品数据进行爬虫
        self.browser.get("https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm")

        # 遍历所有页数
        for page in range(1, 2):

            # 等待该页面全部已买到的宝贝商品数据加载完毕
            good_total = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#tp-bought-root > div.js-order-container')))

            # 获取本页面源代码
            html = self.browser.page_source

            # pq模块解析网页源代码
            doc = pq(html)

            # # 存储该页已经买到的宝贝数据
            good_items = doc('#tp-bought-root .js-order-container').items()

            # 遍历该页的所有宝贝
            for item in good_items:
                good_time_and_id = item.find('.bought-wrapper-mod__head-info-cell___29cDO').text().replace('\n',
                                                                                                           "").replace(
                    '\r', "")
                good_merchant = item.find('.seller-mod__name___2d3js').text().replace('\n', "").replace('\r', "")
                good_name = item.find('.suborder-mod__production___3WebF'
                                      ' > div:nth-of-type(2) > p > a > span:nth-of-type(2)').text().replace('\n', "").replace('\r', "")
                ##tp-bought-root > div:nth-child(17) > div > table > tbody:nth-child(3) > tr > td:nth-child(1) > div > div:nth-child(2) > p:nth-child(1) > a:nth-child(1) > span:nth-child(2)
                # 只列出商品购买时间、订单号、商家名称、商品名称
                # 其余的请自己实践获取
                print(good_time_and_id, good_merchant, good_name)

            print('\n\n')

            # 大部分人被检测为机器人就是因为进一步模拟人工操作
            # 模拟人工向下浏览商品，即进行模拟下滑操作，防止被识别出是机器人
            # 随机滑动延时时间
            swipe_time = random.randint(1, 3)
            self.swipe_down(swipe_time)

            # 等待下一页按钮 出现
            good_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pagination-next')))
            # 点击下一页按钮
            good_total.click()
            sleep(2)


if __name__ == "__main__":
    weibo_username = "15023458863"  # 改成你的微博账号
    weibo_password = "********"  # 改成你的微博密码

    a = taobao_infos()
    a.login()  # 登录
    a.crawl_good_buy_data()  # 爬取淘宝 我已买到的宝贝商品数据