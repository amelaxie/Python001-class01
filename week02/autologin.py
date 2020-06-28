from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


def autologin(username, passwd):
    browser = webdriver.Chrome()
    sleep(1)
    # 打开浏览器
    browser.get('https://shimo.im')
    sleep(3)

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
    cookies = browser.get_cookies()
    sleep(5)
    
    # 关闭浏览器
    browser.close
    return cookies


if __name__ == "__main__":
    username = "remotedesk@qq.com"
    passwd = "gktest999"
    print(autologin(username, passwd))
