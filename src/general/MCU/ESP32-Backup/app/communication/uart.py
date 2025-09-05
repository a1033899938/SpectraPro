# UART通信模块
from machine import UART, Pin
from app.logger import print_level
from app.device import Device
import time

class UARTCommunication(Device):
    """UART通信管理器，封装所有UART相关操作"""
    
    def __init__(self, cfg):
        super().__init__(device_id="Controller 1", name="Controller 1", params=None)
        self.cfg = cfg
        self.uart = None

        self.initialized = False
        # 调用父类初始化方法
        self.initialize()

    def _check_required_params(self):
        """
        检查设备初始化所需的必要参数是否齐全且有效
        :return: 所有参数有效返回True，否则返回False
        """
        # 检查配置对象是否存在
        if not hasattr(self, 'cfg'):
            self._error_info = "缺少配置对象(cfg)"
            return False

        # 定义UART必须的配置参数及其验证规则
        uart_required = [
            ('_uart_num', lambda x: isinstance(x, int) and x >= 0),
            ('_uart_tx', lambda x: isinstance(x, int) and x >= 0),
            ('_uart_rx', lambda x: isinstance(x, int) and x >= 0),
            ('_uart_baudrate', lambda x: isinstance(x, int) and x in [9600, 19200, 38400, 57600, 115200, 230400])
            ('_command_timeout', lambda x: isinstance(x, int) and x >= 0)
            ('_max_retry_count', lambda x: isinstance(x, int) and 10>= x >= 0)
        ]

        # 检查每个必要参数
        for param_name, validator in uart_required:
            # 检查参数是否存在
            if not hasattr(self.cfg, param_name):
                self._error_info = f"缺少必要配置参数: {param_name}"
                return False

            # 获取参数值并验证有效性
            param_value = getattr(self.cfg, param_name)
            if not validator(param_value):
                self._error_info = f"配置参数无效: {param_name}={param_value}"
                return False

        return True


    def _initialize(self):
        """重写初始化方法"""
        try:
            self.uart = UART(
                self.cfg._uart_num,
                baudrate=self.cfg._uart_baudrate,
                tx=self.cfg._uart_tx,
                rx=self.cfg._uart_rx
            )

            self.uart.init(
                baudrate=self.cfg._uart_baudrate,
                bits=8,
                parity=self.cfg._uart_parity,
                stop=1,
                timeout=2000,
                timeout_char=100
            )

            # 更可靠的UART验证：尝试发送测试命令或读取标识
            self._verify_uart_connection()
            
        except Exception:
            raise # 重新抛出异常，让父类捕获处理

    def send_data(self, data):
        """发送数据到串口"""
        if not self.initialized:
            print_level(1, "init", "UART未初始化，无法发送数据")
            return False
            
        try:
            if isinstance(data, str):
                data = data + '\r\n'
                data = data.encode('utf-8')
            
            bytes_sent = self.uart.write(data)
            return bytes_sent
        except Exception as e:
            return False

    def send_response(self, session_id, message):
        """发送带会话ID的响应"""
        response = f"SESSION:{session_id};MESSAGE:{message}"
        return self.send_data(response)

    def receive_data(self, max_len=1024):
        """从串口接收数据"""
        if not self.initialized or not self.uart.any():
            return None
            
        try:
            data = self.uart.readline()
            if data:
                data = data.replace(b'\x00', b'')  # 移除NULL字符
                str_data = data.decode('utf-8').strip()
                if str_data:
                    return str_data
            return None
        except UnicodeError:
            print_level(1, "error: uart", "UART数据解码失败（Unicode格式错误）")
            return None
        except Exception as e:
            print_level(1, "error: uart", f"接收数据错误: {e}")
            return None

    def close(self):
        """关闭UART连接"""
        if self.uart:
            self.uart.deinit()
            self.initialized = False
        return False