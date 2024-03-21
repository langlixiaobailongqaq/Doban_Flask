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

app = Flask(__name__)


# 启用调试模式
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    """ 首页 """
    return render_template('index.html')


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
    app.run()
