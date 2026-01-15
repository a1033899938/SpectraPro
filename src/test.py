import numpy as np


def generate_hierarchical_sampling_centers(
        total_range_x,
        total_range_y,
        num_samples
):
    """
    生成层级化的采样中心，确保采样点均匀分散。
    例如:
    - 5个点: 在整个区域内分散布置5个点。
    - 25个点: 将区域分为5个大块，每块内再分散布置5个点。
    - 125个点: 分为5*5*5的三层结构。

    参数:
        total_range_x (float): 大区域在X轴上的总范围（宽度）。
        total_range_y (float): 大区域在Y轴上的总范围（高度）。
        num_samples (int): 期望的总采样点数 (应为 5 的幂，如 5, 25, 125 等)。

    返回:
        np.ndarray: 一个形状为 (num_samples, 2) 的NumPy数组，
                   其中每行包含一个采样中心的 (x, y) 坐标。
    """
    # 检查采样数是否为5的幂
    if num_samples <= 0:
        raise ValueError("采样数必须是正整数。")

    level = 0
    temp = num_samples
    while temp % 5 == 0 and temp > 1:
        temp //= 5
        level += 1

    if temp != 1:
        print(f"警告: 采样数 {num_samples} 不是 5 的幂。")
        print(f"将采用最接近的 5 的幂: {5 ** level}。")
        num_samples = 5 ** level
        if num_samples == 1:  # 如果用户输入的是1或无法被5整除的小数，默认使用5个点
            num_samples = 5
            level = 1

    centers = []

    # 定义在一个正方形区域内，5个采样点的相对中心位置 (x, y)
    # 这些点被设计成均匀分散在区域内
    relative_offsets = [
        (-0.5, 0.5),  # 左上
        (0.5, 0.5),  # 右上
        (-0.5, -0.5),  # 左下
        (0.5, -0.5),  # 右下
        (0.0, 0.0),  # 中心
    ]

    def recursive_generate(parent_center, parent_half_size_x, parent_half_size_y, current_level):
        """递归函数，用于在指定父区域内生成采样点"""
        if current_level == level:
            # 如果达到目标层级，将父区域的中心作为采样点
            centers.append(parent_center)
            return

        # 计算子区域的大小
        child_half_size_x = parent_half_size_x / 2.0
        child_half_size_y = parent_half_size_y / 2.0

        # 在父区域内，根据相对偏移生成子区域的中心
        for dx, dy in relative_offsets:
            child_center_x = parent_center[0] + dx * parent_half_size_x
            child_center_y = parent_center[1] + dy * parent_half_size_y

            # 递归地在子区域内生成下一层级的采样点
            recursive_generate(
                (child_center_x, child_center_y),
                child_half_size_x,
                child_half_size_y,
                current_level + 1
            )

    # 初始调用，从整个大区域的中心开始
    initial_center = (0, 0)
    initial_half_size_x = total_range_x / 2.0
    initial_half_size_y = total_range_y / 2.0

    recursive_generate(initial_center, initial_half_size_x, initial_half_size_y, 0)

    return np.array(centers)


import matplotlib.pyplot as plt


def visualize_hierarchical_sampling(
        total_range_x,
        total_range_y,
        map_x,
        map_y,
        sampling_centers
):
    """
    可视化层级化采样布局。
    """
    plt.figure(figsize=(12, 10), dpi=500)

    # 1. 绘制大区域的边界
    big_square_x = [-total_range_x / 2, total_range_x / 2, total_range_x / 2, -total_range_x / 2, -total_range_x / 2]
    big_square_y = [-total_range_y / 2, -total_range_y / 2, total_range_y / 2, total_range_y / 2, -total_range_y / 2]
    plt.plot(big_square_x, big_square_y, 'b--', linewidth=2, label='Total Area')

    # 2. 绘制每个采样区域的方形边界
    half_map_x = map_x / 2
    half_map_y = map_y / 2
    for (x0, y0) in sampling_centers:
        square_x = [x0 - half_map_x, x0 + half_map_x, x0 + half_map_x, x0 - half_map_x, x0 - half_map_x]
        square_y = [y0 - half_map_y, y0 - half_map_y, y0 + half_map_y, y0 + half_map_y, y0 - half_map_y]
        plt.plot(square_x, square_y, 'g-', linewidth=1, alpha=0.7)
        plt.fill(square_x, square_y, 'r', alpha=0.1)

    # 3. 在每个采样区域的中心绘制一个点
    # plt.scatter(sampling_centers[:, 0], sampling_centers[:, 1], c='r', s=50,
    #             edgecolors='k', zorder=5, label=f'Sampling Centers ({len(sampling_centers)} points)')

    # 4. 图表美化
    plt.xlabel('X Coordinate', fontsize=14)
    plt.ylabel('Y Coordinate', fontsize=14)
    plt.title('Hierarchical "Dice 5" Sampling Layout Visualization', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.axis('equal')

    params_text = (f'Total Range: X={total_range_x}, Y={total_range_y}\n'
                   f'Sample Size: X={map_x}, Y={map_y}\n'
                   f'Total Samples: {len(sampling_centers)}')
    plt.text(0.02, 0.98, params_text, transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.show()


# --- 调用示例 ---
if __name__ == '__main__':
    # 大区域尺寸
    total_range_x = 1000*6
    total_range_y = 1000*6

    # 每个小采样区域的尺寸
    map_x = 50
    map_y = 50

    # 期望的采样点数 (最好是 5, 25, 125, ...)
    num_samples = 100

    # 生成采样中心
    sampling_centers = generate_hierarchical_sampling_centers(
        total_range_x, total_range_y, num_samples
    )

    print(f"生成了 {len(sampling_centers)} 个采样中心。")

    # 可视化
    visualize_hierarchical_sampling(total_range_x, total_range_y, map_x, map_y, sampling_centers)