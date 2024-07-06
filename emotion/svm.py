from utils import load_corpus, stopwords
import joblib
TRAIN_PATH = "./data/weibo2018/train.txt"
TEST_PATH = "./data/weibo2018/test.txt"


# 分别加载训练集和测试集
train_data = load_corpus(TRAIN_PATH)
test_data = load_corpus(TEST_PATH)

import pandas as pd
#加载数据集
df_train = pd.DataFrame(train_data, columns=["words", "label"])
df_test = pd.DataFrame(test_data, columns=["words", "label"])
#特征编码（Tf-Idf模型）
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(token_pattern='\[?\w+\]?',
                             stop_words=stopwords)
X_train = vectorizer.fit_transform(df_train["words"])
y_train = df_train["label"]

X_test = vectorizer.transform(df_test["words"])
y_test = df_test["label"]
model_Tfidf = joblib.dump(vectorizer,"model/vectorizer.model")
#模型训练&测试
from sklearn import svm

clf = svm.SVC()
clf.fit(X_train, y_train)
model_save = joblib.dump(clf,'model/svm.model')
# 在测试集上用模型预测结果
y_pred = clf.predict(X_test)
# 测试集效果检验
from sklearn import metrics

print(metrics.classification_report(y_test, y_pred))
print("svm准确率:", metrics.accuracy_score(y_test, y_pred))
#
# from utils import processing
#
# strs = ["只要流过的汗与泪都能化作往后的明亮，就值得你为自己喝彩", "烦死了！为什么周末还要加班[愤怒]"]
# words = [processing(s) for s in strs]
# vec = vectorizer.transform(words)
#
# output = clf.predict(vec)
# print(output)
# print(type(output[:]))
# print(output)

