import joblib
import torch
from lstm_source import LSTM
from gensim.models.word2vec import Word2Vec
from lstm_source import collate_fn
from utils import processing

#贝叶斯预测
def bayes_predict(strs):
    vectorizer = joblib.load("model/Bag.model") #导入训练好的词向量模型
    clf = joblib.load('model/bayes.model') #导入bayes模型
    strs = [strs]
    words = [processing(s) for s in strs]
    vec = vectorizer.transform(words)
    output = clf.predict_proba(vec)
    output=output[:, 1]
    return output

#svm预测
def svm_predict(strs):
    from utils import processing
    import joblib
    vectorizer = joblib.load("model/vectorizer.model") #导入训练好的词向量模型
    clf = joblib.load('model/svm.model') #导入训练好的svm模型
    strs = [strs]
    words = [processing(s) for s in strs]
    vec = vectorizer.transform(words)
    output = clf.predict(vec)
    return output

#Lstm神经网络预测
def lstm_predict(strs):
    # 超参数
    embed_size = 64
    hidden_size = 64
    num_layers = 2

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    word2vec = Word2Vec.load("model/model3.pkl") #导入训练好的词向量模型
    lstm = LSTM(embed_size, hidden_size, num_layers)
    lstm.load_state_dict(torch.load("model/state_lstm_5.model")) #导入lstm模型
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
        outputs = outputs.view(-1)  # 将输出展平
        print(outputs)
        print(type(outputs))
    return outputs

def lstm_bayes_svm(strs):
    lstmprob = lstm_predict(strs)
    bayesprob = bayes_predict(strs)
    svmprob = svm_predict(strs)
    predict = (lstmprob + bayesprob) * 0.8+ (svmprob* 0.2)
    return predict




if __name__ == "__main__":
    while True:
        input_str = input("你要判断的语句（退出请输1）：")
        if input_str == "1":
            break
        output = lstm_bayes_svm(input_str)
        if output > 1:
            print("积极")
        else:
            print("消极")


