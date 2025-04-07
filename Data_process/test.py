import numpy as np
from src.general.edit_data import sort_lists
powers = [3, 2, 1, 5]
ints = [1, 2, 3, 4]
errors = [4, 3, 2, 1]


# zipped_lists = zip(powers, ints, errors)
# sorted_zipped_lists = sorted(zipped_lists, key=lambda x: x[0])
# # 解压缩得到排序后的 list1 和 list2
# powers, ints, errors_now = zip(*sorted_zipped_lists)
powers, ints, errors = sort_lists(powers, ints, errors)
print(type(powers))
print(powers, ints, errors)