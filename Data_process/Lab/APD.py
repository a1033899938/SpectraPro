"""
Author: Junjie-Xie
Updated: 2025/12/29
Functions: 
"""
filepath = r"D:\ExpData\APD_TestLog.txt"
len1 = len("Rate: ")
len2 = len(" counts/s")

num1 = 0
num2 = 0
with open(filepath, "r", encoding="utf-8") as file:
    # 逐行读取文件内容
    for line in file:
        clean_line = line.strip()
        count_str = clean_line[len1:-len2]
        count = float(count_str)
        count = int(count)

        if count % 231 != 0:
            print(count)
            num1 += 1
        else:
            num2 += 1

print(num1, num2)