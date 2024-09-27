import numpy as np


def Scale_up(Min, Max, Mid, min, max):
    scale = (Mid-Min)/(Max-Min)  # scale = (Mid-Min)/(Max-Min) = (mid-min)/(max-min)
    mid = scale*(max-min)+min
    return mid


def transform_position_SpanToLim(x_min, y_min, x_span, y_span):
    x_max = x_min + x_span
    y_max = y_min + y_span
    return x_min, x_max, y_min, y_max


def transform_position_LimToSpan(x_min, x_max, y_min, y_max):
    try:
        x_span = x_max - x_min
        y_span = y_max - y_min
        return x_min, y_min, x_span, y_span
    except Exception as e:
        print(f"Error numerical_transform.transform_position_LimToSpan:\n  |--> {e}")

