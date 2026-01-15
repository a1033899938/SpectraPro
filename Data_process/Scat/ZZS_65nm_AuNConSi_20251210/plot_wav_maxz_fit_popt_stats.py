from src.general.proc.ProcTrack import *
from Data_process.Scat.ZZS_65nm_AuNConAu_20260108.figure_setting import *

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_circle_20251210\ZZS_65nm_AuNConSi_20251210.h5"
process_types = ["before_achro", "after_achro"]
roots = ["OceanOpticsSpectrometer/20251210/sample1_before_achro_circle",
         "OceanOpticsSpectrometer/20251210/sample1_circle_1"]
colors = [
    "#000000",  # 纯黑
    "#FF0000",  # 正红
    "#00FF00",  # 正绿
    "#0000FF",  # 正蓝
    "#FFFF00",  # 明黄
    "#00FFFF",  # 青色
    "#800080",  # 紫色
    "#FFA500",  # 橙色
    "#808080",  # 深灰
    "#FF69B4",  # 粉色
    "#A52A2A",  # 棕色
    "#228B22"  # 森林绿
]

fig = plt.figure(figsize=(12*3, 8), dpi=200)
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

particles_slopes = [[None for _ in range(10)], [None for _ in range(10)]]
particles_times = [[None for _ in range(10)], [None for _ in range(10)]]
particles_positions = [[] for _ in range(12)]
for iType, (process_type, root, particles_slope, particles_time) in enumerate(zip(process_types, roots, particles_slopes, particles_times)):

    PROC = ProcTrack(filepath, process_type, root)

    tile_keys, full_tile_keys = PROC.get_tile_keys(mask=["Tile_10"])

    for iTile, full_tile_key in enumerate(full_tile_keys):
        particle_keys, full_particle_keys = PROC.get_particle_keys(full_tile_key)

        for iParticle, full_particle_key in enumerate(full_particle_keys):
            stage_position = PROC.get_attrs(full_particle_key, "stage position now")
            particles_positions[iParticle].append(stage_position)

            if iParticle >= 10:
                continue

            """筛选valid的图片"""
            is_valid = PROC.get_attrs(full_particle_key, f"JunProc: is_valid")
            if is_valid:
                fit_popts = PROC.get_attrs(full_particle_key, "JunProc: wav-maxz fit popts")
                slope_section_1 = fit_popts[0][0]
                slope_section_2 = fit_popts[1][0]
                slopes = [slope_section_1, slope_section_2]
                particles_slope[iParticle] = slopes if particles_slope[iParticle] is None else np.vstack([particles_slope[iParticle], slopes])

                norm_required_time = PROC.get_attrs(full_particle_key, "JunProc: wav-maxz norm. total_second(s/nm)")
                particles_time[iParticle] = norm_required_time if particles_time[iParticle] is None else np.vstack([particles_time[iParticle], norm_required_time])
            else:
                # print(full_particle_key)
                pass

"stage position"
for iParticle, particle_positions in enumerate(particles_positions):
    for iPosition, particle_position in enumerate(particle_positions):
        x = particle_position[0]
        y = particle_position[1]
        ax1.scatter(x, y, edgecolor=colors[iParticle], color="none", label=f"p{iParticle}" if iPosition == 0 else None)

image_markers = PROC.proc_tiled_image("/OceanOpticsSpectrometer/20251210/sample1_before_achro_circle/Tile_0", 3)
subimage_origin = PROC.proc_tiled_image(full_tile_key, 0)
subimage_origin = cv2.convertScaleAbs(subimage_origin, alpha=2, beta=0)
ax2.imshow(image_markers)
ax3.imshow(np.array(subimage_origin))
my_stage_position(ax1, title="Stage Position", unit="um")
my_stage_position(ax2, title="Full Image w. Markers", unit="px")
my_stage_position(ax3, title="Sub Image Origin", unit="px")
ax1.set_aspect(ax2.get_aspect())
save_path = os.path.join(os.path.dirname(filepath), fr"Image/tracking_path.png")
fig.savefig(save_path)
plt.close(fig)

points1 = [[],[]]
points2 = [[],[]]
times1 = [[], []]
times2 = [[], []]

