import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 创建数据
x = np.linspace(0, 10, 100)  # x 轴数据
y_values = np.linspace(0, 5, 10)  # y 轴分布的不同曲线

# 创建一个空的 z 值列表
z_values = []

# 生成不同的 z 值曲线（例如正弦波）
for i, y in enumerate(y_values):
    z = np.sin(x + y) * (1 + 0.1 * y)  # 每条曲线的 z 值
    z_values.append(z)

# 创建三维图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制每条曲线
for i, y in enumerate(y_values):
    ax.plot(x, np.full_like(x, y), z_values[i], label=f'y={y:.1f}')

# 设置标签
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_zlabel('Z轴')

# 添加图例
ax.legend()

# 显示图形
plt.show()