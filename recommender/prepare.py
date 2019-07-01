#从数据库加载数据集
from common.exportFromDB import exportToCSV
exportToCSV("recommender_user_info","recommender_user_info")
exportToCSV("user_reading_record","user_reading_record")
exportToCSV("medical_record","medical_record")
