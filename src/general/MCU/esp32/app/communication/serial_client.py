# UART通信模块
from machine import UART, Pin
import time, re
from app.hardware.stepper_motor import *


class Serial_Client:
    """UART通信管理器，封装所有UART相关操作"""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.uart = None
        self.stepper_motor = STEPPER_MOTOR(cfg._stepper_motor_En, cfg._stepper_motor_In1, cfg._stepper_motor_In2, cfg._stepper_motor_In3, cfg._stepper_motor_In4)

    def connect(self):
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
        except Exception as e:
            print(f"Error(Serial_Client::connect): {str(e)}")

    def disconnect(self):
        try:
            if self.uart:
                self.uart.deinit()
        except Exception as e:
            print(f"Error(Serial_Client::disconnect): {str(e)}")

    def _write(self, data):
        try:
            data = f"{data}\r\n".encode("utf-8")
            bytes_sent = self.uart.write(data)
        except Exception as e:
            print(f"Error(Serial_Client::_write): {str(e)}")

    def _read(self):
        try:
            data = self.uart.readline()
            if data:
                data = data.replace(b'\x00', b'')  # 移除NULL字符
                str_data = data.decode('utf-8').strip()
                if str_data:
                    return str_data
        except Exception as e:
            print(f"Error(Serial_Client::_read): {str(e)}")

    def _reading_thread(self):
        while True:
            try:
                recv = self._read()
                if recv is not None:
                    print(recv)
                    parts = recv.split(";")
                    for part in parts:
                        if "SESSION" in part:
                            session_num = part.replace("SESSION:", "")
                        elif "CMD" in part:
                            cmd = part.replace("CMD:", "")
                    self._session_execute(cmd)
                    self._write(f"SESSION:{session_num};STATUS:executed")
            except Exception as e:
                print(f"Error(Serial_Client::_reading_thread): {str(e)}")

    def _session_execute(self, cmd):
        try:
            if "RS" in cmd:
                # RS_R_2: 旋转位移台右（顺时针）转2步
                parts = cmd.split("_")
                direction = parts[1]
                steps = int(parts[2])
                if direction == "R":
                    self.stepper_motor.direction = 1
                elif direction == "L":
                    self.stepper_motor.direction = -1
                else:
                    raise ValueError("Invalid direction")
                self.stepper_motor.spin_steps(steps, duration=0.001)
        except Exception as e:
            print(f"Error(Serial_Client::_session_execute): {str(e)}")


