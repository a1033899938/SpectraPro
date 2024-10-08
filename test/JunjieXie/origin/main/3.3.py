"""获取时间"""
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt


if __name__ == '__main__':
    now = QDate.currentDate()
    print(now)
    print(now.toString())
    print(now.toString(Qt.ISODate))
    print(now.toString(Qt.DefaultLocaleLongDate))
    print("-------------------------------------")

    datetime = QDateTime.currentDateTime()
    print(datetime)
    print(datetime.toString())
    print(datetime.toString(Qt.ISODate))
    print(datetime.toString(Qt.DefaultLocaleLongDate))
    print(datetime.toString("yyyy//MM//dd HH:--mm:--ss"))  # 任意组合形式输出时间
    print("-------------------------------------")

    time = QTime.currentTime()
    print(time)
    print(time.toString())
    print(time.toString(Qt.ISODate))
    print(time.toString(Qt.DefaultLocaleLongDate))
