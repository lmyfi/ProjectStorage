from utils import load_corpus, stopwords
import numpy as np
import joblib
import pandas as pd
from gensim.models.word2vec import Word2Vec
def get_data():
    TRAIN_PATH = "./data/weibo2018/train.txt"
    TEST_PATH = "./data/weibo2018/test.txt"

    # 分别加载训练集和测试集
    train_data = load_corpus(TRAIN_PATH)
    test_data = load_corpus(TEST_PATH)
    df_train = pd.DataFrame(train_data, columns=["text", "label"])
    df_test = pd.DataFrame(test_data, columns=["text", "label"])
    return df_test, df_train

def get_vec():
    word2vec = Word2Vec.load("model/model3.pkl")
    return word2vec




import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
from torch.utils.data import Dataset, DataLoader

device = "cuda:0" if torch.cuda.is_available() else "cpu"

# 超参数
learning_rate = 5e-4
input_size = 768
num_epoches = 5
batch_size = 100
embed_size = 64
hidden_size = 64
num_layers = 2


# 数据集
class MyDataset(Dataset):
    def __init__(self, df):
        word2vec = get_vec()
        self.data = []
        self.label = df["label"].tolist()
        for s in df["text"].tolist():
            vectors = []
            for w in s.split(" "):
                if w in word2vec.wv.key_to_index:
                    vectors.append(word2vec.wv[w])  # 将每个词替换为对应的词向量
            vectors = torch.Tensor(vectors)
            self.data.append(vectors)

    def __getitem__(self, index):
        data = self.data[index]
        label = self.label[index]
        return data, label

    def __len__(self):
        return len(self.label)


def collate_fn(data):
    """
    :param data: 第0维：data，第1维：label
    :return: 序列化的data、记录实际长度的序列、以及label列表
    """
    data.sort(key=lambda x: len(x[0]), reverse=True)  # pack_padded_sequence要求要按照序列的长度倒序排列
    data_length = [len(sq[0]) for sq in data]
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    data = pad_sequence(x, batch_first=True, padding_value=0)  # 用RNN处理变长序列的必要操作
    return data, torch.tensor(y, dtype=torch.float32), data_length



def get_test_train():
    df_train, df_test = get_data()
    # 训练集
    train_data = MyDataset(df_train)
    train_loader = DataLoader(train_data, batch_size=batch_size, collate_fn=collate_fn, shuffle=True)

    # 测试集
    test_data = MyDataset(df_test)
    test_loader = DataLoader(test_data, batch_size=batch_size, collate_fn=collate_fn, shuffle=True)


# 网络结构
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size * 2, 1)  # 双向, 输出维度要*2
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, lengths):
        h0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(device)  # 双向, 第一个维度要*2
        c0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(device)

        packed_input = torch.nn.utils.rnn.pack_padded_sequence(input=x, lengths=lengths, batch_first=True)
        packed_out, (h_n, h_c) = self.lstm(packed_input, (h0, c0))

        lstm_out = torch.cat([h_n[-2], h_n[-1]], 1)  # 双向, 所以要将最后两维拼接, 得到的就是最后一个time step的输出
        out = self.fc(lstm_out)
        out = self.sigmoid(out)
        return out




