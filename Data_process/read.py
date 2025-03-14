import numpy as np

# 加载 .npz 文件
data = np.load(r'C:\Users\a1033\Desktop\Contemporary\240806-240808\20240914process\14#\14#.npz')

# 获取数据
for key in data:
    print(f'{key}: {data[key]}')