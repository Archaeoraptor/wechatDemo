# 评分预测

import csv
from sklearn.feature_extraction.text import TfidfVectorizer as TFIV
import numpy as np
from scipy.stats import pearsonr
import csv
import random
from sklearn.metrics import pairwise_distances, mean_squared_error
from math import sqrt
from recommender.process.generateTrainData import getFeatureMatrix, getStopwords


def evaluateByRMSE(pred, testRatingMatrix):
    # nonzero(a)返回数组a中值不为零的元素的下标
    # flatten()创建矩阵
    # print(pred)
    prediction = pred[testRatingMatrix.nonzero()].flatten()
    ground_truth = testRatingMatrix[testRatingMatrix.nonzero()].flatten()
    # print(ground_truth.shape)
    return sqrt(mean_squared_error(prediction, ground_truth))


def dataSplit(factor):
    f_in = csv.reader(open("../data/recommender/train/SR.csv", "r", encoding="utf-8"))
    train = csv.writer(open("../data/recommender/train/train.csv", "w", encoding="utf-8", newline=""))
    test = csv.writer(open("../data/recommender/train/test.csv", "w", encoding="utf-8", newline=""))
    ls = []
    size = 0
    for line in f_in:
        size += 1
        ls.append(line)
    index = int(size * factor)
    random.shuffle(ls)
    for line in ls[:index]:
        train.writerow(line)
    for line in ls[index:]:
        test.writerow(line)


def getPredScores(id, weights, scores):
    """
    @return param:recommendRes Dict格式，文章id-评分预测结果
    """
    res = {}  # 文章加权评分
    times = {}  # 次数，加权平均值的分母
    for userId, articleDic in scores.items():
        if id != userId:
            for article, score in articleDic.items():
                if article not in res.keys():
                    res[article] = 0.0
                    a = weights[userId]
                    b = score
                    c = a * int(b)
                    res[article] = weights[userId] * int(score) + res[article]

                    if article not in times.keys():
                        times[article] = 1
                    else:
                        times[article] += 1
                else:
                    res[article] = weights[userId] * int(score) + res[article]
                    if article not in times.keys():
                        times[article] = 1
                    else:
                        times[article] += 1
    recommendRes = {}
    for articleId, score in res.items():
        recommendRes[articleId] = score / times[articleId]
    return recommendRes


def getPearsonMatrix():
    """
    @return param： pearsonrMatrix 用户相关系数矩阵  userLen * userLen
    """
    matrix = getFeatureMatrix()
    pearsonrMatrix = pairwise_distances(matrix, metric="cosine")
    # pearsonrMatrix = np.zeros((100, 100))
    # for i in range(100):
    #     for j in range(100):
    #         pearsonrMatrix[i, j] = pearsonr(matrix[i], matrix[j])[0]
    return pearsonrMatrix


def getPearsonMatrix_2():
    """
    @return param： pearsonrMatrix 用户相关系数矩阵  userLen * userLen
    基于病案首页计算相关系数
    """
    f_in = csv.reader(open("../data/recommender/process/medicalRecord.csv", "r", encoding="utf-8"))

    user_data = []
    for line in f_in:
        user_data.append(" ".join(line[3:7]))
    tfv = TFIV(min_df=4, max_features=None, strip_accents='unicode', analyzer='word', token_pattern='(?u)\\b\\w+\\b',
               ngram_range=(2, 3), use_idf=1, smooth_idf=1, sublinear_tf=1, stop_words=getStopwords())
    tfv.fit(user_data)
    user_all = tfv.transform(user_data)
    user_feature = []
    for x in user_all:
        user_feature.append(np.array(x.todense())[0].tolist())
    matrix = user_feature[:100]
    pearsonrMatrix = pairwise_distances(matrix, metric="cosine")
    # pearsonrMatrix = np.zeros((100, 100))
    # for i in range(100):
    #     for j in range(100):
    #         pearsonrMatrix[i, j] = pearsonr(matrix[i], matrix[j])[0]
    return pearsonrMatrix


def getPearsonMatrix_3(userLen, articleLen):
    # 基于浏览记录构建相关系数矩阵
    trainData = csv.reader(open("../data/recommender/train/train.csv", "r", encoding="utf-8"))
    trainDataMatrix = np.zeros([userLen, articleLen])
    for line in trainData:
        trainDataMatrix[int(line[0]) - 1, int(line[1]) - 1] = int(line[2])
    pearsonrMatrix = pairwise_distances(trainDataMatrix, metric="cosine")
    return pearsonrMatrix


