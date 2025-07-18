import h5py
from src.general.numerical.edit_data import *

def print_name_in_h5(h5file, dir_name, field_in=None, field_out=None, sort_field=None, print_names=True):
    with h5py.File(h5file, 'r') as f:
        data = f[dir_name]
        sp_names = []
        nums = []
        for key in data.keys():
            if_print = True
            if field_in is None:
                pass
            else:
                if not all(element in key for element in field_in):
                    if_print = False

            if field_out is None:
                pass
            else:
                if not all(element not in key for element in field_out):
                    if_print = False

            if if_print:
                sp_names.append(key)
                if sort_field is not None:
                    idx_start = len(sort_field[0]) if sort_field[0] else None
                    idx_end = -len(sort_field[1]) if sort_field[1] else None
                    nums.append(int(key[idx_start : idx_end]))

        if sort_field is not None:
            nums, sp_names = sort_lists(nums, sp_names)

        if print_names:
            for sp_name in sp_names:
                print(f"\"{sp_name}\",")
    return nums, sp_names


