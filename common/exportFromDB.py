#从数据库加载数据集
import pymysql
import csv
def exportToCSV(tableName,fileName,index):
    """
    将数据表数据导出到本地csv文件，以便进行算法的训练
    :param tableName: 数据表名
    :param fileName: 目标文件名
    :param index: 开始位置
    :return:
    """
    file = "../data/" + file +".csv"
    f = open(file,"a",newline="",encoding="utf-8")
    writer = csv.writer(f)
    db = pymysql.connect("211.83.111.221:3308", "root", "123456", "xw_utf8mb4")
    cursor = db.cursor()
    begin = index
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


def getLastId(file):
    """

    :param file: 文件名 不需要后缀
    :return: 最后一条数据的 ID
    """
    file = "../data/"+ file +".csv"
    f = open(file,"r",newline="",encoding="utf-8")
    reader = csv.reader(f)
    id = 0
    for line in reader:
        id+=1
    f.close()
    return id



if __name__ == '__main__':
    index = getLastId("user")
    exportToCSV("user","user",index)