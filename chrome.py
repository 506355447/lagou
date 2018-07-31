from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

from config import *
import pymongo
client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)

#搜索
def search():
    print('正在搜索-------------------------->>>>')
    try:
        #爬取的网站url
        browser.get("https://www.taobao.com")
        # 获取搜索框
        input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#q')))
        # 获取搜索按钮
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        # 输入搜索内容
        input.send_keys(KEYWORD)
        # 点击搜索按钮
        submit.click()
        #获取总页数
        total=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutError:
        print('搜索出现异常：重新输入>>>>>>>>>>>>')
        return search()

#翻页
def next_pares(page_number):
    print('正在翻页-------------------------->>>>',page_number)
    try:
        # 获取页码框
        input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        # 获取页码按钮
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        #清空输入框
        input.clear()
        # 输入搜索内容
        input.send_keys(page_number)
        # 点击搜索按钮
        submit.click()
        #页数是否加载成功判断
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutError:
        print("翻页出现异常：重新进行翻页>>>>>>>>>>>>")
        next_pares(page_number)

def get_products():
    #判断页面是否加载完成
    wait .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html=browser.page_source
    #获取页面代码
    doc=pq(html)
    #获取提取数据
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        #数据格式化
        product={
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
            'title': item.find('.title').text(),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'img':item.find('.pic .img').attr('src')


        }
        print('获取完成-------------------------->>>>')
        #print(product)
        save_to_mongo(product)

#存储到MONGODB数据库中
def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功',result)
    except Exception:
        print('存储到MONGODB失败',result)

def main():
    try:
        total=int(search()[1:5])
        for i in range(2,total+1):
            next_pares(i)
    except Exception:
        print("出错了")
    finally:
        browser.close()#关闭浏览器程序

if __name__=='__main__':
    main()