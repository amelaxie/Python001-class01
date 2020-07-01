# -*- coding:utf-8 -*-
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


# 自动登录获取cookies
def autologin(username, passwd):
    browser = webdriver.Chrome()
    sleep(1)
    # 打开浏览器
    browser.get('https://shimo.im')
    sleep(2)

    # 点击登录，进入登录页面
    loginbutton = browser.find_element_by_xpath(
        '//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    loginbutton.click()
    sleep(2)

    # 在用户名、密码栏中输入相应的账号密码
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys(username)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys(passwd)
    sleep(1)

    # 点击登录按钮
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()

    # 获取cookie信息
    sleep(2)
    cookies = browser.get_cookies()

    # 关闭浏览器
    browser.close
    return cookies


# 调用获取个人信息接口
def get_userinfo(seleuium_cookies):
    try:
        # 将seleuium获得的cookies转换格式
        cookies = RequestsCookieJar()
        for cookie in seleuium_cookies:
            cookies.set(cookie['name'], cookie['value'])
        s = requests.session()
        s.verify = False
        # 设置相关头参数反反爬
        s.headers = {
            "referer": "https://shimo.im/profile",
            "accept": "application/vnd.shimo.v2+json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        _url = "https://shimo.im/lizard-api/users/me"
        rsp = s.get(_url, cookies=cookies)
        print(rsp.text)
    except Exception as e:
        print (e)


if __name__ == "__main__":
    username = "remotedesk@qq.com"
    passwd = "gktest999"
    cookies = (autologin(username, passwd))
    get_userinfo(cookies)
