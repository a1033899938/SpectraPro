from scipy.optimize import curve_fit
from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *

def triple_peaks_fitting(x, y, ax=None, if_x_unit_energy=False):
    fitting_paras = {}

    if not if_x_unit_energy:
        p0 = [100, 537, 6,
              100, 550, 6,
              10, 577, 6]

        bounds = ([0, 527, 5,
                   0, 540, 5,
                   0, 567, 5],
                  [100000, 547, 10,
                   100000, 560, 15,
                   100000, 587, 15])
    else:
        p0 = [1, 2.31, 0.026,
              1, 2.26, 0.026,
              1, 2.15, 0.026]

        bounds = ([0, 2.28, 0.01,
                   0, 2.22, 0.01,
                   0, 2.1, 0.01],
                  [1e5, 2.35, 0.1,
                   1e5, 2.28, 0.1,
                   1e5, 2.19, 0.1])

    if_fit_success = False
    boundary_warnings = []  # 存储边界警告信息
    try:
        # 选择用于拟合的数据波段
        popt, pcov = curve_fit(lorentzian_2_plus_gaussian_1, x, y, p0=p0, bounds=bounds)
        A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt

        # 检测参数是否达到边界（添加容差1e-6避免浮点数精度误差）
        TOL = 1e-6
        param_names = ["A1", "x1", "gamma1", "A2", "x2", "gamma2",
                       "A3", "x3", "gamma3"]

        for i, (param, name) in enumerate(zip(popt, param_names)):
            if param <= bounds[0][i] + TOL:
                boundary_warnings.append(f"参数 {name} 达到下界: {param:.6f} (下界={bounds[0][i]})")
            elif param >= bounds[1][i] - TOL:
                boundary_warnings.append(f"参数 {name} 达到上界: {param:.6f} (上界={bounds[1][i]})")

        print(f'拟合结果: '
              f'A1 = {A1:.1f}, mu1 = {x1:.1f}, sigma1 = {gamma1:.1f}',
              f'A2 = {A2:.1f}, mu2 = {x2:.1f}, sigma2 = {gamma2:.1f}',
              f'A3 = {A2:.1f}, mu3 = {x3:.1f}, sigma3 = {gamma3:.1f}')

        # 打印边界警告（如果有）
        if boundary_warnings:
            print("\n警告：以下参数达到边界，拟合结果可能不可靠：")
            for warning in boundary_warnings:
                print(f"  - {warning}")
        else:
            if_fit_success = True
        print("END===========================================")
    except:
        A1, x1, gamma1 = [p0[0], p0[1], p0[2]]
        print("拟合失败，用预测值代替拟合参数")

    mag = (A1 / np.pi) / (gamma1 / 2)
    cw = x1
    linewidth = gamma1
    fitting_paras["mag"] = mag
    fitting_paras["cw"] = cw
    fitting_paras["linewidth"] = linewidth

    if ax is not None:
        y_fit = lorentzian_2_plus_gaussian_1(x, *popt)
        y_fit1 = lorentzian(x, A1, x1, gamma1)
        y_fit2 = gaussian(x, A2, x2, gamma2)
        y_fit3 = lorentzian(x, A3, x3, gamma3)
        ax.plot(x, y_fit, 'r-', label='Global Lorentzian-Gaussian Fit')
        ax.plot(x, y_fit1, 'b--', label='Peak 1 (Lorentzian Component)')
        ax.plot(x, y_fit2, 'g--', label='Peak 1 (Gaussian  Component)')
        ax.plot(x, y_fit3, 'm--', label='Peak 3 (Lorentzian Component)')
    return fitting_paras

