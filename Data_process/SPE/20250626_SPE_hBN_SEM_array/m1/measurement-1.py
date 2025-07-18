import os.path
import h5py
import matplotlib.pyplot as plt
import numpy as np

from src.general.figure import set_figure
from src.general import choose_range


def the_figure1(ax):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', ylabel='Normalized Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 100))  # Normalized
    # ax.legend()
    # set_figure.set_legend(ax, legend_labels=None)
    plt.tight_layout()

def the_figure2(ax, cbar):
    """拟合曲线"""
    # 设置标题和轴标签
    set_figure.set_label_and_title(ax, title=f'PL mapping-538nm', xlabel='X Position', ylabel='Y Position', colorbar=cbar, colorbar_label='Normalized Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, colorbar=cbar)  # Normalized
    # ax.legend()
    # set_figure.set_legend(ax, legend_labels=None)
    plt.tight_layout()

class IntervalTracker:
    def __init__(self, intervals):
        """
        初始化区间跟踪器

        参数:
        intervals: 区间列表，每个区间是一个元组 (lower_bound, upper_bound)
        """
        self.intervals = intervals
        # 初始化每个区间的使用状态为 False（未使用）
        self.used_status = {idx: False for idx in range(len(intervals))}

    def check_value(self, value):
        """
        检查值是否在未使用的区间内

        参数:
        value: 需要检查的值

        返回:
        如果值在某个未使用的区间内，返回 True 并标记该区间为已使用
        否则返回 False
        """
        for idx, (lower, upper) in enumerate(self.intervals):
            if lower < value <= upper and not self.used_status[idx]:
                self.used_status[idx] = True  # 标记区间为已使用
                return True
        return False

datapath1 = r"D:\ExpData\SPE\20250626_SPE_hBN_SEM_array\measurement-1.h5"

keys = ['hBN_afterSEM_mapping_450ex-200uW_0',
        'hBN_afterSEM_mapping_450ex-500uW_0',
        'hBN_afterSEM_mapping_450ex-500uW-hazyspot_0',
        'hBN_afterSEM_mapping_450ex-500uW-spot1_0',
        'hBN_afterSEM_mapping_450ex-500uW-spot2_0',
        'hBN_afterSEM_mapping_450ex-500uW-spot1_1',
        'hBN_after_SEM_array_point-1_0',
        'hBN_after_SEM_array_point-2_450ex_2mW_0']

intervals = [
    (240, 500),
    (200, 240),
    (150, 200),
    (100, 150),
    (50, 100),
    (0, 20)
]
tracker = IntervalTracker(intervals)

"""fig0"""
with h5py.File(datapath1, "r") as f:
    mapping_name = keys[4]
    data = f['OceanOpticsSpectrometer'][mapping_name]
    row_keys = data.keys()
    row1_key = list(data.keys())[0]
    row1 = data[row1_key]
    column_keys_of_row1 = row1.keys()


    bgd = np.array(data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['background'])
    bgd_time = data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['background_int'] / 1000
    wav = np.array(data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['wavelengths'])
    bgd = bgd / bgd_time
    mapping_range = [len(row_keys), len(column_keys_of_row1)]
    mapping = np.zeros([mapping_range[0], mapping_range[1]])

    peak_idx = np.argmin(np.abs(wav - 538))

    fig1 = plt.figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(111)

    for i in range(mapping_range[0]-1):
        parent_key = f"x-{i}"
        for j in range(mapping_range[1]):
            print(f"i now: {i}, j now: {j}")
            child_key = f"{mapping_name[:-2]}-x{i}-y{j}"
            sp = data[f"{parent_key}/{child_key}"]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd
            # print(sp)
            x, y = choose_range(wav, sp, min_val=400, max_val=900)
            # y = y / np.max(y)
            # ax1.plot(x, y)

            # 0
            # if np.max(y) > 320 and not has_larger_than_320:
            #     ax1.plot(x, y)
            #     has_larger_than_320 = True
            # elif np.max(y) < 320 and np.max(y) > 300 and not has_larger_than_300:
            #     ax1.plot(x, y)
            #     has_larger_than_300 = True
            # elif np.max(y) < 300 and np.max(y) > 200 and not has_larger_than_200:
            #     ax1.plot(x, y)
            #     has_larger_than_200 = True
            # elif np.max(y) < 200 and np.max(y) > 100 and not has_larger_than_100:
            #     ax1.plot(x, y)
            #     has_larger_than_100 = True
            # elif np.max(y) < 100 and np.max(y) > 50 and not has_larger_than_50:
            #     ax1.plot(x, y)
            #     has_larger_than_50 = True
            # elif np.max(y) <= 20 and not has_smaller_than_20:
            #     ax1.plot(x, y)
            #     has_smaller_than_20 = True

            # 4
            # if sp[peak_idx] < 500 and sp[peak_idx] > 250 and not has_larger_than_250:
            #     ax1.plot(x, y)
            #     has_larger_than_250 = True
            # elif sp[peak_idx] < 250 and sp[peak_idx] > 200 and not has_larger_than_200:
            #     ax1.plot(x, y)
            #     has_larger_than_200 = True
            # elif sp[peak_idx] < 200 and sp[peak_idx] > 150 and not has_larger_than_150:
            #     ax1.plot(x, y)
            #     has_larger_than_150 = True
            # elif sp[peak_idx] < 150 and sp[peak_idx] > 100 and not has_larger_than_100:
            #     ax1.plot(x, y)
            #     has_larger_than_100 = True
            # elif sp[peak_idx] < 100 and sp[peak_idx] > 50 and not has_larger_than_50:
            #     ax1.plot(x, y)
            #     has_larger_than_50 = True
            # elif sp[peak_idx] <= 20 and not has_smaller_than_20:
            #     ax1.plot(x, y)
            #     has_smaller_than_20 = True
            result = tracker.check_value(sp[peak_idx])
            if result:
                ax1.plot(x, y)

            mapping[i][j] = np.max(sp[peak_idx - 5:peak_idx + 5])

ax1.axvline(x=537.8, color='blue', linestyle='--', linewidth=1.5, alpha=0.7)  # 蓝色虚线
ax1.axvline(x=6, color='green', linestyle='-.', linewidth=3, alpha=0.5)    # 绿色点划线
ax1.axvline(x=8, color='#FF8C00', linestyle=':', linewidth=2, alpha=0.9)   # 橙色点线
the_figure1(ax1)
# np.save(os.path.join(os.path.dirname(datapath1), fr'm1\mapping_5.npy'), mapping_5)

# save_fig = 0
# mapping_5 =np.load(os.path.join(os.path.dirname(datapath1), fr'm1\mapping_5.npy'))
mapping_range = [mapping.shape[0], mapping.shape[1]]

fig2 = plt.figure(figsize=(8, 6))
ax2 = fig2.add_subplot(111)
x = range(mapping_range[0])
y = range(mapping_range[1])
X, Y = np.meshgrid(x, y)
print(f"shape x: {np.shape(X)}")
print(f"shape y: {np.shape(Y)}")
Z = mapping
Z = Z / np.max(Z)
# Z = np.log(Z)
im = ax2.pcolor(X, Y, np.transpose(Z), cmap='viridis')
cbar = plt.colorbar(im)

the_figure2(ax2, cbar)
plt.show()