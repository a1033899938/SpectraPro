"""通过list中的多组数值对list进行排序，在前的数值更优先"""
import copy
import re


def sort_key(filename):
    """定义排序键函数"""
    # 提取文件名中的所有数字（包括整数和浮点数）
    # \d+\.\d+ 匹配浮点数（例如 0.75），\d+ 匹配整数（例如 12、100）
    numbers = re.findall(r'\d+\.\d+|\d+', filename)
    # 将数字从字符串转换为浮点数或整数
    numbers = [float(num) if '.' in num else int(num) for num in numbers]
    return numbers


def sort_files(file_names):
    """对文件名列表进行排序"""
    # 通过深复制确保副本完全独立，避免修改原始列表
    file_names_sorted = copy.deepcopy(file_names)
    # 使用sort方法，传入排序键
    file_names_sorted.sort(key=sort_key)
    return file_names_sorted


# 测试代码
if __name__ == '__main__':
    # 假设你的文件名列表如下
    file_names = [
        "hBNonNPs-2#-1-100x0.80NA100P10str150gr10s",
        "hBNonNPs-10#-2-200x1.00NA200P20str100gr5s",
        "hBNonNPs-2#-1-100x0.75NA10P10str150gr10s",
        # 更多文件名...
    ]
    # 调用排序函数
    file_names_sorted = sort_files(file_names)

    # 打印排序前后的结果
    print("before: ", file_names)
    print("after: ", file_names_sorted)