def quatra_peaks_fitting(x, y, ax=None, maxfev=800, if_x_unit_energy=False):
    def quatra_peaks(x, A1, x1, gamma1, A2, x2, gamma2, RatioA_23, x3, gamma3, A4, x4, gamma4):
        A3 = A2*RatioA_23
        peaks = triple_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3)
        peak4 = gaussian(x, A4, x4, gamma4)
        return peaks+peak4
    fitting_paras = {}

    if not if_x_unit_energy:
        p0 = [100, 537, 6,
              100, 550, 6,
              1, 577, 6,
              10, 550, 100]

        bounds = ([0, 527, 0,
                   0, 540, 6,
                   0.1, 567, 0.3,
                   0, 520, 20],
                  [100000, 547, 10,
                   100000, 560, 20,
                   10, 587, 20,
                   100000, 700, 300])
    else:
        p0 = [1, 2.31, 0.026,
              1, 2.26, 0.026,
              1, 2.15, 0.026,
              1, 2.26, 0.1]

        bounds = ([0, 2.28, 0.01,
                   0, 2.22, 0.01,
                   0.1, 2.1, 0.01,
                   0, 2.1, 0.08],
                  [1e5, 2.35, 0.05,
                   1e5, 2.28, 0.1,
                   10, 2.19, 0.07,
                   1e5, 2.3, 0.2])

    if_fit_success = False
    boundary_warnings = []  # 存储边界警告信息
    try:
        # 选择用于拟合的数据波段
        popt, pcov = curve_fit(quatra_peaks, x, y, p0=p0, bounds=bounds, maxfev=maxfev, ftol=1e-10, xtol=1e-10)
        # ftol：阈值--两次迭代之间的残差变化
        # xtol：阈值--参数的相对误差
        A1, x1, gamma1, A2, x2, gamma2, RatioA_23, x3, gamma3, A4, x4, gamma4 = popt

        # 计算由比例确定的参数
        A3 = A2 * RatioA_23  # 从 RatioA_23 计算 A3

        # 检测参数是否达到边界（添加容差1e-6避免浮点数精度误差）
        TOL = 1e-6
        param_names = ["A1", "x1", "gamma1", "A2", "x2", "gamma2",
                       "RatioA_23", "x3", "gamma3", "A4", "x4", "gamma4"]

        for i, (param, name) in enumerate(zip(popt, param_names)):
            if param <= bounds[0][i] + TOL:
                boundary_warnings.append(f"参数 {name} 达到下界: {param:.6f} (下界={bounds[0][i]})")
            elif param >= bounds[1][i] - TOL:
                boundary_warnings.append(f"参数 {name} 达到上界: {param:.6f} (上界={bounds[1][i]})")

        # 格式化并打印拟合结果（保留两位小数）
        print(f'拟合结果:')
        print(f'  峰1 (Lorentzian): A1 = {A1:.2f}, μ1 = {x1:.2f}, γ1 = {gamma1:.2f}')
        print(f'  峰2 (lorentzian):   A2 = {A2:.2f}, μ2 = {x2:.2f}, γ2 = {gamma2:.2f}')
        print(f'  峰3 (Lorentzian): A3 = {A3:.2f}, μ3 = {x3:.2f}, γ3 = {gamma3:.2f} (由比例确定)')
        print(f'  峰4 (gaussian): A4 = {A4:.2f}, μ4 = {x4:.2f}, σ2 = {gamma4:.2f}')
        print(f'  比例参数: RatioA_23 = {RatioA_23:.2f}')

        # 打印边界警告（如果有）
        if boundary_warnings:
            print("\n警告：以下参数达到边界，拟合结果可能不可靠：")
            for warning in boundary_warnings:
                print(f"  - {warning}")
        else:
            if_fit_success = True
        print("END===========================================")
    except:
        A1, x1, gamma1 = [p0[0], p0[1], p0[2]]
        print("拟合失败，用预测值代替拟合参数")

    mag1 = (A1 / np.pi) / (gamma1 / 2)
    mag2 = (A2 / np.pi) / (gamma2 / 2)
    mag3 = (A3 / np.pi) / (gamma3 / 2)
    mag4 = A4
    gaussian_fwhm = 2.3548 * gamma4

    fitting_paras = {
        # 峰1（洛伦兹）
        "peak1": {"A": A1, "center": x1, "fwhm": gamma1, "magnitude": mag1},
        # 峰2（洛伦兹）
        "peak2": {"A": A2, "center": x2, "fwhm": gamma2, "magnitude": mag2},
        # 峰3（洛伦兹，由峰2比例推导）
        "peak3": {"A": A3, "center": x3, "fwhm": gamma3, "magnitude": mag3},
        # 峰4（高斯）
        "peak4": {"A": A4, "center": x4, "sigma": gamma4, "fwhm": gaussian_fwhm, "magnitude": mag4},  # 高斯半高宽≈2.3548*sigma
        "fit_success": if_fit_success  # 拟合状态标记
    }

    if ax is not None:
        y_fit = quatra_peaks(x, *popt)
        y_fit1 = lorentzian(x, A1, x1, gamma1)
        y_fit2 = lorentzian(x, A2, x2, gamma2)
        y_fit3 = lorentzian(x, A3, x3, gamma3)
        y_fit4 = gaussian(x, A4, x4, gamma4)

        ax.plot(x, y_fit, 'r--', label='Global Lorentzian-Gaussian Fit')
        ax.plot(x, y_fit1, 'b--', label='Peak 1 (Lorentzian Component)')
        ax.plot(x, y_fit2, 'g--', label='Peak 1 (Lorentzian  Component)')
        ax.plot(x, y_fit3, 'm--', label='Peak 3 (Lorentzian Component)')
        ax.plot(x, y_fit4, 'y--', label='Peak 4 (Gaussian Component)')
    return fitting_paras

