#从数据库加载数据集
import pymysql
import csv
def exportToCSV(tableName,file):
    """
    将数据表数据导出到本地csv文件，以便进行算法的训练
    :param tableName: 数据表名
    :param file: 目标文件名
    :return:
    """
    file = "../data/" + file +".csv"
    f = open(file,"w",newline="",encoding="utf-8")
    writer = csv.writer(f)
    db = pymysql.connect("139.224.54.233","root","Asdfghjkl123","xw_utf8mb4")
    cursor = db.cursor()
    begin = 0
    len = 1000
    while True:
        cursor.execute("SELECT * FROM %s LIMIT %s,%s" %(tableName,begin,len))
        data = cursor.fetchall()
        if data:
            for x in data:
                writer.writerow([xx for xx in x])
            begin += len
        else:
            break
    f.close()
    cursor.close()
    db.close()

if __name__ == '__main__':
    exportToCSV("articles","articles")