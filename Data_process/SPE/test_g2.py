"""
Author: Junjie-Xie
Updated: 2026/1/6
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import csv

import numpy as np
import matplotlib.pyplot as plt


def load_spad_data(filename):
    """
    加载SPAD数据
    格式：时间(ps);累积计数
    """
    data = np.loadtxt(filename, delimiter=';')
    times = data[:, 0]  # 时间，单位ps
    counts = data[:, 1]  # 累积计数
    return times, counts

def main():
    # 加载两个txt文件（请替换为实际文件名）
    file1 = r"D:\ExpData\SPE\TCSPC_TEST\2000x-QD-2_C1_2026-01-06T15_38_35.txt"
    file2 = r"D:\ExpData\SPE\TCSPC_TEST\2000x-QD-2_C2_2026-01-06T15_38_35.txt"

    try:
        # 加载数据
        times1, counts1 = load_spad_data(file1)
        times2, counts2 = load_spad_data(file2)

        print(f"文件1数据点: {len(times1)}")
        print(f"文件2数据点: {len(times2)}")

        # 计算g²函数
        tau, g2 = calculate_g2_simple(times1, counts1, times2, counts2,
                                      bin_width=200, max_tau=10000)

        # 绘制结果
        plt.figure(figsize=(10, 6))
        plt.plot(tau, g2, 'b-', linewidth=2)
        plt.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='g²=1 (经典极限)')
        plt.xlabel('Time delay τ (ps)', fontsize=12)
        plt.ylabel('g²(τ)', fontsize=12)
        plt.title('Second-order Correlation Function g²(τ)', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # 保存结果
        results = np.column_stack((tau, g2))
        np.savetxt('g2_results.csv', results, delimiter=',',
                   header='tau(ps),g2', comments='')
        print("结果已保存到 g2_results.csv")

        # 打印统计信息
        print(f"\n统计信息:")
        print(f"最大g²值: {np.max(g2):.3f}")
        print(f"最小g²值: {np.min(g2):.3f}")
        print(f"τ=0处的g²值: {g2[len(g2) // 2]:.3f}")

    except FileNotFoundError as e:
        print(f"错误: 文件未找到 - {e}")
        print("请确保文件存在，或者使用以下示例数据:")

        # 使用示例数据
        print("\n使用示例数据...")

        # 创建示例数据
        np.random.seed(42)
        n_points = 1000

        # 模拟SPAD数据
        times1_example = np.sort(np.random.uniform(0, 1e7, n_points))
        counts1_example = np.arange(1, n_points + 1)

        # 添加一些相关性
        times2_example = times1_example + np.random.normal(0, 100, n_points)  # 添加一些时间抖动
        times2_example = np.sort(times2_example)
        counts2_example = np.arange(1, n_points + 1)

        # 保存示例数据
        data1 = np.column_stack((times1_example, counts1_example))
        data2 = np.column_stack((times2_example, counts2_example))
        np.savetxt('example_data1.txt', data1, delimiter=';', fmt='%.1f;%d')
        np.savetxt('example_data2.txt', data2, delimiter=';', fmt='%.1f;%d')

        print("示例数据已保存为 example_data1.txt 和 example_data2.txt")

        # 使用示例数据计算g²
        tau, g2 = calculate_g2_simple(times1_example, counts1_example,
                                      times2_example, counts2_example,
                                      bin_width=500, max_tau=20000)

        # 绘制结果
        plt.figure(figsize=(10, 6))
        plt.plot(tau, g2, 'b-', linewidth=2)
        plt.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='g²=1 (经典极限)')
        plt.xlabel('Time delay τ (ps)', fontsize=12)
        plt.ylabel('g²(τ)', fontsize=12)
        plt.title('Example: Second-order Correlation Function g²(τ)', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()

    # csv_path = r"D:\ExpData\SPE\TCSPC_TEST\LAP_Anneal_hBN_SPE-1_2026-01-06T15_40_37.csv"
    # txt_path1 = r"D:\ExpData\SPE\TCSPC_TEST\2000x-QD-2_C1_2026-01-06T15_38_35.txt"
    # txt_path2 = r"D:\ExpData\SPE\TCSPC_TEST\2000x-QD-2_C2_2026-01-06T15_38_35.txt"
    #
    # times = []
    # R1s = []
    # R2s = []
    # with open(csv_path, mode='r', encoding='utf-8') as file:
    #     csv_reader = csv.reader(file)
    #     # 跳过表头（如果CSV第一行是列名，如tau,counts）
    #     header = next(csv_reader)
    #     # 逐行读取数据并转换为数值类型（实验数据多为浮点数/整数）
    #     for row in csv_reader:
    #         str_list = row[0].split(";")
    #         num_list = [int(s) for s in str_list]
    #         times.append(num_list[0]/1000)
    #         R1s.append(num_list[1])
    #         R2s.append(num_list[2])
    #
    # fig = plt.figure(figsize=(12, 8), dpi=200)
    # ax = fig.add_subplot(111)
    # ax.plot(times, R1s, label='R1')
    # ax.plot(times, R2s, label='R2')
    # ax.legend()
    # plt.show()