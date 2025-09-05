"""
Author: Junjie-Xie
Updated: 2025/7/29
Functions: 
"""

def print_level(n, title, msg, delimiter='  '):
    """
    按层级输出格式化信息
    :param n: 层级数（1-3，决定缩进量）
    :param title: 模块标题（将转为大写）
    :param msg: 要输出的具体信息
    :return: 格式化后的字符串
    """

    indent = delimiter * (n - 1)  # 计算缩进量（n=1时无缩进，n=2时1层缩进，以此类推）
    formatted_title = title.upper()  # 标题转为大写
    formatted_msg = f"{indent}| {formatted_title} | {msg}"
    if n == 1:
        formatted_msg = '\n' + formatted_msg
    print(formatted_msg)  # 输出格式化信息
    return formatted_msg

def print_title(title, total_counts=60, delimiter='='):
    # 计算标题的视觉长度
    title_counts = len(title)

    # 确保总长度不会小于标题长度
    if total_counts < title_counts + 10:
        total_counts = title_counts + 10

    # 计算左右分隔符的视觉长度
    left_counts = (total_counts - title_counts) // 2
    right_counts = total_counts - title_counts - left_counts

    # 生成左右分隔符（每个分隔符占1个视觉单位）
    left_delimiter = delimiter * left_counts
    right_delimiter = delimiter * right_counts

    formatted_title = f"\n{left_delimiter}{title}{right_delimiter}"
    print(formatted_title)

def print_content(content, total_counts=60, delimiter1='|', delimiter2=' '):
    content_counts = len(content)

    # 确保总长度不会小于标题长度
    if total_counts < content_counts + 10:
        total_counts = content_counts + 10

    # 计算左右分隔符的视觉长度
    left_counts = (total_counts - content_counts) // 2
    right_counts = total_counts - content_counts - left_counts

    # 生成左右分隔符（每个分隔符占1个视觉单位）
    left_delimiter = delimiter2 * (left_counts - 1)
    right_delimiter = delimiter2 * (right_counts - 1)

    formatted_title = f"{delimiter1}{left_delimiter}{content}{right_delimiter}{delimiter1}"
    print(formatted_title)

if __name__ == "__main__":
    # 所有标题都将保持40个字符的总长度
    print_title("weqwqewqewqe")
    print_content("dsadsaweq")
    print_title("abc")
    print_title("we121rr3tsdgdsg")


