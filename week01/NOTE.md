学习笔记

学习了使用bs4模块：
        bsinfo = bs(result.text, 'html.parser')
        for ddinfo in bsinfo.find_all('dd',):
            film_obj = Film()
            for tagname in ddinfo.find_all('p', attrs={'class':'name'}):
                for atag in tagname.find_all('a',):
                    film_obj.name = atag.get("title")
                    film_obj.url = "https://maoyan.com" + atag.get("href")
                    film_obj.type = sub_crawl(film_obj.url)
                    
学习了使用xml模块：
        selector = etree.HTML(response.text)
        for i in range(1, 11):
            item = MytestItem()
            film_name = selector.xpath('//*[@id="app"]/div/div/div/dl/dd[%d]/div/div/div[1]/p[1]/a/text()'%i)[0]
            film_url = selector.xpath('//*[@id="app"]/div/div/div/dl/dd[%d]/div/div/div[1]/p[1]/a/@href'%i)[0]
            film_url = "https://maoyan.com" + film_url
            item['name'] = film_name
            item['url'] = film_url
            
学习使用scrapy的模块分析html
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