def quatra_peaks_fitting2(x, y, ax=None, maxfev=800, if_x_unit_energy=False):
    def quatra_peaks(x, A1, x1, gamma1, A2, x2, gamma2, RatioA_23, x3, gamma3, RatioA_24, x4, gamma4):
        A3 = A2*RatioA_23
        A4 = A2*RatioA_24
        peaks = triple_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3)
        peak4 = lorentzian(x, A4, x4, gamma4)
        return peaks+peak4
    fitting_paras = {}

    if not if_x_unit_energy:
        p0 = [100, 537, 6,
              100, 550, 6,
              1, 577, 6,
              10, 550, 100]

        bounds = ([0, 527, 0,
                   0, 540, 6,
                   0.1, 567, 0.3,
                   0, 520, 20],
                  [100000, 547, 10,
                   100000, 560, 20,
                   10, 587, 20,
                   100000, 700, 300])
    else:
        p0 = [1, 2.31, 0.026,
              1, 2.26, 0.026,
              1, 2.15, 0.026,
              1, 2, 0.026]

        bounds = ([0, 2.28, 0.01,
                   0, 2.22, 0.01,
                   0.1, 2.1, 0.01,
                   0, 1.96, 0.01],
                  [1e5, 2.35, 0.05,
                   1e5, 2.28, 0.1,
                   1, 2.19, 0.07,
                   1, 2.04, 0.07])

    if_fit_success = False
    boundary_warnings = []  # 存储边界警告信息
    try:
        # 选择用于拟合的数据波段
        popt, pcov = curve_fit(quatra_peaks, x, y, p0=p0, bounds=bounds, maxfev=maxfev, ftol=1e-10, xtol=1e-10)
        # ftol：阈值--两次迭代之间的残差变化
        # xtol：阈值--参数的相对误差
        A1, x1, gamma1, A2, x2, gamma2, RatioA_23, x3, gamma3, RatioA_24, x4, gamma4 = popt

        # 计算由比例确定的参数
        A3 = A2 * RatioA_23  # 从 RatioA_23 计算 A3
        A4 = A2 * RatioA_24

        # 检测参数是否达到边界（添加容差1e-6避免浮点数精度误差）
        TOL = 1e-6
        param_names = ["A1", "x1", "gamma1", "A2", "x2", "gamma2",
                       "RatioA_23", "x3", "gamma3", "RatioA_24", "x4", "gamma4"]

        for i, (param, name) in enumerate(zip(popt, param_names)):
            if param <= bounds[0][i] + TOL:
                boundary_warnings.append(f"参数 {name} 达到下界: {param:.6f} (下界={bounds[0][i]})")
            elif param >= bounds[1][i] - TOL:
                boundary_warnings.append(f"参数 {name} 达到上界: {param:.6f} (上界={bounds[1][i]})")

        # 格式化并打印拟合结果（保留两位小数）
        print(f'拟合结果:')
        print(f'  峰1 (Lorentzian): A1 = {A1:.2f}, μ1 = {x1:.2f}, γ1 = {gamma1:.2f}')
        print(f'  峰2 (lorentzian):   A2 = {A2:.2f}, μ2 = {x2:.2f}, γ2 = {gamma2:.2f}')
        print(f'  峰3 (Lorentzian): A3 = {A3:.2f}, μ3 = {x3:.2f}, γ3 = {gamma3:.2f} (由比例确定)')
        print(f'  峰4 (gaussian): A4 = {A4:.2f}, μ4 = {x4:.2f}, σ2 = {gamma4:.2f}')
        print(f'  比例参数: RatioA_23 = {RatioA_23:.2f}, RatioA_24 = {RatioA_24:.2f}')

        # 打印边界警告（如果有）
        if boundary_warnings:
            print("\n警告：以下参数达到边界，拟合结果可能不可靠：")
            for warning in boundary_warnings:
                print(f"  - {warning}")
        else:
            if_fit_success = True
        print("END===========================================")
    except:
        A1, x1, gamma1 = [p0[0], p0[1], p0[2]]
        print("拟合失败，用预测值代替拟合参数")

    mag1 = (A1 / np.pi) / (gamma1 / 2)
    mag2 = (A2 / np.pi) / (gamma2 / 2)
    mag3 = (A3 / np.pi) / (gamma3 / 2)
    mag4 = (A4 / np.pi) / (gamma4 / 2)

    fitting_paras = {
        # 峰1（洛伦兹）
        "peak1": {"A": A1, "center": x1, "fwhm": gamma1, "magnitude": mag1},
        # 峰2（洛伦兹）
        "peak2": {"A": A2, "center": x2, "fwhm": gamma2, "magnitude": mag2},
        # 峰3（洛伦兹）
        "peak3": {"A": A3, "center": x3, "fwhm": gamma3, "magnitude": mag3},
        # 峰4（洛伦兹）
        "peak4": {"A": A4, "center": x4, "fwhm": gamma4, "magnitude": mag4},
        "fit_success": if_fit_success  # 拟合状态标记
    }

    if ax is not None:
        y_fit = quatra_peaks(x, *popt)
        y_fit1 = lorentzian(x, A1, x1, gamma1)
        y_fit2 = lorentzian(x, A2, x2, gamma2)
        y_fit3 = lorentzian(x, A3, x3, gamma3)
        y_fit4 = lorentzian(x, A4, x4, gamma4)

        ax.plot(x, y_fit, 'r--', label='Global Lorentzian-Gaussian Fit')
        ax.plot(x, y_fit1, 'b--', label='Peak 1 (Lorentzian Component)')
        ax.plot(x, y_fit2, 'g--', label='Peak 1 (Lorentzian  Component)')
        ax.plot(x, y_fit3, 'm--', label='Peak 3 (Lorentzian Component)')
        ax.plot(x, y_fit4, 'y--', label='Peak 4 (Lorentzian Component)')
    return fitting_paras

