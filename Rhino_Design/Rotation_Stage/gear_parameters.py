import numpy as np

"""蜗杆"""
print("---Worm---")
# 蜗杆头数Z1
Z1 = 1

# 模数m
m = 4

# 蜗杆直径系数q
q = 10

# 蜗杆分度圆直径d1
d1 = m * q
print(f"蜗杆分度圆直径d1: {d1:.3f} mm")

# 蜗杆齿顶高ha1
ha1 = 1 * m
print(f"蜗杆齿顶高ha1: {ha1:.3f} mm")

# 蜗杆齿顶圆直径d_a1
d_a1 = d1 + 2 * ha1
print(f"蜗杆齿顶圆直径d_a1: {d_a1:.3f} mm")

# 蜗杆齿根高hf1
hf1 = 1.2 * m
print(f"蜗杆齿根高hf1: {hf1:.3f} mm")

# 蜗杆齿根圆直径d_f1
d_f1 = d1 - 2 * hf1
print(f"蜗杆齿根圆直径d_f1: {d_f1:.3f} mm")

# 蜗杆分度圆柱导程角λ
lambda_radians = np.arctan(Z1 / q)
λ_degrees = np.rad2deg(lambda_radians)
print(f"蜗杆分度圆柱导程角λ: {λ_degrees:.3f} °")

# 齿形角α
alpha = 20

# 蜗杆导程Pz
Pz = np.pi * m * Z1
print(f"蜗杆导程Pz: {Pz:.3f} mm")

# 蜗杆轴向齿距pa
pa = np.pi * m
print(f"蜗杆轴向齿距pa: {pa:.3f} mm")

# 蜗杆轴向齿厚Sa
Sa = 0.5 * np.pi * m
print(f"蜗杆轴向齿厚Sa: {Sa:.3f} mm")

# 蜗轮齿数Z2
Z2 = 40

# 蜗杆螺纹部分长度L(图中的b1尺寸)，变位系数ξ=0时，L≥(11 + 0.06*Z2)*m
L = (11 + 0.06 * Z2) * m
print(f"蜗杆螺纹部分长度L≥ {L:.3f} mm")
# 蜗杆螺纹部分长度L
L = 60
print(f"蜗杆螺纹部分长度L: {L:.3f} mm")

# 蜗杆齿根圆半径ρf
rf = 0.3 * m
print(f"蜗杆齿根圆半径ρf: {rf:.3f} mm")


"""蜗轮刀具"""
print("\n---Worm Knife---")
# 蜗轮齿数
# Z2上面已经定义

# 模数
# m上面已经定义

# 蜗轮分度圆直径d2
d2 = m * Z2
print(f"蜗轮分度圆直径d2: {d2:.2f} mm")

# 压力角α
# alpha上面已经定义

# 涡轮基圆直径db
db = d2 * np.cos(np.deg2rad(alpha))
print(f"涡轮基圆直径db: {db:.2f} mm")

# 蜗轮每个齿对应的角度φ
phi = 360 / Z2
print(f"蜗轮每个齿对应的角度φ: {phi} °")

"""Worm Gear"""
print("\n---Worm Gear---")
# 蜗轮变位系数xi
xi = 0
# 蜗轮齿顶高ha2
ha2 = (1 + xi) * m
print(f"蜗轮齿顶高ha2: {ha2:.2f} mm")
# 蜗轮齿顶圆直径d_a2
d_a2 = d2 + 2 * ha2
print(f"蜗轮齿顶圆直径d_a2: {d_a2:.2f} mm")
# 蜗轮齿根高hf2
hf2 = (1.2 - xi) * m
print(f"蜗轮齿根高hf2: {hf2:.2f} mm")
# 蜗轮齿根圆直径d_f2
d_f2 = d2 - 2 * hf2
print(f"蜗轮齿根圆直径d_f2: {d_f2:.2f} mm")
# 蜗轮外径d_e2
d_e2 = d_a2 + 2 * m
print(f"蜗轮外径d_e2: {d_e2:.2f} mm")
# 蜗杆分度圆直径d1
# d1上面已经定义
# 蜗轮齿顶圆弧半径R
R = d1 / 2 - m
print(f"蜗轮齿顶圆弧半径R: {R:.2f} mm")
# 蜗杆齿顶圆直径d_a1
# d_a1上面已经定义
# 蜗轮宽度B
B = 0.75 * d_a1
print(f"蜗轮宽度B: {B:.2f} mm")
# 蜗轮面角2*gamma
gamma = 50
print(f"蜗轮面角2*gamma: {2 * gamma} °")

"""Spiral"""
print("\n---Spiral---")
# 蜗杆头数Z1
# Z1上面已经定义

# 蜗杆导程Pz
# Pz上面已经定义
print(f"蜗杆导程Pz: {Pz:.2f} mm")