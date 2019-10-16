#对数据进行预处理
import csv
path = "../data/articles.csv"
writer = csv.writer(open("../data/titles.csv","w",encoding="utf-8",newline=""))
lines = csv.reader(open(path,"r",encoding="utf-8"))
for line in lines:
    writer.writerow([line[-1]])