import h5py
from src.general.h5_methods import *
from src.general.save_figure import save_subfig

file_path = r'C:\Users\a1033\Desktop\Contemporary\20240620\2024-05-31.h5'
f = h5py.File(file_path, "r")

# fig = plt.figure(figsize=(8, 6))
# ax = {}
# node_path = '/ParticleScannerScan_0/Tiles'
# for i, key in enumerate(f[node_path].keys()):
#     try:
#         file = f[f'{node_path}/{key}']
#         # public_attrs = [attr for attr in dir(file.attrs) if not attr.startswith('_')]
#         # print(public_attrs)
#         print(file.attrs.keys())
#         value = np.array(file)
#         ax[i] = fig.add_subplot(1, len(f['/ParticleScannerScan_0/Tiles'].keys()), i + 1)  # 更正 subplot 参数
#         ax[i].imshow(value)
#         set_figure.set_label_and_title(ax[i], title=key, xlabel='position x', ylabel='position y',
#                                        label_fontsize=25, title_fontsize=25,
#                                        label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                        label_fontweight='bold', title_fontweight='bold',
#                                        label_pad=8, title_pad=15)
#         set_figure.set_spines(ax[i], bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
#         set_figure.set_tick(ax[i], xbins=6, ybins=10, fontsize=15, fontweight='bold',
#                             linewidth=3, tick_pad=5, direction='in')
#         set_figure.set_scientific_y_ticks(ax[i], sci_fontsize=15, sci_fontweight='bold')
#
#         """save image data"""
#         sys_path = r'D:\GitProject\SpectraPro\test\data_processing'
#         save_path = os.path.join(sys_path, node_path.lstrip('/'))
#         save_name = f'{key}.npz'
#         save_fullpath = os.path.join(save_path, save_name)
#         dir_path = os.path.dirname(save_fullpath)
#         GeneralMethods.save_image_data_as_npz(ax[i], save_fullpath)
#     except Exception as e:
#         print(f"Error: {e}")

file_large = f['/ParticleScannerScan_0/Tiles/tile_0']
another_large_file = f['/ParticleScannerScan_0/Tiles/tile_with_centers_0']
file_small = f['/Particle_4/NP_image_0']

large_array = np.array(file_large)
another_large_array = np.array(another_large_file)
small_array = np.array(file_small)

match_fig = match_and_draw_subarray(large_array, small_array, another_large_array, (255, 255, 255), 2)
match_fig_save_fullpath = r'D:\GitProject\SpectraPro\tests\pass\temp\tile_0_matched'
save_subfig(match_fig, match_fig_save_fullpath, mode='both', dpi=300)
plt.show()
