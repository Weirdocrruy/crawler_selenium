# coding=gbk
from selenium import webdriver

# 隐藏打开网页
option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(chrome_options=option)
# driver = webdriver.Chrome()
driver.get('http://fanyi.youdao.com/')
driver.maximize_window()


def translation(words):
    driver.find_element_by_id('inputOriginal').send_keys(words)
    driver.find_element_by_class_name('fanyi__operations--machine').click()
    data = driver.find_element_by_xpath("//div[@class='dict__relative']").text
    print(data)


if __name__ == '__main__':
    words = input('请输入：')
    translation(words)
