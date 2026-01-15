"""
Author: Junjie-Xie
Updated: 2025/12/16
Functions: 
"""
slope1=0.0469
slope2=0.0210

tau1=2.82
tau2=1.92

time1=8.98
time2=6.51
print(f"焦移缩短了{(slope1-slope2)/slope1:.3f}")
print(f"重构速度提高了{((1/tau2)-(1/tau1))/(1/tau1):.3f}")
print(f"重构时间缩短了{(tau1-tau2)/tau1:.3f}")
print(f"重构时间2缩短了{(time1-time2)/time1:.3f}")