def getRecordOfNearstOfUsers(userId, pearsonrMatrix, score_record_train):
    """
    @return param: weights 与userId的相似性权重
    @return param: scores 相似性最高的四个用户的评分情况
    """
    # 基于用户+病案首页推荐
    # relations = np.argsort(np.fabs(pearsonrMatrix[userId]))  # 相关系数 ：使用病案首页推荐的结果
    relations = np.argsort(pearsonrMatrix[userId])  # 相关系数 ：使用病案首页推荐的结果
    users = list(relations)  # 根据最接近的n个用户推荐
    users.remove(userId)
    scores = {}
    weights = {}  # 与目标用户的相关系数
    for user in users:
        weights[user] = pearsonrMatrix[userId, user]
        scores[user] = score_record_train[str(user + 1)]
    return weights, scores


def getScoreRecord():
    # 训练集的评分记录
    import csv
    f_train = csv.reader(open("../data/recommender/train/train.csv", "r", encoding="utf-8"))
    f_test = csv.reader(open("../data/recommender/train/test.csv", "r", encoding="utf-8"))
    res_train = {}
    res_test = {}
    for line in f_train:
        if line[0] not in res_train.keys():
            res_train[line[0]] = {}
            res_train[line[0]][line[1]] = line[2]
        else:
            res_train[line[0]][line[1]] = line[2]
    for line in f_test:
        if line[0] not in res_test.keys():
            res_test[line[0]] = {}
            res_test[line[0]][line[1]] = line[2]
        else:
            res_test[line[0]][line[1]] = line[2]
    return res_train, res_test


def getScoreMatrix_1(userLen, articleLen):
    """
    根据病案首页分词情况
    @return param:  originMatrix:用户的实际评分 userLen*articlesLen
                    predMatrix：预测评分：userLen*articlesLen
    """
    score_record_train, score_record_test = getScoreRecord()
    # pearsonrMatrix = getPearsonMatrix_3(userLen, articleLen)
    # pearsonrMatrix = getPearsonMatrix_2() * 0.5 +getPearsonMatrix_3(userLen, articleLen) * 0.5
    pearsonrMatrix = getPearsonMatrix()

    originMatrix = np.zeros((userLen, articleLen))
    predMatrix = np.zeros((userLen, articleLen))
    for userId in range(userLen):
        score = score_record_test[str(userId + 1)]
        weights, scores = getRecordOfNearstOfUsers(userId, pearsonrMatrix, score_record_train)
        res = getPredScores(userId, weights, scores)
        for articleId, articleScore in score.items():
            originMatrix[userId, int(articleId) - 1] = articleScore
        for articleId, articleScore in res.items():
            predMatrix[userId, int(articleId) - 1] = articleScore
    # print(originMatrix)
    # print(predMatrix)
    print(evaluateByRMSE(predMatrix, originMatrix))
    return predMatrix, originMatrix


def getScoreMatrix_2(userLen, articleLen):
    """
    根据浏览记录
    @return param:  originMatrix:用户的实际评分 userLen*articlesLen
                    predMatrix：预测评分：userLen*articlesLen
    """
    score_record_train, score_record_test = getScoreRecord()
    pearsonrMatrix = getPearsonMatrix_3(userLen, articleLen)
    # pearsonrMatrix = getPearsonMatrix_2() * 0.5 +getPearsonMatrix_3(userLen, articleLen) * 0.5
    # pearsonrMatrix = getPearsonMatrix()

    originMatrix = np.zeros((userLen, articleLen))
    predMatrix = np.zeros((userLen, articleLen))
    for userId in range(userLen):
        score = score_record_test[str(userId + 1)]
        weights, scores = getRecordOfNearstOfUsers(userId, pearsonrMatrix, score_record_train)
        res = getPredScores(userId, weights, scores)
        for articleId, articleScore in score.items():
            originMatrix[userId, int(articleId) - 1] = articleScore
        for articleId, articleScore in res.items():
            predMatrix[userId, int(articleId) - 1] = articleScore
    # print(originMatrix)
    # print(predMatrix[20].shape)
    print(evaluateByRMSE(predMatrix, originMatrix))
    return predMatrix, originMatrix


