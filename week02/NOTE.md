学习笔记


# 本周学习了如何使用数据库存储scaray抓取的信息
	我使用了sqlalchemy组件保存数据致mysql
#	简单的验证码识别
# 使用WebDriver 模拟用户登录，比如
  loginbutton = browser.find_element_by_xpath(
        '//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
  loginbutton.click()
	browser.find_element_by_xpath('div/input').send_keys(username)
	browser.find_element_by_xpath('div/input').send_keys(passwd)
	browser.find_element_by_xpath('div[1]/button').click()
	
# 学习自己编写下载中间件，下载中间件的优先级，值低的优先级高先处理，优先级低的数值高后处理

# 使用redis集群搭建分布式爬虫