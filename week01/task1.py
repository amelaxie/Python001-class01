# -*- coding:utf-8 -*-
import requests
import json
from lxml import etree
from time import sleep
from sys import exit
from bs4 import BeautifulSoup as bs

# 电影类
class Film:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.url = ""
        self.release_time = ""

# http请求
def req_get(url):
    try_times = 3
    _header = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }
    while try_times > 0:
        try:
            result = requests.get(url, headers=_header)
            if result.text.find("<title>验证中心</title>") != -1:
                print("未验证，重试")
                continue
            else:
                return result
        except requests.exceptions as e:
            sleep(2)
            print(e)
        finally:
            try_times -= 1

# 爬虫-抓取电影类型
def sub_crawl(url):
    sub_result = req_get(url)
    # print (sub_result.text)
    sub_bsinfo = bs(sub_result.text, 'html.parser')
    #print (sub_bsinfo)
    type_list = []
    for divinfo in sub_bsinfo.find_all('div', attrs={'class': 'movie-brief-container'}):
        for liinfo in divinfo.find_all('a', attrs={'class': 'text-link'}):
            type_list.append(liinfo.get_text().strip())
    return " ".join(type_list)


if __name__ == "__main__":
    try:
        data_list = []
        result = req_get("https://maoyan.com/board")
        if result is None:
            print("获取页面失败")
            exit(1)
        bsinfo = bs(result.text, 'html.parser')

        # dd 标签中获取电影名称、详情页url、电影类型、上映时间
        for ddinfo in bsinfo.find_all('dd',):
            film_obj = Film()
            for tagname in ddinfo.find_all('p', attrs={'class': 'name'}):
                for atag in tagname.find_all('a',):
                    film_obj.name = atag.get("title")
                    film_obj.url = "https://maoyan.com" + atag.get("href")
                    film_obj.type = sub_crawl(film_obj.url)
            for tagtime in ddinfo.find_all('p', attrs={'class': 'releasetime'}):
                film_obj.release_time = tagtime.get_text().split("：")[-1]
            data_list.append(film_obj)
        
        # 结果输出至csv文件
        for data in data_list:
            print(data.name, data.url, data.type, data.release_time)
            output = f'|{data.name}|\t|{data.type}|\t|{data.release_time}|\n\n'
            with open("movies.csv", "a+", encoding="utf-8") as f:
                f.write(output)
    except Exception as e:
        print(e)
