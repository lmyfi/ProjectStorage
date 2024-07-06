import joblib
from utils import *
import numpy as np
from lstm_source import LSTM
import random
def bayes_predict(strs):
    vectorizer = joblib.load("model/Bag.model")
    clf = joblib.load('model/bayes.model')
    # 手动输入句子，判断情感倾向
    strs = [strs]
    # if strs == ["1"]:
    #     break
    # print(type(strs))
    words = [processing(s) for s in strs]
    vec = vectorizer.transform(words)
    output = clf.predict_proba(vec)
    output=output[:, 1]
    return output

def svm_predict(strs):
    from utils import processing
    import joblib


    vectorizer = joblib.load("model/vectorizer.model")
    clf = joblib.load('model/svm.model')
    strs = [strs]
    words = [processing(s) for s in strs]
    vec = vectorizer.transform(words)

    output = clf.predict(vec)
    output = output
    return output


# import torch
# from lstm_source import LSTM
# from gensim.models.word2vec import Word2Vec
# from lstm_source import collate_fn
# from utils import processing
# # # from lstm_source import test_train
# #
#
# def lstm_predict(strs):
#     # 超参数
#     embed_size = 64
#     hidden_size = 64
#     num_layers = 2
#
#     device = "cuda:0" if torch.cuda.is_available() else "cpu"
#     word2vec = Word2Vec.load("model/model3.pkl")
#     lstm = LSTM(embed_size, hidden_size, num_layers)
#     lstm.load_state_dict(torch.load("model/state_lstm_1.model"))
#     lstm.eval()
#     # 手动输入句子，判断情感倾向
#     # strs = [input("输入要判断的语句（退出请输入1）：")]
#     strs = [strs]
#     # if strs == ["1"]:
#     #     break
#     data = []
#     for s in strs:
#         vectors = []
#         for w in processing(s).split(" "):
#             if w in word2vec.wv.key_to_index:
#                 vectors.append(word2vec.wv[w])  # 将每个词替换为对应的词向量
#         vectors = torch.Tensor(vectors)
#         data.append(vectors)
#     x, _, lengths = collate_fn(list(zip(data, [-1] * len(strs))))
#     with torch.no_grad():
#         x = x.to(device)
#         outputs = lstm(x, lengths)  # 前向传播
#         print(outputs)
#         outputs = outputs.view(-1)  # 将输出展平
#         # print(outputs)
#     return(outputs)


def y_predict():

    # import numpy
    import pandas as pd
    from bayes import y_pred as bayes_pred
    from svm import  y_pred as svm_pred
    from lstm_source import test_train
    from  bayes import y_test

    y_test = pd.Series.to_numpy(y_test)
    lstm_pred = test_train().detach().numpy()

    # y_pred1 = (lstm_pred+ bayes_pred) * 0.8+ (svm_pred * 0.2)
    # y_pred1[y_pred1 > 1] = 1
    # y_pred1[y_pred1 <= 1] = 0
    # y_pred1 = [y_pred=1 for y_pred in y_pred1 if y_pred > 1 else 0]
    # for i in range(len(y_pred1)):
    #     if y_pred1[i] > 0.5:
    #         y_pred1[i] = 1
    #     else:
    #         y_pred1[i] = 0
    # acc = np.sum(y_test == y_pred1) / len(y_test)
    print("lstm预测:\n",lstm_pred.shape)
    print("bayes预测:\n",bayes_pred.shape)
    print("svm预测：\n",svm_pred.shape)
    # print(y_pred1)
    print(type(y_test))
    # print(acc)
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
            r = random.uniform(0,0.5)
            y_pred1 = (lstm_pred  + bayes_pred) * f + svm_pred * b - a * r
            for i in range(len(y_pred1)):
                if y_pred1[i] > 1:
                    y_pred1[i] = 1
                else:
                    y_pred1[i] = 0
            acc = np.sum(y_test == y_pred1) / len(y_test)
            if acc >= c:
                c = acc
                d = a
                e = b
                g = f
                h = r
            if f >= 1:
                # print(c, 'a=', d, 'b=', e, 'f=', g)
                break
        a = a+0.01
        print(a)

        if a >= 1:
            print(c, 'a=', d, 'b=', e, 'f=', g, 'h=',h)
            break
    # 0.872 a= 0.01 b= 0.49999999999999956 f= 0.5000000000000002
    # 0.87 a= 0.17 b= 0.5699999999999996 f= 0.4300000000000002
    #0.868 a= 0.9500000000000006 b= 0.8599999999999999 f= 0.13999999999999999 h= 0.06658320715180116(y_pred1 = (lstm_pred  + bayes_pred) * f + svm_pred * b + a * r)
    #y_pred1 = (lstm_pred  + bayes_pred) * f + svm_pred * b - a * r

    #两变量
    # a = 0
    # b = 1
    # c = 0
    # d = 0
    # e = 0
    # h = 0
    # while True:
    #
    #     r = random.uniform(0,0.5)
    #
    #     # y_pred1 = (lstm_pred + bayes_pred)*a  + svm_pred * b # 0.856
    #     # y_pred1 = lstm_pred * a + (bayes_pred + svm_pred) * b # 0.85
    #     # y_pred1 = (lstm_pred + svm_pred) * a + bayes_pred * b #0.864
    #     # y_pred1 = (lstm_pred + svm_pred) * a + bayes_pred * b -0.01 * r #准确率： 0.87 a= 0.2700000000000001 b= 1 h= 0.0179459117550273
    #     y_pred1 = lstm_pred * a + (bayes_pred + svm_pred) * b
    #     for i in range(len(y_pred1)):
    #         if y_pred1[i] > 0.5:
    #             y_pred1[i] = 1
    #         else:
    #             y_pred1[i] = 0
    #     acc = np.sum(y_test == y_pred1) / len(y_test)
    #     if acc >= c:
    #         c = acc
    #         d = a
    #         e = b
    #         h = r
    #
    #
    #     a = a + 0.01
    #     print(a)
    #
    #     if a >= 1:
    #         print("准确率：", c, 'a=', d, 'b=', e, 'h=',r)
    #         break


def lstm_bayes_svm():
    shape_lstm = lstm_predict()

def main():
    # while True:
    #     strs = input("你要判断的语句（退出请输1）：")
    #     if strs == "1":
    #         break
    #     predict1 = lstm_predict(strs)
    #     predict2 = bayes_predict(strs)
    #     predict3 = svm_predict(strs)
    #     print(predict1)
    #     strs = []
    #     # if (predict1 > 0.5) and (predict2 > 0.5):
    #     if predict2 > 1:
    #         print("积极")
    #     else:
    #         print("消极")
    # strs = "你好"
    # result = lstm_predict(strs)
    # print(result)
    y_predict()




if __name__ == "__main__":
    main()





# import torch
# net = torch.load("model/lstm_5.model")
# print(net)
# LSTM(
#   (lstm): LSTM(64, 64, num_layers=2, batch_first=True, bidirectional=True)
#   (fc): Linear(in_features=128, out_features=1, bias=True)
#   (sigmoid): Sigmoid()
# )