# -*- coding:utf-8 -*-
# 数据清洗、情感分析
import pandas as pd
from snownlp import SnowNLP
from sqlalchemy import create_engine
import datetime, time
import pymysql
import re
import emoji
from aip import AipNlp
from config import APP_ID, API_KEY, SECRET_KEY
import urllib.request
import os

""" Baidu NLP APPID AK SK """

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

engine = create_engine('mysql+pymysql://spider:mydb999@localhost:3306/spider?charset=utf8mb4')


# 下载商品图片
def download_img(img_url):
    base_dir = 'F:\\Python学习\\Python001-class01\\week10\\mysite\\static\\img'
    dir_list = img_url.split("/")[3:-1]
    dir_name = base_dir
    for subdir in dir_list:
        dir_name = dir_name + os.sep + subdir
    img_name = img_url.split("/")[-1]
    filename = dir_name + os.sep + img_name
    if os.path.exists(filename):
        return True
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    domain = img_url.split("/")[2]
    header = {
        "host": domain, "referer": "www.smzdm.com",
        "user-agent": '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'''
    }
    try_times = 0
    while try_times <= 3:
        try:
            request = urllib.request.Request(img_url, headers=header)
            response = urllib.request.urlopen(request)

            if (response.getcode() == 200):
                with open(filename, "wb") as f:
                    f.write(response.read())  # 将内容写入图片
                    return True
        except Exception as e:
            print(str(e))
            try_times += 1
            time.sleep(0.3)
    return False


# 查询单个商品情感分析信息
def sentiment_summary(goods_id):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='spider', password='mydb999', database='spider',
                               charset='utf8mb4')
        sql = f"select sentiment,count(sentiment) as count from  t_comment_processed t where t.goods_id={goods_id} GROUP BY sentiment"
        cursor = conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        if res:
            return res
    except Exception as e:
        print(e)
        return None


# 百度情感分析
def baidu_nlp(text):
    trytimes = 3
    while trytimes > 0:
        try:
            sinfo = client.sentimentClassify(text)['items'][0]
            sentiment_list = [sinfo['positive_prob'], sinfo['negative_prob'],
                              sinfo['confidence'], sinfo['sentiment']]
            return sentiment_list
        except Exception as e:
            print(e)
            time.sleep(0.5)
            trytimes -= 1


# snownlp情感分析
def snow_nlp(text):
    s = SnowNLP(text)
    positive = s.sentiments
    if positive > 0.65:
        sentiment = 2
    elif positive < 0.35:
        sentiment = 0
    else:
        sentiment = 1
    sentiment_list = [0.0, 0.0, 0.0, sentiment]
    return sentiment_list


# 检查是否已经分析过
def is_nlp(comment_id):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='spider', password='mydb999', database='spider',
                               charset='utf8mb4')
        sql = f"""select * from t_comment_processed WHERE comment_id={comment_id} and sentiment is null """
        cursor = conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res
    except Exception as e:
        print(e)


# 更新商品情感分析信息
def update_goods(goods_id, comment_num, positive, neutral, negative):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='spider', password='mydb999', database='spider',
                               charset='utf8mb4')
        sql = f"""update t_goods_processed  
            set comment_num={comment_num}, positive={positive}, 
            neutral={neutral}, negative={negative} 
            WHERE goods_id={goods_id}"""
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)


# 查询未清洗和分析的新数据
def get_new_crawl_data(interval):
    dt = datetime.datetime.now() - datetime.timedelta(hours=interval) - datetime.timedelta(minutes=5)
    start_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    # 查询语句，获取商品信息和评论信息
    sql_comments = f''' select * from t_comment
      where update_time >='{start_time}' 
      and comment_id not in (select comment_id from t_comment_processed)'''
    # read_sql_query的两个参数: sql语句， 数据库连接
    # sql_goods = f''' select * from t_goods
    # where update_time >='{start_time}'
    # and goods_id not in (select goods_id from t_goods_processed)'''
    sql_goods = f''' select * from t_goods 
    where update_time >='{start_time}' and goods_id not in (select goods_id from t_goods_processed)'''

    df_goods = pd.read_sql_query(sql_goods, engine)
    df_comments = pd.read_sql_query(sql_comments, engine)
    df_g = df_goods.dropna()
    df_c = df_comments.dropna()
    return df_g, df_c


