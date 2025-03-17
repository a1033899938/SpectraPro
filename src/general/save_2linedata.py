import os
import numpy as np

def save_2line_txt(data1, data2, save_path, save_name):
    save_full_path = os.path.join(save_path, save_name)
    if os.path.exists(save_full_path):
        print("File Exist!")
    else:
        if len(data1) != len(data2):
            print("Length Error!")
            print(f"length of data1: {len(data1)}")
            print(f"length of data2: {len(data2)}")
        else:
            # 打开文件并逐行写入数据
            with open(save_full_path, "w") as f:
                for i in range(len(data1)):
                    f.write('{:} {:}\n'.format(data1[i], data2[i]))  # 每行末尾添加换行符
                f.close()

def read_2line_txt(file_full_path):
    data1 = []
    data2 = []
    with open(file_full_path, "r") as f:
        for line in f.readlines():
            columns = line.strip().split()
            if columns:
                data1.append(float(columns[0]))
                data2.append(float(columns[1]))
    return data1, data2

if __name__ == "__main__":
    # save_path = r''
    # save_name = 'powers_ints.txt'
    # # def save_2line_txt(savepath, savename, x, y):
    # # 要保存的数据
    # data1 = [1, 2, 3]
    # data2 = [4, 5, 6]
    # save_2line_txt(data1, data2, save_path, save_name)

    file_path = r''
    file_name = 'powers_ints.txt'
    read_2line_txt(os.path.join(file_path, file_name))
