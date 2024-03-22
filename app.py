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
    # 景点电影数量、评分统计、词汇统计
    movie_number = []
    score_statistics = []
    vocabulary_statistics = len(GenerateWordCloud().cut_dada())
    total_people = []

    con = sqlite3.connect("movie250.db")
    cur = con.cursor()
    sql = "select count(id) from movie250"
    data = cur.execute(sql)
    for item in data:
        movie_number.append(item)

    # 电影总分
    total_score = "select SUM(score) from movie250"
    total_score_data = cur.execute(total_score)
    for item in total_score_data:
        score_statistics.append(item)

    # 电影总人数
    people = "select SUM(rated) from movie250"
    total_people_data = cur.execute(people)
    for item in total_people_data:
        total_people.append(item)
    cur.close()
    con.close()

    movie_number = movie_number[0][0]
    score_statistics = score_statistics[0][0]
    total_people = total_people[0][0]
    score_statistics = round(score_statistics * total_people / total_people / movie_number, 1)
    print(total_people)
    return render_template('index.html', movie_number=movie_number, vocabulary_statistics=vocabulary_statistics,
                           score_statistics=score_statistics)


@app.route('/index')
def home():
    """ 首页 """
    # 景点电影数量、评分统计、词汇统计
    movie_number = []
    score_statistics = []
    vocabulary_statistics = len(GenerateWordCloud().cut_dada())
    total_people = []

    con = sqlite3.connect("movie250.db")
    cur = con.cursor()
    sql = "select count(id) from movie250"
    data = cur.execute(sql)
    for item in data:
        movie_number.append(item)

    # 电影总分
    total_score = "select SUM(score) from movie250"
    total_score_data = cur.execute(total_score)
    for item in total_score_data:
        score_statistics.append(item)

    # 电影总人数
    people = "select SUM(rated) from movie250"
    total_people_data = cur.execute(people)
    for item in total_people_data:
        total_people.append(item)
    cur.close()
    con.close()

    movie_number = movie_number[0][0]
    score_statistics = score_statistics[0][0]
    total_people = total_people[0][0]
    score_statistics = round(score_statistics * total_people / total_people / movie_number, 1)
    print(total_people)
    return render_template('index.html', movie_number=movie_number, vocabulary_statistics=vocabulary_statistics,
                           score_statistics=score_statistics)

@app.route('/movie')
def movie():
    """ 电影详情 """
    data_list = []
    con = sqlite3.connect("movie250.db")
    cur = con.cursor()
    sql = "select * from movie250"
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