import numpy as np
import matplotlib.pyplot as plt


# 1. 模拟实验数据（可替换为真实数据）
def generate_spectrum(x, temp):
    """模拟不同温度下的光谱数据，返回 Y 轴强度"""
    # 模拟特征峰（可根据真实数据调整）
    peak_ix = np.exp(-(x - 1.4) ** 2 / 0.01) * 10  # IX 峰
    peak_wse2 = np.exp(-(x - 1.6) ** 2 / 0.005) * (20 + 5 * temp)  # WSe2 峰
    peak_ws2 = np.exp(-(x - 1.95) ** 2 / 0.01) * (10 + 2 * temp)  # WS2 峰
    return peak_ix + peak_wse2 + peak_ws2 + np.random.normal(0, 0.5, len(x))


# 2. 创建画布与子图（垂直排布，共享 X 轴）
x = np.linspace(1.3, 2.1, 500)  # X 轴范围（如波长/能量）
temperatures = [293, 233, 173, 143, 83]  # 温度条件
fig, axes = plt.subplots(
    len(temperatures), 1,  # 子图数量=温度数量，垂直排布
    sharex=True,  # 共享 X 轴
    figsize=(6, 8),  # 画布尺寸（可调整）
    gridspec_kw={"hspace": 0.1}  # 减小子图间距
)

# 3. 逐个子图绘制数据
for i, (ax, temp) in enumerate(zip(axes, temperatures)):
    y = generate_spectrum(x, temp)
    ax.plot(x, y, color="black", linewidth=1.2)  # 绘制谱线

    # 标注温度（如 293 K）
    ax.text(
        0.03, 0.9, f"{temp} K",  # 位置：左上方
        transform=ax.transAxes,  # 基于子图的相对坐标
        fontsize=10,
        fontweight="bold"
    )

    # 隐藏顶部/右侧边框，简化样式
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_yticks([])  # 隐藏 Y 轴刻度（若需保留可自定义）

# 4. 统一设置 X 轴（仅最下方子图显示 X 轴）
axes[-1].set_xlabel("Photon Energy (eV)", fontsize=12)  # X 轴标题
axes[-1].set_xlim(1.3, 2.1)  # 统一 X 轴范围

# 5. 手动标注特征峰（类似示例中的 IX、WSe2 等）
# 示例：在第一个子图标注 IX 峰
axes[0].scatter(1.4, generate_spectrum(np.array([1.4]), 293),
                color="red", label="IX", zorder=5)
axes[0].text(1.42, 10, "IX", fontsize=9, color="red")

# 可继续添加其他峰标注（如 WSe2、WS2 等）

# 6. 显示图像
plt.tight_layout()
plt.show()