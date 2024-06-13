import jieba
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import os,sys
import numpy as np
import pandas as pd

#文件路径
path = "E:/2/WeiboSentiment-master/data/weibo2018/train.txt"
filepath = os.path.join(path)

#  读取文件
with open(filepath, 'r+', encoding='utf8') as f:
    text = f.read()

# 结巴分词
jieba.add_word("多流形")
raw = list(jieba.cut(text, cut_all=False))

# 获取停用词列表
stopwords_path = os.path.join(path)
stopword_list = []
with open(stopwords_path, 'r+', encoding='utf8') as f:
    for word in f.readlines():
        if len(word) > 0 and word != '\t\n':
            stopword_list.append(word)

# 文本清洗 获得干净文本
pure_text = []
for word in raw:
    if len(word) > 1 and word != "\n\r":
        if not word.isdigit():  # 去数字
            if word.strip() not in stopword_list:  # 去左右空格
                pure_text.append(word.strip())

# （1）用DataFrame操作
content = pd.DataFrame(pure_text, columns=['word'])
# 每个词出现的频率赋予一个新的列
content_new = content.groupby(by=['word'])['word'].agg([("count","count")])
# 按频率排序
content_new = content_new.reset_index().sort_values(by=['count'], ascending=False)
wordcloud = WordCloud(font_path='msyh.ttc', background_color='white', max_font_size=80)
word_frequence = {x[0]:x[1] for x in content_new.head(100).values}

wordcloud = wordcloud.fit_words(word_frequence)
# 展示图片
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
# 保持图片
