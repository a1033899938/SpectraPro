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
        self.ser = None
        self.port = None
        self.baudrate = None
        self.connected = False
        self.running = False

        self.pending_responses = {}
        self.current_session = 0  # 当前会话编号
        self.session_status = {}
        self.response_received = threading.Event()  # 用于等待响应的事件。发送指令时将 session_id 加入 “待处理队列”，收到响应后会从队列中移除

    def start_communication(self):
        """启动通信主循环"""
        try:
            # print_level(1, 'init', f"启动通信主循环, 向串口发送测试指令")
            # self.send_session_command("Hello ESP32-Backup from Pycharm!")

            while True:
                if not any([self.running, self.connected]):
                    print_level(1, 'error', f"连接已断开或通信循环已关闭, 尝试重新连接")
                    self.connect(self.port, self.baudrate)

                    # 启动接收线程（独立线程，负责持续接收数据）
                    self.receive_thread = threading.Thread(target=self._receive_data, daemon=True)
                    self.receive_thread.start()

                if not self.pending_responses:  # 没有等待的响应时才接受用户输入
                    user_input = input("输入要发送的数据 (输入exit退出): ")
                    if user_input.lower() == 'exit':
                        break
                    self.send_session_command(user_input)
                else:
                    # 有等待的响应，短暂休眠
                    time.sleep(0.1)

        except KeyboardInterrupt:
            print_level(1, 'error', "\n用户中断")
        finally:
            print_level(1, 'error', "已断开通信")
            self.disconnect()

    # def connect(self, port, baudrate=115200):
    #     """连接到串口"""
    #     print_title(f"连接串口: {port} @ {baudrate}")
    #
    #     self.port = port
    #     self.baudrate = baudrate
    #     try:
    #         self.ser = serial.Serial(
    #             port=port,
    #             baudrate=baudrate,
    #             timeout=0.1,
    #             parity=serial.PARITY_EVEN,  # 偶校验（与ESP32端parity=1对应）
    #             # parity=serial.PARITY_ODD,  # 奇校验（与ESP32端parity=0对应）
    #             stopbits=serial.STOPBITS_ONE,
    #             bytesize=serial.EIGHTBITS
    #         )
    #
    #         if self.ser.is_open:
    #             self.connected = True
    #             self.running = True
    #             print_level(2, 'success', f"已连接串口: {port} @ {baudrate}, 接收线程启动")
    #             return True
    #         else:
    #             self.connected = False
    #             self.running = False
    #             print_level(2, 'error', f"连接串口失败: 串口未打开")
    #             return False
    #     except Exception as e:
    #         self.connected = False
    #         self.running = False
    #         print_level(2, 'error', f"连接串口失败: {str(e)}")
    #         return False

    # def disconnect(self):
    #     """断开连接"""
    #     print_level(1, 'disconnect', "尝试断开与串口的连接")
    #     try:
    #         if self.ser and self.ser.is_open:
    #             self.ser.close()
    #             self.connected = False
    #             self.running = False
    #         print_level(2, 'success', "已断开与串口的连接")
    #         return True
    #     except Exception as e:
    #         print_level(2, 'error', f"断开与串口的连接失败: {str(e)}")
    #         return False

    # def _write(self, data):
    #     self.ser.write(f"{data}\r\n".encode('utf-8'))

    # def _read(self):
    #     while self.running and self.connected:
    #         try:
    #             if self.ser.in_waiting > 0:
    #                 data = self.ser.readline().decode('utf-8').strip()
    #         except Exception as e:
    #             print_level(2, 'error', f"接收错误: {str(e)}")
    #             break

    def send_session_command(self, cmd):
        """发送指令到串口"""
        print_level(1, 'send', "尝试发送指令到串口")
        if not any([self.connected, self.running]):
            print_level(2, 'error', "连接已断开或通信循环已关闭, 取消发送指令到串口")
            return False

        # 递增会话编号
        self.current_session += 1
        session_id = self.current_session

        try:
            # 发送带会话编号的指令
            data = f"SESSION:{session_id};CMD:{cmd}"
            self.ser.write(f"{data}\r\n".encode('utf-8'))
            print_level(2, 'success', f"已发送指令: {data}, 当前会话编号: {session_id}")

            # 记录正等待响应的会话
            self.session_status[session_id] = 'pending'
            print_level(2, 'resp', f"等待会话响应...")

            # 等待响应，最长10秒
            response_received = self.response_received.wait(10)  # 等待接收线程的响应

            if response_received:
                self.response_received.clear()   # 重置事件状态，为下一次等待做准备
                if session_id not in self.pending_responses:
                    print_level(3, 'success', f"会话 {session_id} 已收到响应, 指令执行成功")
                    return True
                else:
                    # 无效响应
                    print_level(3, 'invalid', f"会话 {session_id} 收到无效响应, 尝试处理...")
                    return self._handle_invalid_response(session_id, cmd)
            else:
                # 超时未收到响应，发起询问
                print_level(3, 'timeout', f"会话 {session_id} 超时未收到响应，发起询问...")
                return self._inquire_session(session_id)

        except Exception as e:
            print_level(2, 'error', f"会话错误: {str(e)}")
            return False

    def _receive_data(self):
        """接收线程：处理resp和inquire"""
        while self.running and self.connected:
            try:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline().decode('utf-8').strip()
                    if data:
                        print_level(1, 'recv', f"从串口接收到信息: {data}")

                        # 检查是否是会话响应
                        if data.startswith("SESSION:"):
                            parts = data.split(";")
                            session_id = None
                            status = ""

                            # 提取会话ID和状态
                            for part in parts:
                                print(part)
                                if part.startswith("SESSION:"):
                                    try:
                                        session_id = int(part.split(":")[1])
                                    except ValueError:
                                        pass
                                elif part.startswith("STATUS:"):
                                    status = part.split(":")[1]
                                elif part.startswith("MSG:"):
                                    msg = part.split(":")[1]

                            if session_id is not None and session_id in self.pending_responses:
                                # 处理"不存在"状态
                                if status == "NOT_FOUND":
                                    print_level(2, 'not found', f"会话 {session_id} 确认不存在")
                                    self.session_not_found_flag[session_id] = True
                                    del self.pending_responses[session_id]
                                    self.response_received.set()
                                # 处理"执行成功"状态
                                elif status == "EXECUTED":
                                    print_level(2, 'EXECUTED', f"会话 {session_id} 执行成功")
                                    del self.pending_responses[session_id]
                                    self.response_received.set()
                                # 处理"重试中"状态
                                elif status == "RETRYING":
                                    print_level(2, 'RETRYING', f"会话 {session_id} 正在重试")
                                else:
                                    print_level(2, "unknow", "接收到未知响应")
                                    del self.pending_responses[session_id]
                                    self.response_received.set()

                                # 处理错误响应
                            elif data.startswith("SESSION:ERROR"):
                                print_level(2, 'recv', f"接收错误: {data}")

                    # 显示输入提示（无等待响应时）
                    if not self.pending_responses:
                        print("输入要发送的数据 (输入exit退出): ", end='', flush=True)
                time.sleep(0.01)
            except Exception as e:
                print_level(2, 'error', f"接收错误: {str(e)}")
                break

    def emergency_stop(self):
        """紧急停止，立即断开连接并执行安全处理"""
        self.running = False
        # 紧急情况下可以发送特定的停止指令
        try:
            if self.ser and self.ser.is_open:
                # 发送紧急停止命令（根据实际设备协议调整）
                self.ser.write(b'EMERGENCY_STOP\n')
                # 确保命令发送完成
                self.ser.flush()
                # 短暂延迟让设备接收命令
                time.sleep(0.1)
                self.ser.close()
        except Exception as e:
            print_level(2, 'emergency_stop', f"发送停止命令时出错: {str(e)}")
        finally:
            self.connected = False
            print_level(1, 'emergency_stop', "已执行紧急停止并断开连接")



    def _handle_invalid_response(self, session_id, cmd):
        # 检查会话是否已被标记为“不存在”（ESP32返回NOT_FOUND）
        if self.session_not_found_flag[session_id]:
            print_level(4, 'not found', f"会话 {session_id} 在串口端无记录，停止处理")
            return False

        # 检查会话是否已被处理（如正常响应后被移除）
        if session_id not in self.pending_responses:
            print_level(4, 'not found', f"会话 {session_id} 已收到响应，停止处理")
            return False

        # 循环处理最多3次无效响应
        while True:
            # 获取当前无效响应次数（从pending_responses中读取）
            current_count = self.pending_responses[session_id][2]

            # 若已达到最大次数（3次），清理并退出
            if current_count >= 3:
                print_level(5, 'timeout', f"会话 {session_id} 多次无效响应，放弃处理, 移除本会话记录")
                del self.pending_responses[session_id]
                return False

            # 等待2秒，判断是否收到有效响应
            print_level(4, 'retry', f"会话 {session_id} 第 {current_count + 1} 次重试，等待响应...")
            response_received = self.response_received.wait(2)

            # 若收到有效响应（会话已被移除），返回成功
            if response_received:
                self.response_received.clear()
                if session_id not in self.pending_responses:
                    print_level(5, 'success', f"会话 {session_id} 重试后已收到有效响应, 指令执行成功")
                    return True
                else:
                    # 仍为无效响应，更新计数并继续循环
                    new_count = current_count + 1
                    self.pending_responses[session_id] = (cmd, time.time(), new_count)
                    print_level(5, 'invalid', f"会话 {session_id} 第 {new_count} 次无效响应")
            else:
                # 等待超时，更新计数并继续循环
                new_count = current_count + 1
                self.pending_responses[session_id] = (cmd, time.time(), new_count)
                print_level(5, 'timeout', f"会话 {session_id} 第 {new_count} 次等待超时")

    def _inquire_session(self, session_id):
        """询问指定会话的执行情况"""
        # 检查是否已标记为"不存在"
        if self.session_not_found_flag[session_id]:
            print_level(4, 'not found', f"会话 {session_id} 在串口端无记录，停止询问")
            del self.pending_responses[session_id]
            return False

        if session_id not in self.pending_responses:
            print_level(4, 'not found', f"会话 {session_id} 已收到响应，停止询问")
            return False

        cmd, _, inquiry_count = self.pending_responses[session_id]

        # 循环最多询问3次
        while True:
            # 获取当前询问次数
            cmd, _, inquiry_count = self.pending_responses[session_id]

            # 达到最大询问次数（3次），清理并退出
            if inquiry_count >= 3:
                print_level(5, 'timeout', f"会话 {session_id} 多次询问无响应，放弃询问")
                del self.pending_responses[session_id]
                return False

            try:
                # 发送询问指令
                inquiry_cmd = f"INQUIRE:SESSION:{session_id}"
                self.ser.write(f"{inquiry_cmd}\r\n".encode('utf-8'))
                print_level(4, 'iqry', f"询问会话 {session_id} 的执行情况 (第 {inquiry_count + 1} 次)")

                # 更新询问次数
                self.pending_responses[session_id] = (cmd, time.time(), inquiry_count + 1)

                # 等待5秒响应
                response_received = self.response_received.wait(5)

                if response_received:
                    # 收到响应，检查会话是否已处理
                    self.response_received.clear()
                    if session_id not in self.pending_responses:
                        print_level(5, 'success', f"会话 {session_id} 询问后收到有效响应")
                        return True
                    else:
                        print_level(5, 'invalid', f"会话 {session_id} 询问后收到无效响应，准备下次询问")
                else:
                    # 超时未收到响应，继续循环（进入下一次询问）
                    print_level(5, 'timeout', f"会话 {session_id} 第 {inquiry_count + 1} 次询问超时")

            except Exception as e:
                print_level(5, 'error', f"询问失败: {str(e)}")
                return




if __name__ == "__main__":
    # 列出可用串口
    ports_info = get_ports()
    for port, info in ports_info.items():
        if "USB-SERIAL CH340" in info["description"] and info["manufacturer"] == "wch.cn":
            print(port)

    # comm = Serial_Server()
    #
    # des_port = 'COM6'
    # des_baudrate = 115200
    # is_connected = comm.connect(des_port, baudrate=des_baudrate)
    # if is_connected:
    #     comm.start_communication()