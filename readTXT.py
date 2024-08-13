import os
import sys
import matplotlib.pyplot as plt
import re  # 用于排序
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator # 用于设置tick最大刻度数

filepath = r'C:\Users\a1033\Desktop\Contemporary\240806-240808\20240808'

files = []
filenames = []
for key in os.listdir(filepath):
    # if '.txt' in key.lower() and '12#' in key and '150gr' in key and '60s' in key and 'PurehBN' not in key:
    # if '.txt' in key.lower() and '12#' in key and '100P' in key and '(' not in key:
    # if '.txt' in key.lower() and '15#' in key and '100P' in key:
    if '.txt' in key.lower() and 'wse2' in key.lower():
        filenames.append(key)
        files.append(os.path.join(filepath, key))

files.sort(key=lambda i: int(re.search(r'(\d+)', i).group()) if re.search(r'(\d+)', i) else float('inf'))
filenames.sort(key=lambda i: int(re.search(r'(\d+)', i).group()) if re.search(r'(\d+)', i) else float('inf'))

le = []
for file, filename in zip(files, filenames):
    with open(file, "r") as f:  # 打开文件
        sp = np.loadtxt(f, usecols=(0, 1), skiprows=0)
        print("The file now is: "+file)
        wavelength = sp[:, 0]
        intensity = sp[:, 1]

        try:
            expose_time_pattern = r'(?<=\D)\d+(?=s)'
            matches = re.findall(expose_time_pattern, filename)
            expose_time = matches[-1]
            expose_time = int(expose_time)
            print(expose_time)
            intensity /= expose_time
        except Exception as e:
            print(f"Error normalizing: {e}")
        # 如果wavelength从大到小，就翻转
        if wavelength[1] > wavelength[0]:
            wavelength = wavelength.reverse()
            intensity = intensity.reverse()
        intensity = intensity/max(intensity)
        x = wavelength
        y = intensity
        plt.plot(x, y, linewidth=0.5)
        plt.tick_params(axis='both', which='major', labelsize=8)  # 设置主刻度字体大小
        plt.tick_params(axis='both', which='minor', labelsize=8)  # 设置次刻度字体大小
        plt.xlabel('Wavelength(nm)', fontsize=8)
        plt.ylabel('Normalized its', fontsize=8)
        le.append(filename)
plt.legend(le, loc='upper right')
plt.show()
# particles.sort(key=lambda i: int(re.search(r'(\d+)', i).group()) if re.search(r'(\d+)', i) else float('inf'))
# filepath