def penta_peaks_fitting(x, y, ax=None):
    """
    五峰拟合函数：3个洛伦兹峰 + 2个高斯峰（峰3由峰2比例推导）
    结构：峰1（洛伦兹）、峰2（洛伦兹）、峰3（洛伦兹，比例推导）、峰4（高斯）、峰5（高斯）
    """
    def penta_peaks(x, A1, x1, gamma1, A2, x2, gamma2,
                   RatioA_23, x3, RatioGamma_23,
                   A4, x4, gamma4, A5, x5, gamma5):
        """五峰模型：前3个洛伦兹峰（峰3比例推导）+ 后2个高斯峰"""
        # 峰3参数由峰2比例计算
        A3 = A2 * RatioA_23  # 峰3振幅 = 峰2振幅 × 比例系数
        gamma3 = gamma2 * RatioGamma_23  # 峰3半高宽 = 峰2半高宽 × 比例系数
        # 前3个洛伦兹峰叠加
        peaks_lorentz = triple_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3)
        # 2个高斯峰
        peak4 = gaussian(x, A4, x4, gamma4)
        peak5 = gaussian(x, A5, x5, gamma5)
        return peaks_lorentz + peak4 + peak5

    # 初始化拟合参数字典（存储所有峰参数）
    fitting_paras = {
        "peak1": {"A": None, "center": None, "fwhm": None, "magnitude": None},  # 洛伦兹
        "peak2": {"A": None, "center": None, "fwhm": None, "magnitude": None},  # 洛伦兹
        "peak3": {"A": None, "center": None, "fwhm": None, "magnitude": None,
                 "ratio_A": None, "ratio_fwhm": None},  # 洛伦兹（比例推导）
        "peak4": {"A": None, "center": None, "sigma": None, "fwhm": None, "magnitude": None},  # 高斯
        "peak5": {"A": None, "center": None, "sigma": None, "fwhm": None, "magnitude": None},  # 新增高斯峰
        "fit_success": False  # 拟合状态标记
    }

    # 初始猜测值（根据数据特征调整，与四峰相比新增峰5参数）
    p0 = [
        100, 537, 6,    # 峰1：A1, x1, gamma1（洛伦兹，gamma=半高宽）
        20, 550, 6,     # 峰2：A2, x2, gamma2（洛伦兹）
        1, 577, 1,      # 峰3：RatioA_23（A3/A2）, x3, RatioGamma_23（gamma3/gamma2）
        50, 550, 100,  # 峰4：A4, x4, gamma4（高斯，sigma）
        50, 650, 100    # 峰5：A5, x5, gamma5（新增高斯峰，sigma）
    ]

    # 拟合参数边界（限制合理范围，新增峰5边界）
    bounds = (
        [0, 535, 0,       # 峰1下界：A1≥0, x1≥535, gamma1≥0
         0, 540, 6,       # 峰2下界：A2≥0, x2≥540, gamma2≥6
         0.1, 575, 0.5,   # 峰3比例下界：RatioA≥0.1, x3≥575, RatioGamma≥0.5
         0.1, 500, 20,    # 峰4下界：A4≥0.1, x4≥500, sigma≥20
         0.1, 600, 10],   # 峰5下界：A5≥0.1, x5≥580, sigma≥10
        [100000, 540, 10,  # 峰1上界：A1≤1e5, x1≤540, gamma1≤10
         100000, 560, 20,  # 峰2上界：A2≤1e5, x2≤560, gamma2≤20
         10, 580, 2,       # 峰3比例上界：RatioA≤10, x3≤580, RatioGamma≤2
         100000, 600, 200, # 峰4上界：A4≤1e5, x4≤700, sigma≤300
         100000, 700, 200] # 峰5上界：A5≤1e5, x5≤650, sigma≤200
    )

    if_fit_success = False
    try:
        # 执行拟合
        popt, pcov = curve_fit(penta_peaks, x, y, p0=p0, bounds=bounds)
        # 解析拟合参数（按模型顺序）
        A1, x1, gamma1, A2, x2, gamma2, RatioA_23, x3, RatioGamma_23, A4, x4, gamma4, A5, x5, gamma5 = popt

        # 计算衍生参数
        A3 = A2 * RatioA_23  # 峰3振幅（比例推导）
        gamma3 = gamma2 * RatioGamma_23  # 峰3半高宽（比例推导）
        # 高斯峰半高宽（FWHM = 2.3548×sigma）
        gaussian4_fwhm = 2.3548 * gamma4
        gaussian5_fwhm = 2.3548 * gamma5
        # 各峰幅值（洛伦兹幅值=A/(π×(gamma/2))，高斯幅值=A）
        mag1 = (A1 / np.pi) / (gamma1 / 2)  # 洛伦兹峰顶点高度
        mag2 = (A2 / np.pi) / (gamma2 / 2)
        mag3 = (A3 / np.pi) / (gamma3 / 2)
        mag4 = A4  # 高斯峰顶点高度（即振幅A）
        mag5 = A5

        # 更新参数字典（拟合成功）
        fitting_paras.update({
            "peak1": {"A": A1, "center": x1, "fwhm": gamma1, "magnitude": mag1},
            "peak2": {"A": A2, "center": x2, "fwhm": gamma2, "magnitude": mag2},
            "peak3": {
                "A": A3, "center": x3, "fwhm": gamma3, "magnitude": mag3,
                "ratio_A": RatioA_23, "ratio_fwhm": RatioGamma_23
            },
            "peak4": {"A": A4, "center": x4, "sigma": gamma4, "fwhm": gaussian4_fwhm, "magnitude": mag4},
            "peak5": {"A": A5, "center": x5, "sigma": gamma5, "fwhm": gaussian5_fwhm, "magnitude": mag5},
            "fit_success": True
        })

        # 打印拟合结果
        print(f'拟合结果:')
        print(f'  峰1 (Lorentzian): A1 = {A1:.2f}, μ1 = {x1:.2f}, γ1 = {gamma1:.2f}, 幅值 = {mag1:.2f}')
        print(f'  峰2 (Lorentzian): A2 = {A2:.2f}, μ2 = {x2:.2f}, γ2 = {gamma2:.2f}, 幅值 = {mag2:.2f}')
        print(f'  峰3 (Lorentzian): A3 = {A3:.2f}, μ3 = {x3:.2f}, γ3 = {gamma3:.2f} (由比例确定), 幅值 = {mag3:.2f}')
        print(f'    比例参数: RatioA_23 = {RatioA_23:.2f}, RatioGamma_23 = {RatioGamma_23:.2f}')
        print(f'  峰4 (Gaussian):   A4 = {A4:.2f}, μ4 = {x4:.2f}, σ4 = {gamma4:.2f}, FWHM ≈ {gaussian4_fwhm:.2f}, 幅值 = {mag4:.2f}')
        print(f'  峰5 (Gaussian):   A5 = {A5:.2f}, μ5 = {x5:.2f}, σ5 = {gamma5:.2f}, FWHM ≈ {gaussian5_fwhm:.2f}, 幅值 = {mag5:.2f}')
        if_fit_success = True

    except Exception as e:
        # 拟合失败，使用初始猜测值
        A1, x1, gamma1 = p0[0], p0[1], p0[2]
        A2, x2, gamma2 = p0[3], p0[4], p0[5]
        RatioA_23, x3, RatioGamma_23 = p0[6], p0[7], p0[8]
        A4, x4, gamma4 = p0[9], p0[10], p0[11]
        A5, x5, gamma5 = p0[12], p0[13], p0[14]
        # 计算衍生参数（同拟合成功逻辑）
        A3 = A2 * RatioA_23
        gamma3 = gamma2 * RatioGamma_23
        gaussian4_fwhm = 2.3548 * gamma4
        gaussian5_fwhm = 2.3548 * gamma5
        mag1 = (A1 / np.pi) / (gamma1 / 2)
        mag2 = (A2 / np.pi) / (gamma2 / 2)
        mag3 = (A3 / np.pi) / (gamma3 / 2)
        mag4 = A4
        mag5 = A5
        # 更新参数字典（拟合失败）
        fitting_paras.update({
            "peak1": {"A": A1, "center": x1, "fwhm": gamma1, "magnitude": mag1},
            "peak2": {"A": A2, "center": x2, "fwhm": gamma2, "magnitude": mag2},
            "peak3": {
                "A": A3, "center": x3, "fwhm": gamma3, "magnitude": mag3,
                "ratio_A": RatioA_23, "ratio_fwhm": RatioGamma_23
            },
            "peak4": {"A": A4, "center": x4, "sigma": gamma4, "fwhm": gaussian4_fwhm, "magnitude": mag4},
            "peak5": {"A": A5, "center": x5, "sigma": gamma5, "fwhm": gaussian5_fwhm, "magnitude": mag5},
            "fit_success": False
        })
        print(f"拟合失败：{str(e)}，使用初始猜测值代替")

    # 绘制拟合曲线（若传入ax）
    if ax is not None:
        # 计算拟合曲线（区分拟合成功/失败的参数）
        if if_fit_success:
            y_fit = penta_peaks(x, A1, x1, gamma1, A2, x2, gamma2,
                               RatioA_23, x3, RatioGamma_23,
                               A4, x4, gamma4, A5, x5, gamma5)
        else:
            y_fit = penta_peaks(x, *p0)  # 用初始值计算

        # 计算各组分峰
        y_fit1 = lorentzian(x, A1, x1, gamma1)  # 峰1（洛伦兹）
        y_fit2 = lorentzian(x, A2, x2, gamma2)  # 峰2（洛伦兹）
        y_fit3 = lorentzian(x, A3, x3, gamma3)  # 峰3（洛伦兹）
        y_fit4 = gaussian(x, A4, x4, gamma4)    # 峰4（高斯）
        y_fit5 = gaussian(x, A5, x5, gamma5)    # 峰5（高斯）

        # 绘制曲线（修正标签，保持风格一致）
        ax.plot(x, y_fit, 'r-', label='Global Fit')
        ax.plot(x, y_fit1, 'b--', label='Peak 1 (Lorentzian)')
        ax.plot(x, y_fit2, 'g--', label='Peak 2 (Lorentzian)')
        ax.plot(x, y_fit3, 'm--', label='Peak 3 (Lorentzian)')
        ax.plot(x, y_fit4, 'y--', label='Peak 4 (Gaussian)')
        ax.plot(x, y_fit5, 'c--', label='Peak 5 (Gaussian)')  # 新增峰5曲线

    return fitting_paras

