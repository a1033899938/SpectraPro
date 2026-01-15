"""
Author: Junjie-Xie
Updated: 2025/7/23
Functions: 
"""
from matplotlib import pyplot as plt


class MyColor:
    # 冷色调（20种）- 以蓝、绿、紫等冷色为主
    cold_colors = [
        "#ADD8E6", "#87CEEB", "#87CEFA", "#4169E1", "#00008B",
        "#4B0082", "#3CB371", "#00FF7F", "#98FB98", "#AFEEEE",
        "#40E0D0", "#00FFFF", "#006400", "#6B8E23", "#008080",
        "#778899", "#9370DB", "#D8BFD8", "#800080", "#B0C4DE"
    ]

    # 暖色调（20种）- 以红、橙、黄等暖色为主
    warm_colors = [
        "#FF1493", "#FF4500", "#FF7F50", "#FF0000", "#FF69B4",
        "#FF6347", "#FFA500", "#FFC125", "#FFD700", "#FFFF00",
        "#F5F5DC", "#FAEBD7", "#A0522D", "#8B4513", "#8B4513",
        "#DAA520", "#B22222", "#FF7F50", "#F7DC6F", "#B87333"
    ]

    # 已有的颜色系列
    light_gradient = [
        "#FFFFFF", "#F9F9F9", "#F0F0F0", "#E8E8E8", "#E0E0E0", "#D9D9D9",
        "#D1D1D1", "#C9C9C9", "#C0C0C0", "#B8B8B8", "#B0B0B0", "#A8A8A8",
        "#A0A0A0", "#999999", "#919191", "#898989", "#818181", "#797979",
        "#707070", "#686868", "#606060", "#595959"
    ]

    dark_gradient = [
        "#000000", "#0A0A0A", "#141414", "#1E1E1E", "#282828", "#323232",
        "#3C3C3C", "#464646", "#505050", "#5A5A5A", "#646464", "#6E6E6E",
        "#787878", "#828282", "#8C8C8C", "#969696", "#A0A0A0", "#AAACAA",
        "#B4B4B4", "#BEBEBE", "#C8C8C8", "#D2D2D2"
    ]

    # 新增颜色系列时，只需在这里添加列表即可
    professional = [
        "#2C7FB8", "#E41A1C", "#4DAF4A", "#984EA3", "#FF7F00",
        "#FFFF33", "#A65628", "#F781BF", "#999999", "#1F78B4",
        "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F",
        "#FF7F00", "#CAB2D6", "#6A3D9A", "#FFFF99", "#B15928"
    ]

    vibrant = [
        "#FF3366", "#3366FF", "#33CC99", "#FFCC00", "#9966FF",
        "#FF6666", "#66CCFF", "#FF9900", "#CC66FF", "#66FF66",
        "#FF3300", "#0066FF", "#FFCC33", "#9933FF", "#33FFCC",
        "#CC3300", "#00CCFF", "#FF66B2", "#6633FF", "#33FF66"
    ]

    @classmethod
    def get_color_series(cls, series_name):
        """
        获取整个颜色系列

        参数:
            series_name: 颜色系列名称（类属性名）
        返回:
            该系列的颜色列表
        异常:
            AttributeError: 当系列名称不存在时
        """
        if not hasattr(cls, series_name):
            raise AttributeError(f"颜色系列 '{series_name}' 不存在")

        series = getattr(cls, series_name)
        if not isinstance(series, list):
            raise TypeError(f"颜色系列 '{series_name}' 必须是列表类型")

        return series

    @classmethod
    def get_color(cls, series_name, index):
        """
        获取指定系列中指定索引的颜色

        参数:
            series_name: 颜色系列名称
            index: 颜色索引
        返回:
            对应的颜色值
        异常:
            AttributeError: 系列不存在时
            IndexError: 索引超出范围时
        """
        series = cls.get_color_series(series_name)

        # if not (0 <= index < len(series)):
        #     raise IndexError(
        #         f"颜色系列 '{series_name}' 的索引超出范围（0-{len(series) - 1}）"
        #     )
        index = index % len(series)

        return series[index]


# 使用示例
if __name__ == "__main__":
    # # 获取整个专业色系
    # pro_colors = MyColor.get_color_series("professional")
    #
    # # 获取深色渐变系列的第5个颜色
    # dark_color = MyColor.get_color("dark_gradient", 4)
    #
    # # 新增一个金属色系后直接使用
    # MyColor.metal = ["#D4AF37", "#C0C0C0", "#9E9E9E"]
    # metal_color = MyColor.get_color("metal", 1)

    import numpy as np
    import math
    # colors = [(1,0,0, i) for i in np.arange(0, 1.1, 0.1)]
    colors = plt.get_cmap("Reds")(np.linspace(1, 0.1, 10))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    import numpy as np
    for i in range(10):
        x = np.arange(400, 1001, 200)
        y = np.random.randn(len(x))
        a = ax.plot(x, y, color=colors[i], label="\u03C4")
    ax.legend()
    plt.show()

