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

filefolder = r"D:\ExpData\SPE\20250917RenishawRaman\XJJ\20250917\20250722#"
filters = ['.spc', '.wdf']
files = list_dir_files(filefolder, filters)

new_files = []
nums = []
for file in files:
    if "Si_with_EBI" in file and "(532ex_1%" in file:
        # if 'hBN_with_EBI_P_1.txt' in file or "hBN_with_EBI_P_1-1.txt" in file:
        #     continue
        # else:
        new_files.append(file)
    else:
        pass

# print(new_files)
new_files = sort_files(new_files)
nums = range(1, len(new_files)+1, 1)

fig = plt.figure(figsize=(8, 6), dpi=200)
ax = fig.add_subplot(111)
the_graph4(ax, title="Si w/ EBI-532ex_1%")

for num, file in zip(nums, new_files):
    data = read_lines_txt(os.path.join(filefolder, file), separator='\t', skip_lines=1, row_lines_names=None)
    x = np.array(data['data1'])
    y = np.array(data['data2'])
    mask = (500 < x) & (x < 800)
    x, y = x[mask], y[mask]
    print(np.min(x), np.max(x))

    ax.plot(x, y)

plt.tight_layout()
plt.show()