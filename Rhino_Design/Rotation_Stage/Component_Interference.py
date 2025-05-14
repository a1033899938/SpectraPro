import numpy as np
def spur_gear(m, z):
    """
    计算直齿轮的全齿高和分度圆、齿顶圆、齿根圆、基圆直径
    :param m: 模数
    :param z: 齿数
    :return:
    """
    haa = 1  # 齿顶高系数
    cc = 1  # 顶隙系数
    alpha = np.deg2rad(20)  # 压力角

    # 齿高
    ha = haa * m  # 齿顶高
    hf = (haa + cc) * m  # 齿根高
    h = ha + hf  # 全齿高

    d = m * z
    da = d + 2*ha
    df = d - 2*hf
    db = d*np.cos(alpha)
    return h, d, da, df, db
