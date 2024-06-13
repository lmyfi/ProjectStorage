from utils import processing
from utils import load_corpus
import pandas as pd
from sklearn.model_selection import train_test_split
#lstm
TRAIN_PATH = "./data/weibo2018/train.txt"
TEST_PATH = "./data/weibo2018/test.txt"

# 分别加载训练集和测试集
train_data = load_corpus(TRAIN_PATH)
test_data = load_corpus(TEST_PATH)


df_train = pd.DataFrame(train_data, columns=["text", "label"])
df_test = pd.DataFrame(test_data, columns=["text", "label"])

# train_test = df_train["text"]
# train_train = df_train["label"]
#
# df_train,

