# _*_ coding:utf-8 _*_
import csv

import pandas as pd


def getDiseaseOfArticles():
    f_in = csv.reader(open("../data/classifier/process/all.csv", "r", encoding="utf-8"))
    # index,title,label,link,resource,content,disease
    diseases = set()
    for line in f_in:
        if line[0] != "index":
            diseases.add(line[6])
    return diseases
    # res :{"骨肉瘤",
    # "畸胎瘤",
    # "直肠癌",
    # "肾癌",
    # "大肠癌", "食管癌", "甲状腺癌", "慢性粒细胞白血病",
    # "黑色素瘤", "结直肠癌", "乳腺肿瘤", "胃肠道间质瘤",
    # "小细胞肺癌", "胰腺内分泌肿瘤", "子宫肌瘤", "卵巢癌",
    # "浆细胞白血病", "卵巢囊肿", "贲门癌", "弥漫大B细胞淋巴瘤",
    # "骨髓瘤", "神经内分泌瘤", "淋巴癌", "骨巨细胞瘤", "髓母细胞瘤",
    # "骨髓增生异常综合征", "葡萄胎", "宫颈癌前病变", "多发性骨髓瘤",
    # "急性早幼粒细胞白血病", "睾丸癌", "甲状腺肿瘤", "听神经瘤", "肾肿瘤",
    # "乳腺纤维瘤", "肠肿瘤", "脑膜瘤", "骨癌", "甲状腺结节", "软组织肉瘤",
    # "鼻咽癌", "脂肪瘤", "生殖细胞瘤", "膀胱癌", "胃癌", "结肠癌", "椎管内肿瘤",
    # "脑肿瘤", "胰腺癌", "霍奇金淋巴瘤", "急性淋巴细胞白血病", "皮肤癌", "输卵管肿瘤",
    # "神经内分泌肿瘤", "脑癌", "肝癌", "喉癌", "脑动脉瘤", "乳腺癌", "纤维瘤", "胆囊癌",
    # "肺癌", "软骨瘤", "血管瘤", "食道癌", "前列腺癌", "绒毛膜癌", "骨转移癌",
    # "子宫内膜癌", "白血病", "颅咽管瘤", "胶质瘤", "宫颈癌", "肺肿瘤",
    # "口腔癌", "卵巢肿瘤"}
    """
    卵巢癌", "卵巢囊肿" 卵巢肿瘤
    子宫肌瘤 宫颈癌前病变 子宫内膜癌 宫颈癌
    "霍奇金淋巴瘤", "急性淋巴细胞白血病" "淋巴癌"
    直肠癌 大肠癌 结直肠癌 肠肿瘤 结肠癌
   结直肠癌如何处理 弥漫大B细胞淋巴瘤如何处理
   胰腺内分泌肿瘤合并到胰腺癌
   软骨瘤合并到骨癌
   宫颈癌和宫颈癌前病变合并
   神经内分泌瘤和神经内分泌肿瘤合并(如何？)
   肺肿瘤、小细胞肺癌和肺癌合并--->肺肿瘤
   甲状腺肿瘤、甲状腺结节和甲状腺癌合并
   结肠癌和大肠癌合并
   卵巢癌和卵巢肿瘤合并
   食道癌和食管癌 合并-->食道癌




   卵巢囊肿、卵巢癌和卵巢肿瘤合并
   肾肿瘤、肾癌和骨转移癌合并
   乳腺纤维瘤和纤维瘤合并
   绒毛膜癌和葡萄胎  什么意思。。
   白血病、急性淋巴细胞白血病、浆细胞白血病和浆细胞白血病 急性早幼粒细胞白血病  慢性粒细胞白血病 是否合并
   脑癌、脑动脉瘤、脑肿瘤和脑膜癌是否合并
   乳腺肿瘤和乳腺癌是否合并（乳腺肿瘤已录入）
   骨巨细胞瘤和骨癌是否合并（骨癌已经录入）
   脑动脉瘤 未并入
   椎管内肿瘤 未录入
   听神经瘤 未录入
   """


def rebuildArticleData():
    f_in = csv.reader(open("../data/classifier/process/all.csv", "r", encoding="utf-8"))
    out = csv.writer(open("../data/classifier/train/ALL_4.csv", "w", encoding="utf-8", newline=""))
    # index,title(1),label,link,resource,content(5),disease(6)
    for line in f_in:
        if line[0] != "index":  # 标签行
            # 肺肿瘤、小细胞肺癌和肺癌合并--->肺肿瘤
            # 食道癌和食管癌 合并-->食道癌
            if line[6] in ["肺肿瘤", "小细胞肺癌", "肺癌", "肺肿瘤"]:
                out.writerow(["肺部肿瘤", line[1] + line[5]])
            if line[6] in ["肝癌", "肝肿瘤"]:
                out.writerow(["肝部肿瘤", line[1] + line[5]])
            if line[6] in ["食道癌", "食管癌"]:
                out.writerow(["食道肿瘤", line[1] + line[5]])
            if line[6] in ["胃癌", "胃肿瘤"]:
                out.writerow(["胃部肿瘤", line[1] + line[5]])
            if line[6] in ["直肠癌", "大肠癌", "结直肠癌", "肠肿瘤", "结肠癌"]:
                out.writerow(["肠部肿瘤", line[1] + line[5]])
            if line[6] in ["胰腺癌"]:
                out.writerow(["胰腺肿瘤", line[1] + line[5]])
            if line[6] in ["前列腺癌"]:
                out.writerow(["前列腺肿瘤", line[1] + line[5]])
            if line[6] in ["膀胱癌"]:
                out.writerow(["膀胱肿瘤", line[1] + line[5]])
            if line[6] in ["脑癌", "脑肿瘤"]:
                out.writerow(["脑部肿瘤", line[1] + line[5]])
            if line[6] in ["霍奇金淋巴瘤", "淋巴癌", "急性淋巴细胞白血病", "白血病", "急性淋巴细胞白血病", "浆细胞白血病和浆细胞白血病", "急性早幼粒细胞白血病", "慢性粒细胞白血病"]:
                out.writerow(["淋巴肿瘤", line[1]+ line[5]])
            if line[6] in ["乳腺肿瘤", "乳腺癌"]:
                out.writerow(["乳腺肿瘤", line[1]+ line[5]])
            if line[6] in ["子宫肌瘤", "子宫内膜癌", "宫颈癌"]:
                out.writerow(["子宫颈肿瘤", line[1]+ line[5]])
            if line[6] in ["卵巢癌", "卵巢囊肿", "卵巢肿瘤"]:
                out.writerow(["卵巢肿瘤", line[1]+ line[5]])


def processArticleCSV():

    train = pd.read_csv("../data/classifier/train/ALL_4.csv", encoding="utf-8", header=None)
    train.columns = ["disease", "content"]
    disease_list = list(train["disease"])
    disease_num_dic = {}
    for x in disease_list:
        if x in disease_num_dic:
            disease_num_dic[x] += 1
        else:
            disease_num_dic[x] = 1
    print(disease_num_dic)


def articleDataBalance():
    # 调整数据集比例
    pass


if __name__ == '__main__':
    rebuildArticleData()
    processArticleCSV()
