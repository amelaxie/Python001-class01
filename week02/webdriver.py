from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

browser = webdriver.Chrome()
sleep(1)
browser.get('https://maoyan.com/board')

sleep(4)
ybox = browser.find_element_by_xpath('//*[@id="yodaBox"]')
action = ActionChains(browser)
action.click_and_hold(ybox).perform()

#action.move_by_offset(10,0).perform()   #平行移动鼠标
#action.move_by_offset(10,0).perform()   #平行移动鼠标
#action.move_by_offset(30,0).perform()   #平行移动鼠标
for i in range(10):
    action.move_by_offset(20,0).perform()   #平行移动鼠标
    sleep(0.2)
    #action.move_by_offset(100,0).perform()   #平行移动鼠标


# for index in range(20):
#     try:
#         action.move_by_offset(10,0).perform()   #平行移动鼠标
#     except UnexpectedAlertPresentException:
#         break
#     sleep(0.1)
#     # action.move_by_offset(20,0).perform()   #平行移动鼠标
#     # action.reset_actions()
action.reset_actions()
sleep(0.1)    #等待停顿时间

sucess_text = browser.switch_to.alert.text
print(sucess_text)    #打印警告框提示
 
sleep(5)



