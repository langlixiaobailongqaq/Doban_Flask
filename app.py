#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:zhengxin
@file: app.py.py
@time: 2024/3/20  14:19
# @describe:
"""
import sqlite3
from flask import request
from flask import Flask, render_template

from word_cloud import GenerateWordCloud

app = Flask(__name__)


# 启用调试模式
app.debug = True


@app.route('/')
def index():
    """ 首页-景点电影数量、评分统计、词汇统计 """
    # 景点电影数量
    movie_number = []
    # 电影总分
    score_statistics = []
    # 词汇统计
    vocabulary_statistics = len(GenerateWordCloud().cut_dada())
    # 电影总人数
    total_people = []

    con = sqlite3.connect("movie250.db")
    cur = con.cursor()
    sql = "select count(id),SUM(score),SUM(rated) from movie250"
    data = cur.execute(sql)
    for item in data:
        movie_number.append(item[0])
        score_statistics.append(item[1])
        total_people.append(item[2])
    cur.close()
    con.close()

    movie_number = movie_number[0]
    score_statistics = score_statistics[0]
    total_people = total_people[0]
    score_statistics = round(score_statistics * total_people / total_people / movie_number, 1)
    # print(movie_number, score_statistics,  total_people)
    return render_template('index.html', movie_number=movie_number, vocabulary_statistics=vocabulary_statistics,
                           score_statistics=score_statistics)


@app.route('/index')
def home():
    """ 首页-景点电影数量、评分统计、词汇统计 """
    # 景点电影数量
    movie_number = []
    # 电影总分
    score_statistics = []
    # 词汇统计
    vocabulary_statistics = len(GenerateWordCloud().cut_dada())
    # 电影总人数
    total_people = []

    con = sqlite3.connect("movie250.db")
    cur = con.cursor()
    sql = "select count(id),SUM(score),SUM(rated) from movie250"
    data = cur.execute(sql)
    for item in data:
        movie_number.append(item[0])
        score_statistics.append(item[1])
        total_people.append(item[2])
    cur.close()
    con.close()

    movie_number = movie_number[0]
    score_statistics = score_statistics[0]
    total_people = total_people[0]
    score_statistics = round(score_statistics * total_people / total_people / movie_number, 1)
    # print(movie_number, score_statistics,  total_people)
    return render_template('index.html', movie_number=movie_number, vocabulary_statistics=vocabulary_statistics,
                           score_statistics=score_statistics)


@app.route('/movie')
def movie():
    """ 电影详情 """
    data_list = []
    con = sqlite3.connect("movie250.db")
    cur = con.cursor()
    sql = "select * from movie250 ORDER BY ename, score DESC"
    data = cur.execute(sql)
    for item in data:
        data_list.append(item)
    cur.close()
    con.close()

    # 当前页码，从第一页开始
    page = int(request.args.get("page", 1))
    # 每页的数量
    per_page = int(request.args.get('per_page', 25))

    # 计算开始和结束项
    start = (page - 1) * per_page
    end = start + per_page

    # 获取当前页面的数据
    paginate_data = data_list[start:end]
    # 计算总页数
    total_pages = (len(data_list) + per_page - 1) // per_page
    return render_template('movie.html', movies=paginate_data, total_pages=total_pages, current_page=page)


@app.route('/search', methods=['GET'])
def search():
    """ 搜索 """
    keyword = request.args.get('q', '')
    con = sqlite3.connect("movie250.db")
    cur = con.cursor()
    sql = "select * from movie250 where cname like '%{}%'".format(keyword)
    data = cur.execute(sql)
    data_list = []
    for item in data:
        data_list.append(item)
    cur.close()
    con.close()

    # 当前页码，从第一页开始
    page = int(request.args.get("page", 1))
    # 每页的数量
    per_page = int(request.args.get('per_page', 25))

    # 计算开始和结束项
    start = (page - 1) * per_page
    end = start + per_page

    # 获取当前页面的数据
    paginate_data = data_list[start:end]
    # 计算总页数
    total_pages = (len(data_list) + per_page - 1) // per_page
    return render_template('movie.html', movies=paginate_data, total_pages=total_pages, current_page=page)


@app.route('/score')
def score():
    """ 电影评分 """
    # 评分
    score = []
    # 每一个电影评分对应的电影数量
    num = []
    con = sqlite3.connect('movie250.db')
    cur = con.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))
        num.append(item[1])
    cur.close()
    con.close()
    return render_template('score.html', score=score, num=num)


@app.route('/word')
def word():
    """ 词云 """
    return render_template('word.html')


@app.route('/team')
def team():
    return render_template('team.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)