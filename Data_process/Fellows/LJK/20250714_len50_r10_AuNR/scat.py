from src.general.load_data.save_read_data import *
from src.general.figure.set_figure import *

def the_figure(ax):
    """拟合曲线"""
    set_label_and_title(ax, title='', ylabel='Intensity(a.u.)')
    set_spines(ax)
    set_tick(ax)  # Normalized
    set_legend(ax)
    plt.tight_layout()

exp_file = r"D:\FDTDSimFile\NP_scattering\AuNR\wav_ext_scat_abs.npz"
# sim_file = r"D:\FDTDSimFile\NP_scattering\AuNR\len50_r10_AuNR_inCTAB-sim-scat.txt"
sim_file = r"D:\FDTDSimFile\NP_scattering\AuNR\len75_r12.5_AuNR_CTABshell2-sim-scat.txt"

exp_data = np.load(exp_file)
exp_wav = exp_data["wav"]
exp_ext = exp_data["ext"]
exp_scat = exp_data["scat"]
exp_abs = exp_data["abs"]

sim_wav, sim_scat, sim_abs = read_lines_txt(sim_file, skip_lines=1)
sim_wav = np.array(sim_wav)
sim_scat = np.array(sim_scat)
sim_abs = -np.array(sim_abs)
sim_ext = sim_scat + sim_abs
sim_ext = np.array(sim_ext)

fig = plt.figure(figsize=(12, 8), dpi=200)
ax = fig.add_subplot(111)
exps = [exp_scat, exp_abs, exp_ext]
exps_les = ["exp_scat", "exp_abs", "exp_ext"]

sims = [sim_scat, sim_abs, sim_ext]
sims_les = ["sim_scat", "sim_abs", "sim_ext"]

for i, (exp, sim) in enumerate(zip(exps, sims)):
    ax.plot(exp_wav, exp, '-', label=exps_les[i])
    ax.plot(sim_wav, np.array(sim)*1e13*4, '--', label=sims_les[i])

the_figure(ax)
plt.show()
