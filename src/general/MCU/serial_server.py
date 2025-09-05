"""
Author: Junjie-Xie
Updated: 2025/8/8
Functions: 
"""

import serial
import serial.tools.list_ports
import threading
import time
from src.general.print_level import *

def get_ports():
    """列出所有可用串口"""
    ports = serial.tools.list_ports.comports()
    ports_info = {}
    for port in ports:
        ports_info[port.device] = {
            "description": port.description,
            "vid": port.vid,
            "pid": port.pid,
            "manufacturer": port.manufacturer,
        }
    return ports_info

class Serial_Server:
    def __init__(self):
        self.serials = {}

        self.sessions = {}
        self.session_num = 0
        self.response_received = threading.Event()  # 用于等待响应的事件。发送指令时将 session_id 加入 “待处理队列”，收到响应后会从队列中移除

    def connect(self, port, port_name=None, recv_slot=None,baudrate=115200):
        """连接到串口"""
        print_title(f"连接串口: {port} @ {baudrate}")

        if port_name is None:
            port_name = port

        try:
            ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=0.1,
                parity=serial.PARITY_EVEN,  # 偶校验（与ESP32端parity=1对应）
                # parity=serial.PARITY_ODD,  # 奇校验（与ESP32端parity=0对应）
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )

            self.serials = {
                f"{port_name}": {
                    "ser": ser,
                    "port": port,
                    "baudrate": baudrate,
                    "is_connected": False,
                    "last_heartbeat_time": None,
                    "recv_slot": self.find_recv_slot(recv_slot),
                }
            }

            if ser.is_open:
                self.serials[port_name].update({"is_connected": True})
            else:
                raise ConnectionError(f"Error(Serial_Server::connect): 串口未成功打开")
        except Exception as e:
            print(f"Error(Serial_Server::connect): {str(e)}")

    def disconnect(self, port_name):
        """断开连接"""
        try:
            if port_name not in self.serials:  # 检查串口是否存在
                raise ValueError(f"Error(Serial_Server::disconnect): {port_name} not in self.serials")
                return

            print_title(f"尝试断开与串口: {port_name}的连接")

            ser = self.serials[port_name]["ser"]
            if ser.is_open:  # 检查串口是否打开
                ser.close()
            self.serials[port_name].update({"is_connected": False})
            print_content(f"已断开与串口: {port_name}的连接")
        except Exception as e:
            print(f"Error(Serial_Server::disconnect): {str(e)}")

    def _write(self, port_name, data):
        try:
            if port_name not in self.serials:  # 检查串口是否存在
                raise ValueError(f"Error(Serial_Server::_write): {port_name} not in self.serials")
                return False

            if not self.serials[port_name]["is_connected"]:
                raise ValueError(f"Error(Serial_Server::_write): {port_name} not connected")
                return False

            ser = self.serials[port_name]["ser"]
            ser.write(f"{data}\r\n".encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error(Serial_Server::_write): {str(e)}")

    def _read(self, port_name):
        try:
            if port_name not in self.serials:  # 检查串口是否存在
                raise ValueError(f"Error(Serial_Server::_read): {port_name} not in self.serials")
                return False

            if not self.serials[port_name]["is_connected"]:
                raise ValueError(f"Error(Serial_Server::_read): {port_name} not connected")
                return False

            ser = self.serials[port_name]["ser"]

            if ser.in_waiting > 0:  # 检查串口缓冲区是否有等待的数据
                data = ser.readline().decode('utf-8').strip()
                return data
        except Exception as e:
            print(f"Error(Serial_Server::_read): {str(e)}")

    def main_loop(self):
        """启动通信主循环"""
        try:
            print_title("启动通信主循环")

            # 启动所有端口的独立接收线程
            for port_name in self.serials.keys():
                self._create_reading_thread(port_name, recv_slot=self.serials[port_name]["recv_slot"])

            while True:
                    user_input = input("输入要发送的数据 (输入exit退出): \n")
                    if user_input.lower() == 'exit':
                        break
                    else:
                        # self._write("RS", user_input)
                        self._create_session(port_name="RS", data=user_input)
                        time.sleep(0.1)

        except KeyboardInterrupt as e:
            print(f"Error(Serial_Server::main_loop): 用户中断")
        finally:
            for port_name in self.serials.keys():
                self.disconnect(port_name)
            print_title("主循环结束, 已断开通信")

    def _reading_thread(self, port_name, recv_slot):
        while True:
            recv = self._read(port_name)
            if recv is not None:
                recv_slot(port_name, recv)

    def _create_reading_thread(self, port_name, recv_slot):
        reading_thread = threading.Thread(target=self._reading_thread, kwargs={"port_name": port_name, "recv_slot": recv_slot}, daemon=True)
        reading_thread.start()

    """create session"""
    def _create_session(self, port_name, data):
        self.sessions[self.session_num] = {
            "command": data,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
            "port_name": port_name,
            "status": "create",
            "pending": False,
            "inquiry": False,
            "connection": False,
        }

        formatted_data = f"SESSION:{self.session_num};CMD:{data};END"
        if self._write(port_name, formatted_data):
            self.sessions[self.session_num].update({"status": "sent"})
        print(self.sessions[self.session_num])
        self.session_num += 1

    """recv event"""
    def find_recv_slot(self, recv_slot):
        if recv_slot is None:
            return self.just_print
        elif recv_slot == "ESP32":
            return self.ESP32

    def just_print(self, recv):
        print(recv)

    def ESP32(self, port_name, recv):
        print(recv)

        # 读取来自串口的会话信息
        parts = recv.split(";")
        part0 = parts[0]
        part1 = parts[1]
        session_num = part0.replace("SESSION:", "")
        session_status = part1.replace("CMD:", "")

        # 更新会话本地记录
        self.sessions[session_num].update({"status": session_status})

        # print(self.sessions[session_num])


if __name__ == "__main__":
    # 列出可用串口
    ports_info = get_ports()
    for port, info in ports_info.items():
        if "USB-SERIAL CH340" in info["description"] and info["manufacturer"] == "wch.cn":
            print(port)

    comm = Serial_Server()
    comm.connect("COM14", "RS")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    # comm._write("RS", "pcjun: hello PC")
    comm.main_loop()
