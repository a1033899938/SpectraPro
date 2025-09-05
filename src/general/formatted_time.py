"""
Author: Junjie-Xie
Updated: 2025/7/31
Functions: 
"""

import time


def formatted_time(timestamp):
    """
    将时间戳格式化为年月日时分秒.两位小数格式
    适配MicroPython（不依赖strftime）
    """
    # 将时间戳转换为本地时间元组
    # 元组结构：(年, 月, 日, 时, 分, 秒, 星期, 年中天数)
    local_time = time.localtime(timestamp)

    # 提取整数部分时间
    year, month, day = local_time[0], local_time[1], local_time[2]
    hour, minute, second = local_time[3], local_time[4], local_time[5]

    # 提取秒的小数部分（保留2位）
    sec_fraction = int((timestamp - int(timestamp)) * 100)

    # 手动拼接成字符串，确保各字段补零
    return f"{year:04d}-{month:02d}-{day:02d} " + f"{hour:02d}:{minute:02d}:{second:02d}.{sec_fraction:02d}"

if __name__ == "__main__":
    print(formatted_time(time.time()))