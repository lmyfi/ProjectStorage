import sys
from PyQt5.Qt import *


class window(QWidget):
    def __init__(self):
        global n
        n = list()
        super().__init__()
        self.setWindowTitle('情感识别')
        self.move(100, 100)
        self.resize(500, 500)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setup_button()
        self.setup_label()
        self.setup_Edit()

    def setup_button(self):
        but1 = QPushButton(self)
        but2 = QPushButton(self)
        but2.setText('清除')
        but1.setText('开始分析')
        but1.move(200, 250)
        but2.move(200, 300)
        but1.pressed.connect(self.but1_do)
        but2.pressed.connect(self.clear)

    def setup_label(self):
        lab1 = QLabel(self)
        lab1.setText('输入你的语句')
        lab2 = QLabel(self)
        lab2.setText('感知你的情感可能是：')
        lab2.move(0, 400)
        lab3 = QLabel(self)
        lab3.setText('裂开')
        lab3.move(0, 420)
        lab3.setStyleSheet('background-color:cyan; font-size:40px;')
        lab3.adjustSize()
        lab4 = QLabel(self)
        lab4.setPixmap(QPixmap('P1.jpg'))
        lab4.resize(190, 190)
        lab4.move(300, 300)
        lab4.setScaledContents(True)

    def setup_Edit(self):
        self.Ed = QTextEdit(self)
        self.Ed.resize(450, 225)
        self.Ed.move(25, 25)
        self.Ed.setStyleSheet("background-color:cyan")
        self.Ed.insertPlainText("123")

    def clear(self):
        self.Ed.clear()

    def but1_do(self):
        m = self.Ed.toPlainText()
        n.append(m)
        print('m=', m)
        print('n=', n)

        import joblib
        import torch
        from lstm_source import LSTM
        from gensim.models.word2vec import Word2Vec
        from lstm_source import collate_fn
        from utils import processing

        vectorizer = joblib.load('结果/vectorizer.model') #词向量模型
        #贝叶斯预测
        clf = joblib.load('model/bayes.model')
        strs = [m]
        words = [processing(s) for s in strs]
        vec = vectorizer.transform(words)
        output = clf.predict_proba(vec)
        bayesprob = output[:, 1]
        # print(bayesprob)
        # print('第一段')

        #svm预测
        clf = joblib.load('model/svm.model')
        strs = [strs]#words = [processing(s) for s in strs]
        vec = vectorizer.transform(words)
        svmprob = clf.predict(vec)# return output

        #lstm神经网络预测
        #超参数
        embed_size = 64
        hidden_size = 64
        num_layers = 2

        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        word2vec = Word2Vec.load("model/model3.pkl")
        lstm = LSTM(embed_size, hidden_size, num_layers)
        lstm.load_state_dict(torch.load("model/state_lstm_5.model"))
        lstm.eval()
        strs = [m]
        data = []
        for s in strs:
            vectors = []
            for w in processing(s).split(" "):
                if w in word2vec.wv.key_to_index:
                    vectors.append(word2vec.wv[w])# 将每个词替换为对应的词向量
            vectors = torch.Tensor(vectors)
            data.append(vectors)
        x, _, lengths = collate_fn(list(zip(data, [-1] * len(strs))))
        with torch.no_grad():
            x = x.to(device)
            outputs = lstm(x, lengths)# 前向传播
            outputs = outputs.view(-1)# 将输出展平
            lstmprob = outputs.numpy()
        # print(outputs)# outputs = item(outputs)
        # predict = output1 * 0.3 + output * 0.3 + outputs.numpy()*0.4 #return predict
        predict = (lstmprob + bayesprob) * 0.8+ svmprob* 0.2



        if predict> 1:
             print('积极')
             x = '积极'
             lab3 = QLabel(self)
             lab3.setText(x)
             lab3.move(0, 420)
             lab3.setStyleSheet('background-color:cyan; font-size:40px;')
             lab3.adjustSize()
             lab3.show()

        else:
             print('消极')
             x = '消极'
             lab3 = QLabel(self)
             lab3.setText(x)
             lab3.move(0, 420)
             lab3.setStyleSheet('background-color:cyan; font-size:40px;')
             lab3.adjustSize()
             lab3.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = window()
    Window.show()
    sys.exit(app.exec())