for iParticle in range(10):
    for iType in range(2):
        particles_slope = particles_slopes[iType]
        slopes = particles_slope[iParticle]

        particles_time = particles_times[iType]
        times = particles_time[iParticle]

        try:
            for iSection in range(2):
                slope = slopes[:, iSection]

                x = [iParticle for _ in range(len(slope))]
                y = slope
                point = [(x0, y0) for x0, y0 in zip(x, y)]
                if iType == 0:
                    points1[iSection] += point
                else:
                    points2[iSection] += point

                time = times[:, iSection]
                y2 = time
                point2 = [(x0, y0) for x0, y0 in zip(x, y2)]
                if iType == 0:
                    times1[iSection] += point2
                else:
                    times2[iSection] += point2

                # ax.scatter(x, y2, edgecolor=colors[iParticle], color=colors[iParticle] if iType == 1 else "none")
        except Exception as e:
            print(str(e))


"required time"
x = np.arange(0, 10, 1)
y = np.arange(0, 0.2+0.003, 0.003)

fig = plt.figure(figsize=(12*2, 8*2), dpi=200)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
axes = [ax1, ax2, ax3, ax4]

for iSection in range(2):
    for iType in range(2):
        time_2d_map = np.zeros([len(y), len(x)])

        if iType == 0:
            times = times1[iSection]
            ax = ax2
        else:
            times = times2[iSection]
            ax = ax3

        for time in times:
            x0, y0 = time
            idx_y = find_val_idx(y, y0)
            time_2d_map[idx_y, x0] += 1

        ax = axes[iSection*2+iType]
        ax.pcolor(x, y, time_2d_map, cmap="coolwarm")


"slope"
x = np.arange(0, 10, 1)
y = np.arange(0, 0.1+0.001, 0.001)

fig = plt.figure(figsize=(12*2, 8*2), dpi=200)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
axes = [ax1, ax2, ax3, ax4]

for iSection in range(2):
    for iType in range(2):
        slope_2d_map = np.zeros([len(y), len(x)])

        if iType == 0:
            points = points1[iSection]
            ax = ax2
        else:
            points = points2[iSection]
            ax = ax3

        for point in points:
            x0, y0 = point
            idx_y = find_val_idx(y, y0)
            slope_2d_map[idx_y, x0] += 1

        ax = axes[iSection*2+iType]
        ax.pcolor(x, y, slope_2d_map, cmap="coolwarm")
        print(np.sum(slope_2d_map))

fit_section = [[500,  656.3],[656.3,  730.]]
my_wav_maxz_fit_popt_stats(ax1, title="before achro: 500 - 656.3 nm")
my_wav_maxz_fit_popt_stats(ax2, title="after achro: 500 - 656.3 nm")
my_wav_maxz_fit_popt_stats(ax3, title="before achro: 656.3 - 730 nm")
my_wav_maxz_fit_popt_stats(ax4, title="after achro: 656.3 - 730 nm")
save_path = os.path.join(os.path.dirname(filepath), fr"Image/wav_maxz-fit-popts-stats.png")
fig.savefig(save_path)
plt.close(fig)

"required time"
x = np.arange(0, 10, 1)
y = np.arange(0, 0.2+0.003, 0.003)

fig = plt.figure(figsize=(12*2, 8*2), dpi=200)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
axes = [ax1, ax2, ax3, ax4]

for iSection in range(2):
    for iType in range(2):
        time_2d_map = np.zeros([len(y), len(x)])

        if iType == 0:
            times = times1[iSection]
            ax = ax2
        else:
            times = times2[iSection]
            ax = ax3

        for time in times:
            x0, y0 = time
            idx_y = find_val_idx(y, y0)
            time_2d_map[idx_y, x0] += 1

        ax = axes[iSection*2+iType]
        ax.pcolor(x, y, time_2d_map, cmap="coolwarm")

fit_section = [[500,  656.3],[656.3,  730.]]
my_wav_maxz_norm_required_time_stats(ax1, title="before achro: 500 - 656.3 nm")
my_wav_maxz_norm_required_time_stats(ax2, title="after achro: 500 - 656.3 nm")
my_wav_maxz_norm_required_time_stats(ax3, title="before achro: 656.3 - 730 nm")
my_wav_maxz_norm_required_time_stats(ax4, title="after achro: 656.3 - 730 nm")
save_path = os.path.join(os.path.dirname(filepath), fr"Image/wav_maxz-norm_required_time-stats.png")
fig.savefig(save_path)
plt.close(fig)
# plt.show()
# print(particles_slope_AA[1])