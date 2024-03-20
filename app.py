#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:zhengxin
@file: app.py.py
@time: 2024/3/20  14:19
# @describe:
"""
import sqlite3

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/movie')
def movie():
    data_list = []
    con = sqlite3.connect('movie250.db')
    cur = con.cursor()
    sql = "select* from movie250"
    data = cur.execute(sql)
    for item in data:
        data_list.append(item)
    cur.close()
    con.close()
    # print(data_list)
    return render_template('movie.html', movies=data_list)



@app.route('/score')
def score():
    return render_template('score.html')


@app.route('/word')
def word():
    return render_template('word.html')


@app.route('/team')
def team():
    return render_template('team.html')


if __name__ == '__main__':
    app.run()
