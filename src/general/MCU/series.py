import serial
import serial.tools.list_ports
import threading
import time
import sys


class ESP32SerialComm:
    def __init__(self):
        self.ser = None
        self.connected = False
        self.running = False
        self.receive_thread = None
        self.user_input = None  # 用于存储用户输入的全局变量

    def list_ports(self):
        """列出所有可用串口"""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port, baudrate=115200):
        """连接到ESP32的串口"""
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=0.1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )

            if self.ser.is_open:
                self.connected = True
                self.running = True
                # 启动接收线程（独立线程，负责持续接收数据）
                self.receive_thread = threading.Thread(target=self._receive_data, daemon=True)
                self.receive_thread.start()
                print(f"已连接到ESP32: {port} @ {baudrate}")
                return True
            return False
        except Exception as e:
            print(f"连接失败: {str(e)}")
            return False

    def disconnect(self):
        """断开连接"""
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.connected = False
        print("已断开与ESP32的连接")

    def send_data(self, data):
        """发送数据到ESP32"""
        if not self.connected:
            print("未连接到ESP32")
            return False

        try:
            # 发送数据并添加换行符作为结束标志
            self.ser.write(f"{data}\n".encode('utf-8'))
            print(f"发送到ESP32: {data}")
            return True
        except Exception as e:
            print(f"发送失败: {str(e)}")
            return False

    def _receive_data(self):
        """接收线程：持续接收数据，不阻塞主线程"""
        while self.running and self.connected:
            try:
                if self.ser.in_waiting > 0:
                    # 读取一行数据（以换行符为结束标志）
                    data = self.ser.readline().decode('utf-8').strip()
                    if data:
                        print(f"\n从ESP32接收: {data}")
                        # 接收数据后显示输入提示（优化用户体验）
                        print("输入要发送的数据 (输入exit退出): ", end='', flush=True)
                time.sleep(0.01)  # 降低CPU占用
            except Exception as e:
                print(f"接收错误: {str(e)}")
                break

    def start_communication(self):
        """启动通信主循环：独立处理用户输入，不阻塞接收"""
        try:
            # 发送测试数据
            self.send_data("Hello ESP32 from Python!")

            # 主循环：处理用户输入（单独的输入逻辑，不阻塞接收线程）
            while True:
                # 显示输入提示（注意添加flush=True确保即时显示）
                user_input = input("输入要发送的数据 (输入exit退出): ")
                if user_input.lower() == 'exit':
                    break
                self.send_data(user_input)

        except KeyboardInterrupt:
            print("\n用户中断")
        finally:
            self.disconnect()


if __name__ == "__main__":
    comm = ESP32SerialComm()

    # 列出可用串口
    ports = comm.list_ports()
    print("可用串口:", ports)

    if ports:
        # 连接到第一个可用串口
        if comm.connect(ports[0], 115200):
            comm.start_communication()  # 启动同时收发的主逻辑
    else:
        print("未找到可用串口，请检查ESP32连接")