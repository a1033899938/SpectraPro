"""打开文件夹，将指定"""
import json
from src.general.h5_tree import *
import h5py

tree_json_path = r'D:\GitProject\SpectraPro\test\JunjieXie\data_processing\20240925\tree.json'
with open(tree_json_path, "r") as f_1:
    tree_data = json.load(f_1)

results = find_items_by_level_and_text(
            tree_data=tree_data,
            level=1,
            text_condition=lambda text: 'Particle' in text and 'Scanner' not in text
                                        and text not in [f'Particle_{i}' for i in range(5)]
        )

h5_path = r"C:\Users\a1033\Desktop\Contemporary\20240620\2024-05-31.h5"
h5_data = h5py.File(h5_path, "r")
print(h5_data)
