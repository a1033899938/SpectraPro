# 创建GridSpec对象，更精确地控制布局
from src.general.proc.ProcTrack import *
from Data_process.Scat.ZZS_65nm_AuNConAu_20260108.figure_setting import *
import os

filepath = r"D:\ExpData\NP_scattering_Dispersion\Noise\noise.h5"

window = 15
half_window = window // 2
with h5py.File(filepath, "r") as f:
    keys = list(f.keys())
    keys = sorted(keys, key=lambda k: int(k.split("_")[-1]))

    for key in keys:
        fig = plt.figure(figsize=[12, 8 * 2], dpi=200)
        ax = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        sp_with_noise = f[key]
        wav = np.array(sp_with_noise.attrs["wavelengths"])
        wav_section = np.array(sp_with_noise.attrs["wav_section"])
        noise_section = np.array(sp_with_noise.attrs["noise_section"])
        baseline = np.array(sp_with_noise.attrs["baseline"])
        residual = np.array(sp_with_noise.attrs["residual"])
        noise_wavs = np.array(sp_with_noise.attrs["noise_wavs"])

        ax.plot(wav, np.array(sp_with_noise), color="black", label="sp_with_noise")
        ax2.plot(wav, np.array(sp_with_noise), color="black", linewidth=3, alpha=0.2, label="sp_with_noise")
        ax.plot(wav_section, noise_section, color="red", label="noise_section")

        ax.plot(wav, baseline, color="lightgray", label="baseline")
        ax.plot(wav, residual, color="green", label="residual")
        my_graph(ax, title = "Spectrum Noise Analysis", xtick=np.arange(400, 1101, 200), xlabel="Wavelength (nm)", ylabel="Intensity(cts)")

        noise_idx = [find_val_idx(wav, wav0) for wav0 in noise_wavs]
        mask = np.ones_like(wav)
        mask[noise_idx] = 0

        correct_sp = np.array(sp_with_noise)
        for noise_wav in noise_wavs:
            wav_idx = find_val_idx(wav, noise_wav)

            wav_start_idx = wav_idx-half_window
            wav_end_idx = wav_idx+half_window

            wav_section = wav[wav_start_idx : wav_end_idx]
            mask_section = mask[wav_start_idx : wav_end_idx]
            sp_section = sp_with_noise[wav_start_idx : wav_end_idx]

            sp_section_without_noise = sp_section * mask_section
            this_correct_sp = np.median(sp_section_without_noise)

            correct_sp[wav_idx] = this_correct_sp

        ax2.plot(wav, correct_sp, "black", linewidth=0.5, label="corrected_sp")
        my_graph(ax2, title = "Spectrum Despiking", xtick=np.arange(400, 1101, 200), xlabel="Wavelength (nm)", ylabel="Intensity(cts)")
        save_path = os.path.join(os.path.dirname(filepath),
                                     fr"Image/Spectrum_Despiking//{key}.png")
        fig.savefig(save_path)
        plt.close(fig)
plt.show()