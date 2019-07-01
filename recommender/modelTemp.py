#推荐算法示例 来自电影数据集
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error
from math import sqrt
from scipy.sparse.linalg import svds


header = ['user_id', 'item_id', 'rating', 'timestamp']

df = pd.read_csv('../data/u.data', sep = '\t', names = header)
n_users = df.user_id.unique().shape[0]#用户数量
n_items = df.item_id.unique().shape[0]#物品数量
print('Number of users = ' + str(n_users) + ' | Number of movies = ' + str(n_items))
# 数据集分割——训练集：测试集 = 3:1
train_data,test_data = train_test_split(df, test_size = 0.25)

train_data_matrix = np.zeros((n_users,n_items))
test_data_matrix = np.zeros((n_users, n_items))
#使用 pandas 遍历行数据
for line in train_data.itertuples():
    #训练集评分矩阵
    train_data_matrix[line[1]-1, line[2]-1] = line[3]
for line in test_data.itertuples():
    #测试集评分矩阵
    test_data_matrix[line[1]-1, line[2]-1] = line[3]

user_similarity = pairwise_distances(train_data_matrix, metric = "cosine")
item_similarity = pairwise_distances(train_data_matrix.T, metric = "cosine")

def predict(rating, similarity, type = 'user'):
    if type == 'user':
        mean_user_rating = rating.mean(axis = 1)    #mean函数：压缩列，对各行求均值，返回 m *1 矩阵
        # print(mean_user_rating)
        rating_diff = (rating - mean_user_rating[:,np.newaxis])
        pred = mean_user_rating[:,np.newaxis] + similarity.dot(rating_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
        #dot函数：矩阵相乘；np.abs()：矩阵元素的绝对值  .T:转置
        # print('test',pred.min())
    elif type == 'item':
        pred = rating.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
        # print('test2',pred.max())
    return pred


item_prediction = predict(train_data_matrix, item_similarity, type = 'item')
user_prediction = predict(train_data_matrix, user_similarity, type = 'user')


def rmse(prediction, ground_truth):
    #nonzero(a)返回数组a中值不为零的元素的下标
    #flatten()创建矩阵
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))
print('User based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix)))
print('Item based CF RMSE: ' + str(rmse(item_prediction, test_data_matrix)))

u, s, vt = svds(train_data_matrix, k=20)
s_diag_matrix = np.diag(s)
X_pred = np.dot(np.dot(u, s_diag_matrix), vt)

print('User-based CF MSE: ' + str(rmse(X_pred, test_data_matrix)))