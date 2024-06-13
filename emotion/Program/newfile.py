import joblib
from utils import processing

vec = joblib.load("model/vectorizer.model")
svm = joblib.load("model/svm.model")
bayes = joblib.load("model/bayes.model")
strs = ["你好吗？"]
words = [processing(s) for s in strs]
# vec = vec.fit_transform(words)
vec = vec.transform(words)
output = svm.predict(vec)
print(output)
