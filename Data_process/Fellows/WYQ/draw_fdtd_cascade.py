from src.general.load_data.load_data_from_txt import *
import os
from src.general.numerical.edit_data import *
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from src.general.figure.set_figure import *

def the_figure(ax):
    """拟合曲线"""
    # set_label_and_title(ax, title=f'Z轴分布的二维图像', xlabel='X', ylabel='Y', mode='3d')
    # set_spines(ax)
    set_tick(ax, mode='3d')  # Normalized
    # plt.tight_layout()

filefolder = r"D:\FDTDSimFile\cascade\txt"

slices = []
nums = []
size = '120'
for filename in os.listdir(filefolder):
    if size +'nm' in filename:
        if 'x_sub' in filename:
            x_sub = read_2d_array_from_txt(os.path.join(filefolder, filename))
        elif 'y_sub' in filename:
            y_sub = read_2d_array_from_txt(os.path.join(filefolder, filename))
        else:
            print(filename)
            slice = read_2d_array_from_txt(os.path.join(filefolder, filename))
            slices.append(slice)
            # print(np.float64(filename[len("80nm_"):-len(".txt")]))
            nums.append(np.float64(filename[len(size + "nm_"):-len(".txt")]))

print(np.shape(slices))
nums, slices = sort_lists(nums, slices)

volume = np.stack(slices, axis=0)  # 沿axis=0（Z轴）堆叠，形状为 (Z, H, W)
Z, H, W = volume.shape
print(f"堆叠后三维数组形状：{volume.shape}")  # 输出 (5, 100, 100)，即 (Z, H, W)

# 创建3D图形
fig = plt.figure(figsize=(10, 15), dpi=500)
ax = fig.add_subplot(111, projection='3d')

spacing_factor = 10  # 增大此值使间距更大

# 沿Z轴分布并显示每个切片
for z in range(0, Z, 2):
    # 创建网格坐标
    x = x_sub
    y = y_sub
    X, Y = np.meshgrid(x, y)

    z_position = z * spacing_factor

    # 在Z=z位置绘制切片图像
    # ax.contourf(X, Y, volume[z], zdir='z', offset=z_position, cmap='coolwarm', alpha=0.3)
    ax.plot_surface(X, Y, np.full_like(volume[z], z_position),
                    rstride=5, cstride=5,
                    facecolors=cm.coolwarm(volume[z] / np.max(volume)),
                    alpha=0.5, linewidth=0)

# 设置坐标轴标签和范围
ax.set_title(size+"nm", fontsize=25, pad=40)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(np.min(x_sub), np.max(x_sub))
ax.set_ylim(np.min(y_sub), np.max(y_sub))
ax.set_zlim(0, (Z-1) * spacing_factor * 1.05)

ax.autoscale(enable=False, axis='z')

# 设置视角
ax.view_init(elev=20, azim=45)  # 调整视角
ax.set_box_aspect([1, 1, 3])
# ax.set_position([0, 0, 1, 1])
ax.set_zticklabels(nums)
plt.tight_layout()
plt.show()

