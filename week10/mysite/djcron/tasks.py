from mysite.celery import app
import sys
import subprocess

sys.path.append('F:\\Python学习\\Python001-class01\\week10\\Analyse\\')
from analyse_baidu import data_analyse


# 爬虫定时任务
@app.task()
def smzdm_phone_crawl():
    subprocess.Popen("F:\\Python学习\\smzdm_crawl.bat")
    return 'crawl task'


# 数据分析定时任务
@app.task()
def smzdm_phone_analyse():
    data_analyse()
    return 'crawl task'
