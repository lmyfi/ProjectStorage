from utils import load_corpus, stopwords
import joblib
from gensim.models.word2vec import Word2Vec
from getdata import df_train, df_test
from sklearn.model_selection import train_test_split

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


from utils import processing

strs = ["只要流过的汗与泪都能化作往后的明亮，就值得你为自己喝彩", "烦死了！为什么周末还要加班[愤怒]", "太差了"]
words = [processing(s) for s in strs]
vec = vectorizer.transform(words)

output = clf.predict(vec)
print(output)
print(type(output[:]))
print(output)

