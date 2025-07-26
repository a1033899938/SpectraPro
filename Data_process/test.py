import numpy as np
from matplotlib import pyplot as plt

# # 生成示例数据
# a = np.linspace(0, 10, 100)
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(a, a)
#
# # 正确设置坐标轴标签，并调整y轴标签位置
# ax.set_xlabel('x')  # 正确的x轴标签设置方式
# # 通过labelpad参数调整y轴标签位置，值越大越靠上
# ax.set_ylabel('y')  # labelpad为标签与轴的距离（像素）
# ax.yaxis.set_label_coords(0, 1)
# plt.show()

print(np.arange(50, 121, 5))
print(len(np.arange(50, 121, 5)))