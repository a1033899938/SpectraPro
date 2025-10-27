# """
# Author: Junjie-Xie
# Updated: 2025/10/9
# Functions:
# """
#
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def calculate_intensity(z, z0, zc):
#     """
#     计算不同偏离量下的相对强度
#     z: 偏离焦平面的距离 (μm)
#     z0: 瑞利长度 (μm)，描述激发光斑的轴向分布
#     zc: 收集系统特征长度 (μm)，描述收集效率的轴向变化
#     """
#     # 激发光强贡献（与光斑面积成反比）
#     excitation = 1 / (1 + (z / z0) ** 2)
#     # 收集效率贡献（离焦导致的耦合效率下降）
#     collection = 1 / (1 + (z / zc) ** 2)
#     # 总强度为两者乘积（相对值）
#     total_intensity = excitation * collection
#     return total_intensity
#
#
# # 参数设置（可根据实际系统调整）
# z0 = 5.8  # 瑞利长度 (μm)，假设激光波长532nm，焦斑半径1μm
# zc = 8.0  # 收集系统特征长度 (μm)，与物镜NA和光纤芯径相关
# z_range = np.linspace(-20, 20, 1000)  # 偏离量范围：-20μm 到 +20μm
#
# # 计算强度
# intensity = calculate_intensity(z_range, z0, zc)
#
# # 配置中文显示
# plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
# plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
#
# # 绘图
# plt.figure(figsize=(10, 6))
#
# # 绘制总强度曲线
# plt.plot(z_range, intensity, 'b-', linewidth=2, label='总强度')
#
# # 可选：分别绘制激发光强和收集效率的贡献
# excitation_contribution = 1 / (1 + (z_range / z0) ** 2)
# collection_contribution = 1 / (1 + (z_range / zc) ** 2)
# plt.plot(z_range, excitation_contribution, 'r--', alpha=0.7, label='激发光强贡献')
# plt.plot(z_range, collection_contribution, 'g-.', alpha=0.7, label='收集效率贡献')
#
# # 标记焦平面位置
# plt.axvline(x=0, color='k', linestyle=':', label='焦平面 (z=0)')
#
# # 图形设置
# plt.xlabel('偏离量 z (μm)')
# plt.ylabel('相对强度')
# plt.title('样品偏离焦平面时的强度变化曲线')
# plt.grid(True, alpha=0.3)
# plt.legend()
# plt.xlim(-20, 20)
# plt.ylim(0, 1.05)
#
# plt.tight_layout()
# plt.show()
#
# # 验证对称性：计算相同绝对值的正负偏离量的强度差异
# z_test = [5, 10, 15]
# print("对称性验证（正/负偏离量的强度差异）：")
# for z in z_test:
#     i_pos = calculate_intensity(z, z0, zc)
#     i_neg = calculate_intensity(-z, z0, zc)
#     print(f"z = ±{z}μm: 强度差异 = {abs(i_pos - i_neg):.6f} (理论应为0)")
#
#
print("abc" in "abc")