from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import joblib
from getdata import df_test, df_train
from sklearn.model_selection import train_test_split
from utils import processing


vectorizer = joblib.load('model/vectorizer.model')

# x = df_train["text"]
# y = df_train["label"]
# x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.25,random_state=0)
# X_train = vectorizer.fit_transform(x_train)
# X_test = vectorizer.transform(x_test)


X_train = vectorizer.fit_transform(df_train["text"])
y_train = df_train["label"]

X_test = vectorizer.transform(df_test["text"])
y_test = df_test["label"]

# 贝叶斯准确率: 0.862
# [[0.5379993  0.4620007 ]
#  [0.58542482 0.41457518]]

model_Bag = joblib.dump(vectorizer,"model/Bag.model")

#训练模型&测试
clf = MultinomialNB()
clf=clf.fit(X_train, y_train)


#保存模型
joblib.dump(clf,"model/bayes.model")
# 在测试集上用模型预测结果
y_pred = clf.predict(X_test)
output = clf.predict_proba(X_test)
y_pred1 = output[:,1]
print(y_pred1.shape)

print(metrics.classification_report(y_test, y_pred))
print("贝叶斯准确率:", metrics.accuracy_score(y_test, y_pred))



# clf = joblib.load('model/bayes.model')

# 手动输入句子，判断情感倾向

strs = ["今天天气很好","今天天气很差"]
words = [processing(s) for s in strs]
vec = vectorizer.transform(words)
output = clf.predict_proba(vec)
# sum = np.sum(output[:,1])
print(output)
# print(type(output[:,1]))
# print(output[:,1])
# print(sum)