def triple_peaks_fitting_voigt_energy(x, y, ax=None, maxfev=10000):
    # 定义包含3个Voigt峰+1个高斯峰的复合函数
    def triple_peaks(x,
                     A1, mu1, sigma1, gamma1,  # Voigt峰1参数
                     A2, mu2, sigma2, gamma2,  # Voigt峰2参数
                     A3, mu3, sigma3, gamma3): # Voigt峰3参数
        # 3个Voigt峰
        peak1 = voigt(x, A1, mu1, sigma1, gamma1)
        peak2 = voigt(x, A2, mu2, sigma2, gamma2)
        peak3 = voigt(x, A3, mu3, sigma3, gamma3)
        return peak1 + peak2 + peak3

    fitting_paras = {}

    # 初始参数猜测（p0）：根据先验知识设置，关键是峰中心和大致展宽
    p0 = [
        1, 2.31, 0.026, 0.00011,    # 峰1：A1, mu1, sigma1, gamma1（sigma和gamma可设为FWHM的1/2左右）
        1, 2.26, 0.026, 0.00011,    # 峰2：A2, mu2, sigma2, gamma2
        1, 2.15, 0.026, 0.00011,     # 峰3：A3, mu3, sigma3, gamma3
    ]

    # 参数边界（bounds）：限制参数范围，避免无意义值（如振幅、展宽>0）
    bounds = (
        [0, 2.28, 0.001, 0.0001,
         0, 2.22, 0.001, 0.0001,
         0, 2.1, 0.001, 0.0001],
        [1e5, 2.35, 0.2, 0.01,
         1e5, 2.28, 0.2, 0.01,
         1e5, 2.19, 0.2, 0.01]
        )

    if_fit_success = False
    try:
        # 拟合：提高迭代次数，降低收敛阈值（ftol, xtol）
        popt, pcov = curve_fit(
            triple_peaks, x, y,
            p0=p0,
            bounds=bounds,
            maxfev=maxfev,
            ftol=1e-16,  # 残差变化阈值（更小更严格）
            xtol=1e-16   # 参数变化阈值
        )

        # 解析拟合结果
        A1, mu1, sigma1, gamma1, A2, mu2, sigma2, gamma2, A3, mu3, sigma3, gamma3 = popt

        # 打印拟合参数
        print("拟合结果:")
        print(f"峰1 (Voigt): A={A1:.2f}, 中心={mu1:.4f}, sigma={sigma1:.4f}, gamma={gamma1:.4f}")
        print(f"峰2 (Voigt): A={A2:.2f}, 中心={mu2:.4f}, sigma={sigma2:.4f}, gamma={gamma2:.4f}")
        print(f"峰3 (Voigt): A={A3:.2f}, 中心={mu3:.4f}, sigma={sigma3:.4f}, gamma={gamma3:.4f} (比例推导)")
        if_fit_success = True

    except Exception as e:
        print(f"拟合失败: {e}，使用初始猜测值替代")
        # 失败时用初始参数填充
        A1, mu1, sigma1, gamma1 = p0[0:4]
        A2, mu2, sigma2, gamma2 = p0[4:8]
        A3, mu3, sigma3, gamma3 = p0[8:12]

    # 计算半高宽（FWHM）：Voigt峰的FWHM无解析解，可近似为高斯和洛伦兹FWHM的组合
    # 高斯FWHM = 2*sqrt(2*ln2)*sigma ≈ 2.3548*sigma
    # 洛伦兹FWHM = 2*gamma
    # Voigt近似FWHM：(FWHM_gauss^5 + 2.69269*FWHM_gauss^4*FWHM_lorentz + ...)^(1/5)（简化可直接取两者最大值）
    fwhm1 = max(2.3548*sigma1, 2*gamma1)
    fwhm2 = max(2.3548*sigma2, 2*gamma2)
    fwhm3 = max(2.3548*sigma3, 2*gamma3)

    # 整理拟合结果字典
    fitting_paras = {
        "peak1": {"A": A1, "center": mu1, "sigma": sigma1, "gamma": gamma1, "fwhm": fwhm1},
        "peak2": {"A": A2, "center": mu2, "sigma": sigma2, "gamma": gamma2, "fwhm": fwhm2},
        "peak3": {"A": A3, "center": mu3, "sigma": sigma3, "gamma": gamma3, "fwhm": fwhm3},
        "fit_success": if_fit_success
    }

    # 绘图（如果传入ax）
    if ax is not None and if_fit_success:
        y_fit = triple_peaks(x, *popt)
        ax.plot(x, y_fit, 'r-', label='Global Lorentzian-Gaussian Fit')
        # 绘制各成分峰
        ax.plot(x, voigt(x, A1, mu1, sigma1, gamma1), 'b--', label='Peak 1 (Voigt Component)')
        ax.plot(x, voigt(x, A2, mu2, sigma2, gamma2), 'g--', label='Peak 1 (Voigt Component)')
        ax.plot(x, voigt(x, A3, mu3, sigma3, gamma3), 'm--', label='Peak 1 (Voigt Component)')

    return fitting_paras

# def poly5_lorentz():
#     fig = plt.figure(figsize=(12, 8), dpi=100)
#     ax = fig.add_subplot(121)
#
#     x = wav
#     y = scats[-1, :]
#     ax.plot(x, y)
#     coefficients = np.polyfit(x, y, 5)  # 返回系数 [a, b, c, d]
#     fitted_polynomial = np.poly1d(coefficients)
#     ax.plot(x, fitted_polynomial(x), 'r--')
#
#     def my_curve(x, A, x0, gamma):
#         return lorentzian(x, A, x0, gamma) + fitted_polynomial(x)
#
#     p0 = [0.0008, 600, 100]
#     x = wav
#     y = scats[10, :]
#     popt, pcov = curve_fit(my_curve, x, y, p0=p0)
#     A, x0, gamma = popt
#     ax2 = fig.add_subplot(122)
#     ax2.plot(x, y)
#     ax2.plot(x, my_curve(x, A, x0, gamma))

if __name__ == '__main__':
    x = np.arange(0, 6, 0.01)
    y = np.cos(x)
    fitting_paras = triple_peaks_fitting(x, y)
    print(fitting_paras)
    for key, val in fitting_paras.items():
        print(key, val)
