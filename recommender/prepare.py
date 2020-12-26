# 从数据库加载数据集
import csv
import random

from common.exportFromDB import exportToCSV

# 导出评分记录和病案首页信息
exportToCSV("user_read_record", "SR")
exportToCSV("user_medical_record", "MR")


# 将SR.csv中的离散用户、文章ID映射到连续区间，并返回映射表
def idMapping():
    pass


# 数据集分割
def dataSplit(factor):
    f_in = csv.reader(open("../data/recommender/SR.csv", "r", encoding="utf-8"))
    train = csv.writer(open("../data/recommender/train.csv", "w", encoding="utf-8", newline=""))
    test = csv.writer(open("../data/recommender/test.csv", "w", encoding="utf-8", newline=""))
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


dataSplit(0.8)

