import jieba
import re
import numpy as np
from sklearn.decomposition import PCA
import gensim
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from utils import processing
from getdata import df_train, df_test
import joblib
from gensim.models.word2vec import Word2Vec
from utils import load_corpus, stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

def word2vec():
    #训练词向量
    # word2vec要求的输入格式: list(word)
    wv_input = df_train['text'].map(lambda s: s.split(" "))   # [for w in s.split(" ") if w not in stopwords]
    # Word2Vec
    word2vec = Word2Vec(wv_input,
                               vector_size=64,   # 词向量维度
                               min_count=1,      # 最小词频, 因为数据量较小, 这里卡1
                               epochs=1000)      # 迭代轮次
    word2vec.save("model/word2vec.model")


def tfidf():
    # 特征编码（Tf-Idf模型）
    vectorizer = TfidfVectorizer(token_pattern='\[?\w+\]?',
                                 stop_words=stopwords)
    X_train = vectorizer.fit_transform(df_train["text"])
    y_train = df_train["label"]

    X_test = vectorizer.transform(df_test["text"])
    y_test = df_test["label"]
    model_Tfidf = joblib.dump(vectorizer, "model/vectorizer.model")

def countvec():
    #### 特征编码（词袋模型）
    vectorizer = CountVectorizer(token_pattern='\[?\w+\]?',
                                 stop_words=stopwords)
    X_train = vectorizer.fit_transform(df_train["text"])
    y_train = df_train["label"]

    # X_test = vectorizer.transform(df_test["text"])
    # y_test = df_test["label"]
    model_save = joblib.dump(vectorizer,'model/countvec.model')



def keshihua():
    # #分词
    # f = open("好莱坞.txt",'r',encoding='utf-8')
    # lines = []
    # for line in f:
    #     temp = jieba.cut(line)
    #     words = []
    #     for i in temp:
    #         # 过滤掉所有的标点符号
    #         i = re.sub("[\s+\.\!\/_,$%^*(+\"\'””《》]+|[+——！，。？、~@#￥%……&*（）：；‘]+", "", i)
    #         if len(i) > 0:
    #             words.append(i)
    #     if len(words) > 0:
    #         lines.append(words)
    # print(lines[0:5])

    # #文本读取处理
    # path = 'data/weibo2018/train.txt'
    # data = []
    # with open(path, "r", encoding="utf8") as f:
    #     for line in f:
    #         [_, seniment, content] = line.split(",", 2)
    #         content = processing(content)
    #         data.append(content)
    # print(data[0:5])

    # #模型训练
    # model = Word2Vec(data,vector_size=20,window=2, min_count=3, epochs=7,negative=10,sg=1)
    # print("昆凌的词向量：",model.wv.get_vector("昆凌"))
    # print("\n和昆凌相关性最高的20个词")
    # a = model.wv.most_similar("昆凌",topn = 20)
    # print(a)

    #可视化
    rawWordVec = []
    word2ind = {}
    for i, w in enumerate(model.wv.index_to_key):
        rawWordVec.append(model.wv[w])
        word2ind[w] = i
    rawWordVec = np.array(rawWordVec)
    X_reduced = PCA(n_components=2).fit_transform(rawWordVec)

    # 绘制星空图
    # 绘制所有单词向量的二维空间投影
    fig = plt.figure(figsize=(15,10))
    ax = fig.gca()
    ax.set_facecolor('white')
    ax.plot(X_reduced[:,0],X_reduced[:,1], '.', markersize = 1, alpha = 0.3, color = 'black')

    words = ['开心', '难过', '难受', '太开心了']

    # 设置中文字体 否则乱码
    zhfont1 = matplotlib.font_manager.FontProperties(fname='./华文仿宋.ttf', size=16)
    for w in words:
        if w in word2ind:
            ind = word2ind[w]
            xy = X_reduced[ind]
            plt.plot(xy[0], xy[1], '.', alpha = 1, color = 'orange', markersize=10)
            plt.text(xy[0], xy[1], w, fontproperties = zhfont1, alpha = 1, color = 'red')
    plt.show()

if __name__ == '__main__':
    word2vec()
    countvec()
    tfidf()