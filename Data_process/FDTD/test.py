import lumapi
import numpy as np
import matplotlib.pyplot as plt

# 使用 lumapi.open() 打开 Lumerical FDTD 并保持窗口打开
fdtd = lumapi.open("fdtd")  # 如果没有打开的会话，会创建一个新的

# 确保清除现有内容
fdtd.eval("deleteall;")  # 替代旧的 deleteall() 方法


# 设置计算参数
lambda_range = np.linspace(300e-9, 1100e-9, 500)
c = 2.99792458e8
f_range = c / lambda_range

# 获取金的折射率数据
au_index = fdtd.getfdtdindex("Au (Gold) - CRC", f_range, np.min(f_range), np.max(f_range))

# 计算反射和透射
stackRT_result = fdtd.stackrt(np.transpose(au_index), np.array([10e-9]), f_range)

# 保存项目以便在 Lumerical 中查看
fdtd.save("Gold_Film_Analysis.fsp")

# 可视化结果（使用 matplotlib 或 Lumerical 内置绘图）
fig, ax = plt.subplots()
ax.plot(lambda_range * 1e9, stackRT_result["Ts"], label="Transmission")
ax.set_xlabel("Wavelength [nm]")
ax.set_ylabel("Transmission")
ax.legend()
plt.show()

# 暂停脚本执行，保持 Lumerical 窗口打开
input("Press Enter to close Lumerical...")

# 关闭 Lumerical（如果需要）
# fdtd.close()