def getScoreMatrix_3(userLen, articleLen):
    """
    基于病案首页
    @return param:  originMatrix:用户的实际评分 userLen*articlesLen
                    predMatrix：预测评分：userLen*articlesLen
    """
    score_record_train, score_record_test = getScoreRecord()
    pearsonrMatrix = getPearsonMatrix_2()
    # pearsonrMatrix = getPearsonMatrix_2() * 0.5 +getPearsonMatrix_3(userLen, articleLen) * 0.5
    # pearsonrMatrix = getPearsonMatrix()

    originMatrix = np.zeros((userLen, articleLen))
    predMatrix = np.zeros((userLen, articleLen))
    for userId in range(userLen):
        score = score_record_test[str(userId + 1)]
        weights, scores = getRecordOfNearstOfUsers(userId, pearsonrMatrix, score_record_train)
        res = getPredScores(userId, weights, scores)
        for articleId, articleScore in score.items():
            originMatrix[userId, int(articleId) - 1] = articleScore
        for articleId, articleScore in res.items():
            predMatrix[userId, int(articleId) - 1] = articleScore
    # print(originMatrix)
    # print(predMatrix[20].shape)
    print(evaluateByRMSE(predMatrix, originMatrix))
    return predMatrix, originMatrix


def getScoreMatrix_4(userLen, articleLen, weight):
    """
    根据浏览记录和病案首页混合加权
    @return param:  originMatrix:用户的实际评分 userLen*articlesLen
                    predMatrix：预测评分：userLen*articlesLen
    """
    score_record_train, score_record_test = getScoreRecord()
    # pearsonrMatrix = getPearsonMatrix_3(userLen, articleLen)
    pearsonrMatrix = getPearsonMatrix_2() * weight + getPearsonMatrix_3(userLen, articleLen) * (1 - weight)
    # pearsonrMatrix = getPearsonMatrix()

    originMatrix = np.zeros((userLen, articleLen))
    predMatrix = np.zeros((userLen, articleLen))
    for userId in range(userLen):
        score = score_record_test[str(userId + 1)]
        weights, scores = getRecordOfNearstOfUsers(userId, pearsonrMatrix, score_record_train)
        res = getPredScores(userId, weights, scores)
        for articleId, articleScore in score.items():
            originMatrix[userId, int(articleId) - 1] = articleScore
        for articleId, articleScore in res.items():
            predMatrix[userId, int(articleId) - 1] = articleScore
    # print(originMatrix)
    print(predMatrix)
    print(evaluateByRMSE(predMatrix, originMatrix))
    return predMatrix, originMatrix


def calculateAUC(predMatrix, originMatrix):
    max = np.max(predMatrix)
    min = np.min(predMatrix)
    flag = (max - min) / 2
    pred = np.zeros(predMatrix.shape)
    origin = np.zeros(originMatrix.shape)
    for i in range(originMatrix.shape[0]):
        for j in range(originMatrix.shape[1]):
            if originMatrix[i, j] == 5 or originMatrix[i, j] == 3:
                origin[i, j] = 1
            elif originMatrix[i, j] == 1:
                origin[i, j] = -1
            if predMatrix[i, j] >= flag:
                pred[i, j] = 1
            elif predMatrix[i, j] < flag:
                pred[i, j] = -1
    FN = 0  # 被判定为负样本，但事实上是正样本
    FP = 0  # 被判定为正样本，但事实上是负样本。
    TN = 0  # 被判定为负样本，事实上也是负样本。
    TP = 0  # 被判定为正样本，事实上也是证样本。
    pred = pred.flatten()
    origin = origin.flatten()
    for i in range(len(pred)):
        if pred[i] == 1 and origin[i] == 1:
            TP += 1
        if pred[i] == 1 and origin[i] == -1:
            FP += 1
        if pred[i] == -1 and origin[i] == -1:
            TN += 1
        if pred[i] == -1 and origin[i] == 1:
            FN += 1
    precesion = TP / (TP + FP)
    print(precesion)


def getRecommendedList(userId,num):
    """
    用于向指定用户生成推荐列表，文章数目和用户数目需要在后期改为自动获取，在调试阶段使用的固定值
    :param userId: 用户ID
    :param num: 返回的文章数目
    :return: 文章ID的集合
    """
    predMatrix, originMatrix = getScoreMatrix_4(100, 761, 0.5) #需要选择使用的推荐规则，这里选择了getScoreMatrix_4()方法
    userScoreList = predMatrix[userId]
    list = np.argsort(-userScoreList)[:num]  # 按照评分降序排列，返回索引，即文章ID
    return list

if __name__ == '__main__':
    arr = np.array([[1, 4, 3], [2, 3, 4], [3, 5, 6]])
    print(np.argsort(arr[0])[:1])
