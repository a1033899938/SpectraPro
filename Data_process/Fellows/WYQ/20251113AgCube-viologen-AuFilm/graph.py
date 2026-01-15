"""
Author: Junjie-Xie
Updated: 2025/11/13
Functions: 处理光谱数据并可视化（原始数据、归一化后数据对比）
"""
import numpy as np
import matplotlib.pyplot as plt
from src.general.numerical.edit_data import choose_range  # 确保该函数存在

# 数据路径
sp_path = r"D:\ExpData\Fellows\WYQ\txt\80nm-10V6-5.txt"
sub_path = r"D:\ExpData\Fellows\WYQ\txt\80-vio-back.txt"
ref_path = r"D:\ExpData\Fellows\WYQ\txt\ref-center800-2.txt"

# 加载数据并反转（可能是为了修正波长从小到大的顺序）
# 光谱数据：第一列是波长，第二列是信号值
sp_data = np.loadtxt(sp_path, delimiter="\t")
wav1 = sp_data[:, 0][::-1]  # 波长（反转后）
sp = sp_data[:, 1][::-1]    # 信号（反转后）

sub_data = np.loadtxt(sub_path, delimiter="\t")
wav2_raw = sub_data[:, 0][::-1]
sub_raw = sub_data[:, 1][::-1]
# 截取子数据的波长范围（x1到x2）
wav2, sub = choose_range(wav2_raw, sub_raw, x1=249.045898, x2=1138.107666)

ref_data = np.loadtxt(ref_path, delimiter="\t")
wav3 = ref_data[:, 0][::-1]  # 参考数据波长（反转后）
ref = ref_data[:, 1][::-1]   # 参考数据信号（反转后）

# 归一化处理（可能是散射/吸收光谱的标准归一化）
scat_1 = sp / ref    # 用参考数据归一化
scat_1 /= np.max(scat_1)

scat_2 = sp / sub    # 用背景数据归一化
scat_2 = np.where(np.isinf(scat_2), 1, scat_2)
scat_2 = np.where(np.isnan(scat_2), 1, scat_2)
scat_2 /= np.max(scat_2)

sub_origin = sub / ref
sub_origin /= np.max(sub_origin)

# 绘图设置
fig = plt.figure(figsize=(12, 8), dpi=100)
ax1 = fig.add_subplot(111)  # 归一化结果对比
ax2 = ax1
# ax2 = fig.add_subplot(122)  # 原始数据对比

# 修正plot的参数格式（原代码中颜色参数位置错误）
ax1.plot(wav1, scat_1, "-", color="blue", label="sp / ref")    # 注意：波长轴需与数据匹配
ax1.plot(wav1, scat_2, "-", color="red", label="sp / sub")
ax1.plot(wav1, sub_origin, "-", color="purple", label="sub / ref")

ax2.plot(wav1, sp / np.max(sp), "--", color="green", label="norm. sample")
ax2.plot(wav3, ref / np.max(ref), "--", color="gray", label="norm. reference")
ax2.plot(wav2, sub / np.max(sub), "--", color="orange", label="norm. substrate")

# 美化图表
ax1.set_xlabel("Wavelength")
ax1.set_ylabel("Normalized Intensity")
ax1.set_title("Normalized Spectra")
ax1.legend()

ax2.set_xlabel("Wavelength")
ax2.set_ylabel("Intensity")
# ax2.set_title("Raw Spectra")
ax2.legend()

plt.tight_layout()  # 自动调整布局，避免标签重叠
plt.show()