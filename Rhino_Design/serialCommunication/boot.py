"""
作用：ESP32-Backup 上电后首先执行的脚本，用于底层初始化
内容：
1.硬件初始化（如禁用不必要的外设、设置引脚模式）
2.网络预配置（如启动 WiFi 接入点模式）
3.挂载文件系统（若使用外部存储）
4.导入必要的全局模块（避免在main.py中重复导入）
"""
"""
boot按钮:启动模式选择，按下=下载模式，放开=运行模式
en按钮：复位按钮
1.进入下载模式：先按下boot按钮按住不放，再按下en按钮
2.正常复位：按下en按键就可以
3.通过ctrl+c终端程序
"""
import machine
import time

print("Here's ESP32-Backup!")

# 初始化LED指示灯
led = machine.Pin(2, machine.Pin.OUT)
print("boot")

led.on()  # 上电亮灯表示启动中
print("led on-boot")

# 延时确保硬件就绪
time.sleep(1)
led.off()  # 启动完成熄灯
print("led off-boot")