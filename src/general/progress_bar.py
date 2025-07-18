"""
Author: Junjie-Xie
Updated: 2025/7/18
Functions: 显示进度条
"""
import sys

def print_progress_bar(iteration, total, length=40):
    """
    通过输入当前进度号和总进度数，用打印的方式显示进度条
    :param iteration: 当前进度号
    :param total: 总进度数
    :param length: 进度条的总长度
    :return:
    """
    percent = (iteration / total) * 100
    bar_length = int(length * iteration // total)
    bar = '█' * bar_length + '-' * (length - bar_length)
    sys.stdout.write(f'\r|{bar}| {percent:.2f}%')
    sys.stdout.flush()


if __name__ == '__main__':
    import time
    n = 100
    for i in range(100):
        print_progress_bar(i+1, n)
        time.sleep(0.2)