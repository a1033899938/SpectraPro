"""
Author: Junjie-Xie
Updated: 2025/9/19
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
from src.general.sys.list_dir_files import *
from src.general.numerical.edit_data import *
from src.general.load_data.save_read_data import *
from src.my_style.my_figure import *
from scipy.optimize import curve_fit
# from src.general.numerical.curve_functions import *

filefolder = r"D:\ExpData\SPE\20250917RenishawRaman\XJJ\20250917\20250403#"
file = "hBN_with_EBI_P_9.txt"

fig = plt.figure(figsize=(8, 6*1.3), dpi=200)
ax = fig.add_subplot(111)
fig.suptitle("In-plane vibration of hBN", fontsize=30, fontweight='bold', y=1)
the_graph3(ax)

data = read_lines_txt(os.path.join(filefolder, file), separator='\t', skip_lines=1, row_lines_names=None)
x = np.array(data['data1'])
y = np.array(data['data2'])

mask = (1250 < x) & (x < 1450)
x, y = x[mask], y[mask]

ax.plot(x, y, "o")

def lorentzian(x, A, x0, gamma, C):
    """
    洛伦兹函数
    :param x: 自变量
    :param A: 峰值面积 (幅值=2A/(π*gamma))
    :param x0: 峰值中心位置
    :param gamma: 半高全宽 (FWHM)
    :return: 洛伦兹函数值
    """
    return (A / np.pi) * (0.5 * gamma) / ((x - x0) ** 2 + (0.5 * gamma) ** 2) + C

p0 = [100, 1366, 25, 0]
bounds = [[0, 1250, 0, 0],[1000, 1450, 200, 10000]]
popt, pcov = curve_fit(lorentzian, x, y, p0=p0, bounds=bounds)
A, x0, gamma, C = popt
y_fit = lorentzian(x, A, x0, gamma, C)
ax.plot(x, y_fit, "r-", linewidth=2)
ax.text(1280, 125, f"x0={x0:.1f}", fontsize=20, fontweight="bold", color='red')
ax.text(1280, 120, f"gamma={gamma:.1f}", fontsize=20, fontweight="bold", color='red')
plt.show()