# 情感分析数据
def process_data(df_goods, df_comment):
    comment_data_list = []
    n = 0
    if len(df_comment) > 0:
        for index, c_row in df_comment.iterrows():
            if is_nlp(c_row['comment_id']) is not None:
                print(c_row['comment_id'], "已有评论")
                continue
            text = c_row['text']
            text = emoji.demojize(text)
            sentiment_list = baidu_nlp(text)
            if not sentiment_list:
                sentiment_list = snow_nlp(text)
            c_row_processed = list(c_row) + sentiment_list
            comment_data_list.append(c_row_processed)
            print(c_row_processed)
            time.sleep(0.3)

        df_comment_p = pd.DataFrame(comment_data_list)
        df_comment_p.columns = ['comment_id', 'goods_id', 'text', 'time', 'update_time',
                                'positive_prob', 'negative_prob', 'confidence', 'sentiment']
        try:
            df_comment_p.to_sql('t_comment_processed', engine, if_exists='append', index=False)
        except Exception as e:
            print(e)
    else:
        print("没有新评论")
    if len(df_goods) > 0:
        df_goods.columns = ['goods_id', 'brand', 'category', 'price', 'name', 'url', 'visible_price',
                            'worth', 'worthless', 'time', 'update_time']
        try:
            df_goods.to_sql('t_goods_processed', engine, if_exists='append', index=False)
        except Exception as e:
            print(e)
    else:
        print("没有商品")


# 更新分析后的数据至数据库
def update_goods_summary(df_goods, df_comment):
    df = pd.concat([df_goods['goods_id'], df_comment['goods_id']], axis=0)
    df = df.drop_duplicates()
    for goods_id in list(df):
        result = sentiment_summary(goods_id)
        comment_num = positive = neutral = negative = 0
        if result:
            for st_info in result:
                if st_info[0] == 0:
                    negative = st_info[1]
                elif st_info[0] == 1:
                    neutral = st_info[1]
                elif st_info[0] == 2:
                    positive = st_info[1]
            comment_num = negative + neutral + positive
        update_goods(goods_id, comment_num, positive, neutral, negative)


# 更新所有商品评论和情感分析统计信息
def update_goods_all():
    sql_goods = f''' select * from t_goods'''
    df_goods = pd.read_sql_query(sql_goods, engine)
    df_goods.columns = ['goods_id', 'brand', 'category', 'price', 'name', 'url', 'visible_price', 'worth', 'worthless',
                        'time', 'update_time']
    df_goods.drop_duplicates()
    df = df_goods['goods_id']
    for goods_id in list(df):
        result = sentiment_summary(goods_id)
        comment_num = positive = neutral = negative = 0
        if result:
            for st_info in result:
                if st_info[0] == 0:
                    negative = st_info[1]
                elif st_info[0] == 1:
                    neutral = st_info[1]
                elif st_info[0] == 2:
                    positive = st_info[1]
            comment_num = negative + neutral + positive
        update_goods(goods_id, comment_num, positive, neutral, negative)


# 获取所有没有分析的数据
def get_empty_comment():
    sql_comments = f'''select * from t_comment where comment_id not in (select comment_id  from t_comment_processed) and update_time <= '2020-09-02 10:00:00' '''
    df_comments = pd.read_sql_query(sql_comments, engine)

    df_c = df_comments.dropna()
    return None, df_c


# df_g, df_c = get_empty_comment()
# update_goods_summary(df_g, df_c)
# update_goods_all()
def data_analyse():
    df_g, df_c = get_new_crawl_data(24)
    process_data(df_g, df_c)
    if len(df_g) > 0 or len(df_c) > 0:
        update_goods_summary(df_g, df_c)
    for img_url in list(df_g['url'].drop_duplicates()):
        if not download_img(img_url):
            print(f"下载失败：{img_url}")
        time.sleep(0.3)
