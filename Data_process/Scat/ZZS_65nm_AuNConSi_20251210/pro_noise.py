import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import h5py

# 创建GridSpec对象，更精确地控制布局
from scipy import signal, stats
from scipy.ndimage import gaussian_filter1d
from src.general.proc.ProcTrack import *

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_circle_20251210\ZZS_65nm_AuNConSi_20251210.h5"
savepath = r"D:\ExpData\NP_scattering_Dispersion\Noise\noise.h5"

def do_find(iTile, iParticle, iSp, show, save_h5):
    with h5py.File(filepath, "r") as f:
        folderpath = f"/OceanOpticsSpectrometer/20251210/sample1_circle_1/Tile_{iTile}/65nmAuNConSi_{iParticle}/Spectra/scan_z/"  # sample1_circle_1， sample1_before_achro_circle
        def do_find_noise(sp):
            window_size = 11
            baseline = signal.medfilt(sp, kernel_size=window_size)
            residual = sp - baseline
            # residual[residual < 30] = 0
            residual[residual < 50] = 0
            indice = np.where(residual != 0)[0]
            if indice.size > 0:
                noise_wavs = wav[indice]

                wav_center = noise_wavs[len(noise_wavs) // 2]
                wav_range = [max(346.13427734375, wav_center - 50), min(1121.445249044236, wav_center + 50)]
                wav1, wav2 = wav_range
                wav_idx1 = find_val_idx(wav, wav1)
                wav_idx2 = find_val_idx(wav, wav2)

                wav_section = wav[wav_idx1:wav_idx2]
                sp_section = sp[wav_idx1:wav_idx2]

                return [wav_section, sp_section, baseline, residual, noise_wavs]
            else:
                return None

        if show == "all":
            folder = f[folderpath]
            keys = list(folder.keys())
            keys = sorted(keys, key=lambda k: int(k.split("_")[-1][1:]))

            indice = []
            for i, key in enumerate(keys):
                sp = folder[key]
                wav = np.array(sp.attrs['wavelengths'])
                # 仅获取第一条光谱的bgd, ref, 节省时间
                bgd = np.array(sp.attrs['background'])
                bgd_time = sp.attrs['background_int'] / 1000
                bgd = bgd / bgd_time
                sp_time = sp.attrs['integration_time'] / 1000
                sp = np.array(sp)
                sp = sp / sp_time

                sp = sp - bgd

                ax.plot(wav, sp)

                rst = do_find_noise(sp)
                if rst is not None:
                    wav_section, sp_section, baseline, residual, noise_wavs = rst
                    print(i, key, noise_wavs)
                    indice.append(i)

            return indice

        if show == "single":
            spname = f"scan_z_p{iSp}"
            sppath = f"{folderpath}//{spname}"
            sp = f[sppath]
            wav = np.array(sp.attrs['wavelengths'])
            # 仅获取第一条光谱的bgd, ref, 节省时间
            bgd = np.array(sp.attrs['background'])
            bgd_time = sp.attrs['background_int'] / 1000
            bgd = bgd / bgd_time

            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time

            sp = sp - bgd
            ax.plot(wav, sp, color='black')

            rst = do_find_noise(sp)
            if rst is not None:
                wav_section, sp_section, baseline, residual, noise_wavs = rst
                print(noise_wavs)
                ax2.plot(wav, baseline, color='lightblue', linewidth=5, label='baseline')
                # ax.plot(wav, baseline, color='lightblue', linewidth=5, label='baseline')
                ax2.plot(wav, residual, color='lightgray', linewidth=5, label='residual')

                ax.plot(wav_section, sp_section, color='red')

        if save_h5:
            def do_dataset():
                dset = f.create_dataset(dset_name, data=sp)
                dset.attrs.update({"filepath": filepath,
                                   "spectrum path": sppath,
                                   "wavelengths": wav,
                                   "wav_section": wav_section,
                                   "noise_section": sp_section,
                                   "noise_wavs": noise_wavs,
                                   "baseline": baseline,
                                   "residual": residual,})

            with h5py.File(savepath, 'a') as f:
                keys = list(f.keys())
                keys = sorted(keys, key=lambda x: int(x.split('_')[-1]))

                if keys == []:
                    num_now = -1
                else:
                    num_now = int(keys[-1].split('_')[-1])

                dset_name = f"sp_with_noise_{num_now+1}"

                if dset_name in keys:
                    ok = input(f"文件存在, 输入ok覆盖原文件")
                    if ok == "ok":
                        del f[dset_name]
                        do_dataset()
                        print("覆盖成功")
                    else:
                        print("取消覆盖")
                else:
                    do_dataset()
                    print("创建成功")

fig = plt.figure(figsize=[12, 8 * 2], dpi=200)
ax = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

iTile = 1
iParticle = 4
iSp = 31

show = "all"
# show = "single"
# save_h5 = True

for iTile in range(10):
    for iParticle in range(10):
        # if iTile == 0:
        #     continue
        # elif iTile == 1 and iParticle < 4:
        #     continue

        indice = do_find(iTile, iParticle, iSp=0, show="all", save_h5=False)
        if indice != []:
            for idx in indice:
                do_find(iTile, iParticle, iSp=idx, show="single", save_h5=True)
                fig.canvas.draw()
                fig.canvas.flush_events()
    plt.show()