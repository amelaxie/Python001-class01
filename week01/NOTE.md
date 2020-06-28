学习笔记

pip 加速
pip install sqlalchemy -i https://pypi.douban.com/simple/ 

使用bs4模块：
# beautifulsoup 默认解析方式html.parser 搜索p标签 class属性为name的html代码，获得标签内属性使用get方法
from bs import beautifulsoup as 	bs
bsinfo = bs(result.text, 'html.parser')
for ddinfo in bsinfo.find_all('dd',):
    film_obj = Film()
    for tagname in ddinfo.find_all('p', attrs={'class':'name'}):
        for atag in tagname.find_all('a',):
            film_obj.name = atag.get("title")
	            film_obj.url = "https://maoyan.com" + atag.get("href")
            film_obj.type = sub_crawl(film_obj.url)
                    
使用xml模块：
# lxml使用xpath搜索到相应的html代码，使用text()获取标签内的内容
import lxml.etree 				
selector = etree.HTML(response.text)
for i in range(1, 11):
    item = MytestItem()
    film_name = selector.xpath('//*[@id="app"]/div/div/div/dl/dd[%d]/div/div/div[1]/p[1]/a/text()'%i)[0]
    film_url = selector.xpath('//*[@id="app"]/div/div/div/dl/dd[%d]/div/div/div[1]/p[1]/a/@href'%i)[0]
    film_url = "https://maoyan.com" + film_url
    item['name'] = film_name
    item['url'] = film_url
    
# 使用pandas模块输出csv文件,输出index序号（从0开始），输出header表头
import pandas as pd
mylist = [file_name, plan_date, rating]
movie1 = pd.Dataframe(data = mylist)
movie1.to_csv('./movie.csv', encoding='utf-8', index=False, header=False)

# 初始化一个元组，推导式 生成包含所有页面的元组
numlist = tuple(i for i in range(0,10))
urls = tuple(f'https://movie.douban.com/top250?start={ page * 25 }&filter=' for page in range(10))

# dir(math) 查看模块中的相关方法，  help(math) 查看模块使用方法

# html标签，文字内容一般放在span标签内，链接一边是a标签，图片一般是img标签

# scrapy核心组件：引擎Enginne、调度器Scheduler、下载器Downloader、
爬虫Spider、项目管道Item Pipelines、下载器中间件Downloader Middlewares、爬虫中间件Spider Middlewares
scrapy创建项目：scrapy startproject myspiders
scrapy创建一个爬虫：scrapy genspider movies
allowd_domains 限制爬虫域名范围
start_urls 启动后第一次发起的http请求

# 使用scrapy的模块分析html
from scrapy.selector import Selector
movies = Selector(response=response).xpath('//dd')
for movie in movies:
    print ("-----------------------------------")
    item = MytestItem()
    name = movie.xpath('./a/@title').extract_first().strip()
    url = "https://maoyan.com" + movie.xpath('./a/@href').extract_first().strip()
    releasetime = movies.xpath('./div/div/div[1]/p[3]/text()').extract_first().strip()
    item['name'] = name
    item['url'] = url
    item['releasetime'] = releasetime.split("：")[-1]
    print(name,url)
    yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse2)
    
    
# get() 、getall() 是新版本的方法，extract() 、extract_first()是旧版本的方法。
# 前者更好用，取不到就返回None，后者取不到就raise一个错误。
# 对于scrapy.selector.unified.SelectorList对象，getall()==extract(),get()==extract_first()
# 对于scrapy.selector.unified.Selector对象，getall()==extract(),get()!=extract_first()
            
scrapy相关设置：
settings.py      
# ua设置
USER_AGENT
      
# pipeline设置项开启：
ITEM_PIPELINES = {
    'mytest.pipelines.MytestPipeline': 300,
}

# 下载延时
DOWNLOAD_DELAY = 1
