import numpy as np
import cv2
import matplotlib.pyplot as plt


def match_subarray(large_array, small_array):
    # convert array to float
    large_float = np.float32(large_array)
    small_float = np.float32(small_array)

    # match by template
    result = cv2.matchTemplate(large_float, small_float, cv2.TM_CCOEFF_NORMED)

    # find position of best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # get shape of small array
    small_shape = small_array.shape
    top_left = max_loc
    bottom_right = (top_left[0] + small_shape[1], top_left[1] + small_shape[0])

    return top_left, bottom_right, max_val


def match_and_draw_subarray(large_array, small_array, another_large_array=None, color=255, linewidth=2):
    """Draw matched region by small array. Note: you should add 'plt.show()' manually after this."""
    top_left, bottom_right, match_value = match_subarray(large_array, small_array)
    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    if another_large_array is None:
        matched_region = large_array[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0], :].copy()
        cv2.rectangle(large_array, top_left, bottom_right, color, linewidth)
        ax1.imshow(large_array)
    else:
        matched_region = another_large_array[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0], :].copy()
        cv2.rectangle(another_large_array, top_left, bottom_right, color, linewidth)
        ax1.imshow(another_large_array)

    ax2.imshow(matched_region)
    ax3.imshow(small_array)

    ax1.set_title("Matched Result")
    ax2.set_title("Matched Region")
    ax3.set_title("Under Matched Array")
    return fig
