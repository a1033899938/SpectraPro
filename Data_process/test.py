import re


def extract_session_cmd(input_str):
    # 正则表达式模式：匹配SESSION:数字;CMD:任意字符;END格式
    # \d+ 匹配一个或多个数字
    # .*? 非贪婪匹配任意字符（直到遇到;END为止）
    pattern = r"SESSION:\d+;CMD:.*?;END"

    # 查找所有匹配的部分
    matches = re.findall(pattern, input_str)

    return matches


# 示例用法
if __name__ == "__main__":
    test_str = "这是一段包含目标内容的文本SESSION:123;CMD:hello world;END这里是其他内容SESSION:456;CMD:test;END结尾部分"

    result = extract_session_cmd(test_str)
    print(result)
    # 输出: ['SESSION:123;CMD:hello world;END', 'SESSION:456;CMD:test;END']
