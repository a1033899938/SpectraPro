def print_level(n, title, msg):
    """
    按层级输出格式化信息
    :param n: 层级数（1-3，决定缩进量）
    :param title: 模块标题（将转为大写）
    :param msg: 要输出的具体信息
    :return: 格式化后的字符串
    """
    delimiter = '  '  # 每层缩进的分隔符
    indent = delimiter * (n - 1)  # 计算缩进量（n=1时无缩进，n=2时1层缩进，以此类推）
    formatted_title = title.upper()  # 标题转为大写
    formatted_msg = f"{indent}| {formatted_title} | {msg}"
    print(formatted_msg)  # 输出格式化信息
    return formatted_msg

if __name__ == "__main__":
    # 第一级（无缩进）
    print_level(1, "main", "主循环启动...")

    # 第二级（1层缩进）
    print_level(2, "second", "初始化硬件组件")

    # 第三级（2层缩进）
    print_level(3, "third", "LED控制器初始化完成")

    # 自定义标题示例
    print_level(2, "session", "会话1开始执行指令")
