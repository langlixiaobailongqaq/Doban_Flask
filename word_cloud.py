#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:zhengxin
@file: wordcloud.py
@time: 2024/3/21  10:55
# @describe:
"""
import jieba                # 分词
from PIL import Image       # 图片处理
from wordcloud import WordCloud     # 绘图数据可视化
import matplotlib.pyplot as plt     # 词云
import numpy as np      # 矩阵运算
import sqlite3


# 词云所需的文字数据
conn = sqlite3.connect('movie250.db')
cur = conn.cursor()
data = cur.execute('select introduction  from movie250')
text = ''
for item in data:
    # 将所有文本拼接到一起
    text = text + item[0]
    # print(text)
cur.close()
conn.close()


# 分词
cut = jieba.cut(text)
string = ''.join(cut)
print(len(string))

# 打开遮罩图片
img = Image.open(r'./static/assets/img/tree.jpg')
# 将图片转变为图片数组
img_array = np.array(img)

# 设置词云参数
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path='/System/Library/Fonts/PingFang.ttc'
)

# 生成词云-从文本中选择生成的词云对象
wc.generate(string)

# 绘制词云-从第一个位置开始绘制
fig = plt.figure(1)
# 按照词云wc 的规则进行显示词云图片
plt.imshow(wc)
# 关闭坐标轴
plt.axis('off')
# 查看效果
# plt.show()

#  保存词云图片-设置分辨率(保存词云图片时，需注释 plt.show() 代码)
plt.savefig(r'./static/assets/img/word_cloud.jpg', dpi=500)

