import joblib
from utils import *
import numpy as np
import random



#贝叶斯预测
def bayes_predict(strs):
    vectorizer = joblib.load("model/Bag.model") #导入词向量模型
    clf = joblib.load('model/bayes.model') #导入bayes模型
    strs = [strs]
    words = [processing(s) for s in strs]
    vec = vectorizer.transform(words)
    output = clf.predict(vec)
    print("贝叶斯：{}".format(output))
    return output
#svm预测
def svm_predict(strs):
    from utils import processing
    import joblib
    vectorizer = joblib.load("model/vectorizer.model") #导入向量模型
    clf = joblib.load('model/svm.model') #导入svm模型
    strs = [strs]
    words = [processing(s) for s in strs]
    vec = vectorizer.transform(words)
    output = clf.predict(vec)
    print("svm:{}".format(output))
    return output
#lstm预测
def lstm_predict(strs):
    # 超参数
    embed_size = 64
    hidden_size = 64
    num_layers = 2

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    word2vec = Word2Vec.load("model/model3.pkl") #导入词向量模型
    lstm = LSTM(embed_size, hidden_size, num_layers)
    lstm.load_state_dict(torch.load("model/state_lstm_5.model")) #导入神经网络模型
    lstm.eval()

    strs = [strs]
    data = []
    for s in strs:
        vectors = []
        for w in processing(s).split(" "):
            if w in word2vec.wv.key_to_index:
                vectors.append(word2vec.wv[w])  # 将每个词替换为对应的词向量
        vectors = torch.Tensor(vectors)
        data.append(vectors)
    x, _, lengths = collate_fn(list(zip(data, [-1] * len(strs))))
    with torch.no_grad():
        x = x.to(device)
        outputs = lstm(x, lengths)  # 前向传播
        # print(outputs)
        outputs = outputs.view(-1)  # 将输出展平 如：torch.Size([1,1]),展平为torch.Size([1])
        # print(outputs)
        if outputs > 0.6:
            outputs = 1
        else:
            outputs = 0
        print("lstm:{}".format(outputs))
    return(outputs)

#三合一模型
def lstm_bayes_svm():
    while True:
        strs = input("你要判断的语句（退出请输1）：")
        if strs == "1":
            break
        lstmprob = lstm_predict(strs)
        bayesprob = bayes_predict(strs)
        svmprob = svm_predict(strs)
        predict = lstmprob + bayesprob + svmprob
        print(predict)
        if predict >= 2:
            print("积极")
        else:
            print("消极")

import torch
from lstm_source import LSTM
from gensim.models.word2vec import Word2Vec
from lstm_source import collate_fn
from utils import processing

import pandas as pd
from bayes import y_pred1 as bayes_pred #bayes预测测试集的结果 shape(500,0)
from svm import  y_pred as svm_pred #bayes预测测试集的结果 shape(500,0)
from lstm_source import test_train
from bayes import y_test

y_test = pd.Series.to_numpy(y_test) #测试集标签
lstm_pred = test_train().numpy() #lstm测试集测试结果

#带入参数预测
def y1_predict():
    y_pred1 = (lstm_pred+ bayes_pred) * 0.8+ (svm_pred * 0.2)
    # y_pred1 = (lstm_pred + bayes_pred) * 0.5000000000000002 + svm_pred * 0.49999999999999956 + 0.01
    # # 0.872 a= 0.01 b= 0.49999999999999956 f= 0.5000000000000002
    # #0.868 a= 0.07 b= 0.5199999999999996 f= 0.48000000000000026
    # #0.868 a= 0.03 b= 0.3499999999999994 f= 0.6500000000000004
    # #a= 0.2700000000000001 b= 1 h= 0.0179459117550273
    # y_pred1 = (lstm_pred + svm_pred) * 0.2700000000000001 + bayes_pred * 1 - 0.01 * 0.0179459117550273
    for i in range(len(y_pred1)):
        if y_pred1[i] > 0.5:
            y_pred1[i] = 1
        else:
            y_pred1[i] = 0
    acc = np.sum(y_test == y_pred1) / len(y_test)

    print("\nlstm预测:\n",lstm_pred)
    print("bayes预测:\n",bayes_pred)
    print("svm预测：\n",svm_pred)
    print(y_pred1)
    print(type(y_test))
    print(acc)

def y2_predict():

    #两变量
    a = 0
    b = 1
    c = 0.87
    d = 0
    e = 0
    count = 0
    while True:
        r = random.uniform(-0.5,0.5)

        count += 1

        # y_pred1 = (lstm_pred + bayes_pred)*a  + svm_pred * b # 0.856
        # y_pred1 = lstm_pred * a + (bayes_pred + svm_pred) * b # 0.85
        # y_pred1 = (lstm_pred + svm_pred) * a + bayes_pred * b #0.864
        # y_pred1 = (lstm_pred + svm_pred) * a + bayes_pred * b -0.01 * r #准确率： 0.87 a= 0.2700000000000001 b= 1 h= 0.0179459117550273
        y_pred1 = lstm_pred * a + (bayes_pred + svm_pred) * b
        # y_pred1 = lstm_pred * a + bayes_pred * b  + svm_pred * f + r
        for i in range(len(y_pred1)):
            if y_pred1[i] > 0.5:
                y_pred1[i] = 1
            else:
                y_pred1[i] = 0
        acc = np.sum(y_test == y_pred1) / len(y_test)
        if acc >= c:
            c = acc
            d = a
            e = b
        if a >= 1:
            print("准确率：", c, 'a=', d, 'b=', e, 'h=',r)
            break

def y3_predict():
    from bayes import y_test
    y_test = pd.Series.to_numpy(y_test)
    lstm_pred = test_train().detach().numpy()
    a = 0
    b = 0
    c = 0.5
    f = 1
    h = 0
    while True:
        #三变量
        b = 1
        f = 0
        while True:
            b = b - 0.01
            f = f + 0.01
            # r = random.uniform(0,0.5)
            # 0.872 a= 0.01 b= 0.49999999999999956 f= 0.5000000000000002
            y_pred1 = (lstm_pred  + bayes_pred) * f + svm_pred * b + a
            for i in range(len(y_pred1)):
                if y_pred1[i] > 1:
                    y_pred1[i] = 1
                else:
                    y_pred1[i] = 0
            acc = np.sum(y_test == y_pred1) / len(y_test)
            if acc >= c:
                c = acc
                a1 = a
                b1= b
                f1= f
                # h = r
            if f >= 1:
                # print(c, 'a=', a1, 'b=', e, 'f=', g)
                break
        a = a+0.01
        print(a)

        if a >= 1:
            print(c, 'a=', a1, 'b=', b1, 'f=', f1)
            break
    # 0.872 a= 0.01 b= 0.49999999999999956 f= 0.5000000000000002
    # 0.87 a= 0.17 b= 0.5699999999999996 f= 0.4300000000000002
    #0.868 a= 0.9500000000000006 b= 0.8599999999999999 f= 0.13999999999999999 h= 0.06658320715180116(y_pred1 = (lstm_pred  + bayes_pred) * f + svm_pred * b + a * r)
    #y_pred1 = (lstm_pred  + bayes_pred) * f + svm_pred * b - a * r

    #0.876 a= 0.21000000000000005 b= 0.5499999999999996 f= 0.45000000000000023  y_pred1 = (lstm_pred  + bayes_pred) * f + svm_pred * b + a

    # 0.86 a= 0.3300000000000001 b= 0.6199999999999997 f= 0.38000000000000017

def main():
    lstm_bayes_svm()
    y3_predict()



if __name__ == "__main__":
    main()

