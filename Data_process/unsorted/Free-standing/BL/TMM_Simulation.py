import numpy as np

from src.general.figure import set_figure

# file = r"D:\BaiduSyncdisk\Junjie Xie Backup\PPT\2025\开题\1\BL_sim_30d.txt"
file = r"D:\BaiduSyncdisk\Junjie Xie Backup\PPT\2025\开题\1\BL_sim_45d-6450-hole.txt"

data = np.loadtxt(file, delimiter='\t', skiprows=0)
print(np.shape(data))

# 提取角度、波长和吸收值
angle_array = data[:, 0]
wavelength_array = data[:, 1]
absorption = data[:, 2]

# 获取唯一的角度和波长值（假设数据按网格排列）
unique_angles = np.unique(angle_array)
unique_wavelengths = np.unique(wavelength_array)

# 重塑吸收值为矩阵（角度×波长）
n_angles = len(unique_angles)
n_wavelengths = len(unique_wavelengths)

# 检查数据点数量是否匹配
if n_angles * n_wavelengths != len(absorption):
    raise ValueError("数据点数量与角度和波长的组合不匹配")

absorption_matrix = absorption.reshape(n_angles, n_wavelengths)

def the_figure(ax, cbar):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', xlabel='Angle(degree)', ylabel='Energy(eV)', colorbar=cbar, colorbar_label='Intensity(cts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, colorbar=cbar, ticks_xlabel=np.arange(-30, 31, 10), ticks_ylabel=np.arange(1.55, 2.16, 0.15))  # Normalized
    set_figure.set_scientific_y_ticks(ax, cbar, sci_position=(2, 0))
    # ax.invert_yaxis()
    plt.tight_layout()

x = unique_angles
y = unique_wavelengths
y = 1240 / y
print(np.min(y))
print(np.max(y))
z = absorption_matrix

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)

im = ax.pcolor(x, y, np.transpose(z), cmap='viridis')

cbar = fig.colorbar(im)
ax.set_xlim([-30, 30])
the_figure(ax, cbar)

plt.show()
