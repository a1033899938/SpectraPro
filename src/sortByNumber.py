"""通过list中的多组数值对list进行排序，在前的数值更优先"""
import copy
import re


class sortFiles:
    def __init__(self, file_names):
        # 通过深复制，确保副本完全独立
        # 列表 (list)、字典 (dict)、集合 (set) 等都是可变对象。
        # 如果你将可变对象传递给函数或类，并在函数或类中修改该对象，那么原始对象也会被修改，因为它们都指向同一个内存位置。
        # 字符串 (str)、整数 (int)、浮点数 (float)、元组 (tuple) 等都是不可变对象。
        # 如果你将不可变对象传递给函数或类，即使在函数或类中尝试修改该对象，原始对象也不会被改变。相反，操作会创建一个新的对象
        self.file_names_sorted = copy.deepcopy(file_names)
        self.sort_files()

    def sort_key(self, filename):
        """定义排序键函数"""
        # 提取文件名中的所有数字（包括整数和浮点数）
        # \d+\.\d+ 匹配浮点数（例如 0.75），\d+ 匹配整数（例如 12、100）
        numbers = re.findall(r'\d+\.\d+|\d+', filename)
        # 将数字从字符串转换为浮点数或整数
        numbers = [float(num) if '.' in num else int(num) for num in numbers]
        return numbers

    def sort_files(self):
        """对文件名列表进行排序"""
        # .sort方法对self.file_names_sorted进行排序
        # 所有元素都传给sort方法
        # 每个元素都调用self.sort_key方法获得numbers返回给sort函数
        # sort通过numbers们，对self.file_names_sorted进行排序
        self.file_names_sorted.sort(key=self.sort_key)


# 测试代码
if __name__ == '__main__':
    # 假设你的文件名列表如下
    file_names = [
        "hBNonNPs-12#-1-100x0.80NA100P10str150gr10s",
        "hBNonNPs-10#-2-200x1.00NA200P20str100gr5s",
        "hBNonNPs-12#-1-100x0.75NA10P10str150gr10s",
        # 更多文件名...
    ]
    # 实例化sortFiles
    sorter = sortFiles(file_names)
    # 访问实例化后的sorter中的属性file_names（即排完序的file_names）
    file_names_sorted = sorter.file_names_sorted

    # file_names_sorted = sortFiles(file_names).file_names_sorted  # 相同效果
    # 打印排序前后的结果
    print("before: ", file_names)
    print("after: ", file_names_sorted)
