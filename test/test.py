from src.general.load_data.save_read_data import *

filepath = r"D:\ExpData\Fellows\WYQ\20250714_WYQ_SHIN\data\shin-8_0.txt"
data = read_lines_txt(filepath, separator=' ', skip_lines=1, row_lines_names=0)
wav = np.array(data["wav"])
bgd = np.array(data["bgd"])
ref = np.array(data["ref"])
sp = np.array(data["sp"])

scat = (sp - bgd) / (ref - bgd)

from matplotlib import pyplot as plt
fig, ax = plt.subplots()
ax.plot(wav, ref - bgd)
plt.show()
