from utils import load_corpus, stopwords
from sklearn import metrics
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from utils import processing
import joblib
import numpy as np



#加载数据集
TRAIN_PATH = "./data/weibo2018/train.txt"
TEST_PATH = "./data/weibo2018/test.txt"
# 分别加载训练集和测试集
train_data = load_corpus(TRAIN_PATH)
test_data = load_corpus(TEST_PATH)
df_train = pd.DataFrame(train_data, columns=["words", "label"])
df_test = pd.DataFrame(test_data, columns=["words", "label"])
#特征编码（词袋模型）
vectorizer = CountVectorizer(token_pattern='\[?\w+\]?',
                             stop_words=stopwords)

X_train = vectorizer.fit_transform(df_train["words"])
y_train = df_train["label"]

X_test = vectorizer.transform(df_test["words"])
y_test = df_test["label"]
model_Bag = joblib.dump(vectorizer,"model/Bag.model")

#训练模型&测试
clf = MultinomialNB()
clf=clf.fit(X_train, y_train)

#保存模型
joblib.dump(clf,"model/bayes.model")
# 在测试集上用模型预测结果
y_pred = clf.predict(X_test)
# print(y_test.shape)
# print(type(y_test))
print(metrics.classification_report(y_test, y_pred))
print("贝叶斯准确率:", metrics.accuracy_score(y_test, y_pred))



# clf = joblib.load('model/bayes.model')

# 手动输入句子，判断情感倾向

# strs = ["今天天气很好","今天天气很差"]
# if strs == ["1"]:
#     break
# print(type(strs))
# words = [processing(s) for s in strs]
# vec = vectorizer.transform(words)
# output = clf.predict_proba(vec)
# sum = np.sum(output[:,1])
# print(output)
# print(type(output[:,1]))
# print(output[:,1])
# print(sum)



