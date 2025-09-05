# UART通信模块
from machine import UART
from app.logger import print_level


class UARTCommunication:
    """UART通信管理器，封装所有UART相关操作"""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.uart = None
        self.initialized = False
        
        # 初始化UART
        self._init_uart()

    def _init_uart(self):
        """初始化UART硬件"""
        try:
            self.uart = UART(
                self.cfg.uart_num, 
                baudrate=self.cfg.uart_baudrate,
                tx=self.cfg.uart_tx, 
                rx=self.cfg.uart_rx
            )
            
            self.uart.init(
                baudrate=self.cfg.uart_baudrate,
                bits=8,
                parity=self.cfg.uart_parity,
                stop=1,
                timeout=2000,
                timeout_char=100
            )
            
            # 验证初始化
            if self.uart.any() is not None:
                self.initialized = True
                print_level(1, "init", "UART通信初始化完成")
            else:
                print_level(1, "error: uart", "UART初始化后不可用")
                raise Exception("UART初始化后不可用")
            
        except Exception as e:
            print_level(1, "error: uart", f"UART初始化失败: {e}")
            self.initialized = False

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

