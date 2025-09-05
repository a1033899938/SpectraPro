# LED硬件控制模块
from machine import Pin
from app.logger import print_level

class LEDController:
    """LED控制器，封装LED相关操作"""
    
    def __init__(self, pin):
        self.led = Pin(pin, Pin.OUT)
        self.led.off()  # 初始状态关闭
        self.status = False  # False=关闭, True=开启
        print_level(1, "init", "LED控制器初始化完成")
        
    def on(self):
        """点亮LED"""
        self.led.on()
        self.status = True
        return True

    def off(self):
        """关闭LED"""
        self.led.off()
        self.status = False
        return True

    def toggle(self):
        """切换LED状态"""
        if self.status:
            self.off()
        else:
            self.on()
        return self.status

    def blink(self, times=1, interval=0.1):
        """闪烁LED指定次数"""
        original_status = self.status
        try:
            for _ in range(times):
                self.on()
                time.sleep(interval)
                self.off()
                time.sleep(interval)
        finally:
            # 恢复原始状态
            if original_status:
                self.on()
        return True
