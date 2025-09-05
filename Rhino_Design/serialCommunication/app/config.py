# 配置管理模块
class Config:
    """应用配置类，集中管理所有配置参数"""
    
    def __init__(self):
        # UART配置
        self.uart_num = 2
        self.uart_tx = 17
        self.uart_rx = 16
        self.uart_baudrate = 115200
        self.uart_parity = 1  # 1=偶校验, 0=奇校验, None=无校验
        
        # 硬件配置
        self.led_pin = 2  # 默认使用板载LED
        
        # 应用配置
        self.command_timeout = 5  # 指令处理超时时间(秒)
        self.max_retry_count = 3  # 最大重试次数

    def update_config(self, **kwargs):
        """动态更新配置参数"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"警告: 未知配置项 {key}")
