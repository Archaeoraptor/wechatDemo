# coding=utf-8
import csv

import jieba
from scipy import sparse
import numpy as np
from scipy.stats import pearsonr
from sklearn.feature_extraction.text import TfidfVectorizer as TFIV


def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    print("正在分词")
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = getStopwords()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


def codeMapping():
    """
    文章id映射到连续空间
    """
    out = csv.writer(open("../data/recommender/train/SR.csv", "w", encoding="utf-8", newline=""))
    f_in = csv.reader(open("../data/recommender/process/scoreRecord.csv", "r", encoding="utf-8"))
    map = {}
    index = 1
    for line in f_in:
        if line[2] not in map.keys():
            map[line[2]] = index
            index += 1
        id = map[line[2]]
        out.writerow(line[1:2] + [id] + line[3:])


def userFeature():
    f_in = csv.reader(open("../data/recommender/process/user_100.csv", "r", encoding="utf-8"))
    user_data = []
    for line in f_in:
        user_data.append(" ".join(line[3:6]))
    tfv = TFIV(min_df=2, max_features=None, strip_accents='unicode', analyzer='word', token_pattern='(?u)\\b\\w+\\b',
               ngram_range=(2, 2), use_idf=1, smooth_idf=1, sublinear_tf=1, stop_words=getStopwords())
    tfv.fit(user_data)
    user_all = tfv.transform(user_data)
    user_feature = []
    for x in user_all:
        user_feature.append(np.array(x.todense())[0].tolist())
    pearsonrMatrix = np.zeros((100, 100))
    for i in range(100):
        for j in range(100):
            pearsonrMatrix[i, j] = pearson(user_feature[i], user_feature[j])
    index = 0
    for x in pearsonrMatrix:
        index += 1
        if index == 1:
            xx = np.argsort(np.fabs(x))
            print(xx)
            break


def getFeatureWords():
    #['下叶', '内膜', '横结肠', '肝曲', '肺', '结肠', '前列腺', '肝', '胆管', '直肠', '宫颈', '膀胱', '特指', '造口', '维持性', '躯干', '前', '皮肤感染', '喉', '颈部', '鼻咽', '脓毒症', '关闭', '胆总管', '叶', '治疗', '淋巴结', '升结肠', '贲门', '子宫', '肺炎', '中', '连接处', '乳房', '胃体', '放射治疗', '术后', '甲状腺', '声门', '肺上', '支气管', '乙状结肠', '对症', '恶性肿瘤', '食管', '胃', '手术', '细菌性', '三分之一', '卵巢', '化学治疗', '降', '面部皮肤', '胃窦', '继发']
    # f_in = csv.reader(open("../data/process/user_100.csv", "r", encoding="utf-8"))
    out = open("../data/recommender/process/seg.txt", "r", encoding="utf-8")
    # for line in f_in:
    #     # user_data.append()
    #     str = seg_depart(" ".join(line[3:6]))
    #     print(str)
    #     out.write(str+"\n")
    #     # break
    # out.close()
    lines = out.readlines()
    s = set()
    for line in lines:
        # print(line.strip().split(" "))
        for x in line.strip().split(" "):
            s.add(x)
    return list(s)


def getFeatureMatrix():
    """
    @return param: features
    """
    featurnList = getFeatureWords()
    out = open("../data/recommender/process/seg.txt", "r", encoding="utf-8")
    lines = out.readlines()
    l_x = len(lines)
    l_y = len(featurnList)
    features = np.zeros((l_x,l_y))
    for i in range(l_x):
        s = set(lines[i].strip().split(" "))
        for word in s:
            features[i,featurnList.index(word)] = 1
    return features
    #
    # print(pearson(features[0],features[26]))
    #
    # pearsonrMatrix = np.zeros((100, 100))
    # for i in range(100):
    #     for j in range(100):
    #         pearsonrMatrix[i, j] = pearsonr(features[i], features[j])[0]
    # index = 0
    # for x in pearsonrMatrix:
    #     index += 1
    #     if index == 1:
    #         xx = np.argsort(np.fabs(x))
    #         print(xx)
    #         break


def pearson(p, q):
    # 只计算两者共同有的
    same = 0
    for i in p:
        if i in q:
            same += 1

    n = same
    # 分别求p，q的和
    sumx = sum([p[i] for i in range(n)])
    sumy = sum([q[i] for i in range(n)])
    # 分别求出p，q的平方和
    sumxsq = sum([p[i] ** 2 for i in range(n)])
    sumysq = sum([q[i] ** 2 for i in range(n)])
    # 求出p，q的乘积和
    sumxy = sum([p[i] * q[i] for i in range(n)])
    # print sumxy
    # 求出pearson相关系数
    up = sumxy - sumx * sumy / n
    down = ((sumxsq - pow(sumxsq, 2) / n) * (sumysq - pow(sumysq, 2) / n)) ** .5
    # 若down为零则不能计算，return 0
    if down == 0: return 0
    r = up / down
    return r


def getStopwords():
    stopwords = []
    with open("../data/recommender/process/stopwords.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            stopwords.append(line.strip())
    return stopwords


def getUserArticlesToScore():
    articles = csv.reader(open("../data/recommender/process/article.csv", "r", encoding="utf-8"))
    scores = csv.reader(open("../data/recommender/process/scoreRecord.csv", "r", encoding="utf-8"))
    users = csv.reader(open("../data/recommender/process/user_100.csv", "r", encoding="utf-8"))
    out = csv.writer(open("../data/recommender/train/data_classifier.csv", "w", encoding="utf-8", newline=""))
    dic = {}
    user = {}
    for line in articles:
        if line[0]!="id":
            dic[line[0]] = line[3]
    for line in users:
        userInfo = line[3:7]
        user[line[0]] = userInfo
    for line in scores:
        out.writerow(user[line[1]]+[dic[line[2]]]+[line[3]])


def getAllDiseases():
    path = "../data/classifier/process/all.csv"
    f_in = csv.reader(open(path,"r",encoding="utf-8"))
    s = set()
    for line in f_in:
        if line[6]!="disease":
            s.add(line[6])
    print(s)



if __name__ == '__main__':
    # a = [1,2,3]
    # b = [1,2,3]
    # c = [1,2,3]
    # print(pearson(a,b))
    # print(pearson(a,c))
    # getFeatureMatrix()
    # print(getStopwords())
    # trainDataGenerator()
    pass