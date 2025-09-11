# 配置管理模块
class Config:
    """应用配置类，集中管理所有配置参数"""
    
    def __init__(self):
        # 初始化UART配置参数
        self._uart_num = 2
        self._uart_tx = 17  # 接CH340的RX
        self._uart_rx = 16  # 接CH340的TX
        self._uart_baudrate = 115200
        self._uart_parity = 1  # 1=偶校验, 0=奇校验, None=无校验

        # motor
        self._stepper_motor_En = 26
        self._stepper_motor_In1 = 27
        self._stepper_motor_In2 = 14
        self._stepper_motor_In3 = 12
        self._stepper_motor_In4 = 13

        # 初始化LED配置参数
        self._led_pin = 2  # 默认使用板载LED
        # 可以添加其他LED相关配置，如闪烁频率等
        self._led_blink_interval = 0.5  # 闪烁间隔（秒）

        # 应用配置
        self._command_timeout = 5  # 指令处理超时时间(秒)
        self._max_retry_count = 3  # 最大重试次数

    def update_config(self, **kwargs):
        """动态更新配置参数"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"警告: 未知配置项 {key}")
