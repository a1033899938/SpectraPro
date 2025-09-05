"""
Author: Junjie-Xie
Updated: 2025/7/30
Functions: 所有连接到ESP32的硬件的基类，提供统一接口和通用功能
"""
import time
from app.formatted_time import *

# 设备状态常量（避免魔法数字）
DEVICE_DISCONNECTED = 0  # 未连接
DEVICE_INITIALIZING = 1  # 初始化中
DEVICE_READY = 2         # 就绪
DEVICE_ERROR = 3         # 错误
DEVICE_BUSY = 4          # 忙碌中


class Device:
    """硬件设备基类，所有外设（传感器、执行器等）需继承此类"""

    def __init__(self, device_id, name="UnknownDevice", params=None):
        """
        初始化设备
        :param device_id: 设备唯一标识（如"I2C_1"、"UART_3"）
        :param name: 设备名称（如"DS18B20"、"ServoMotor"）
        :param params: 设备参数字典（如波特率、地址、引脚等）
        """
        self.device_id = device_id  # 唯一ID，用于区分不同设备
        self.name = name            # 设备名称
        self.params = params or {}  # 设备参数（默认空字典）
        self._status = DEVICE_DISCONNECTED  # 初始状态：未连接
        self._error_info = ""       # 错误信息
        self._last_updated = 0      # 最后一次状态更新时间（毫秒）

    def __str__(self):
        """字符串格式化设备信息"""
        return f"{self.name} (ID: {self.device_id}) - {self.status}"

    @property
    def status(self):
        """将状态常量转换为可读字符串"""
        status_map = {
            DEVICE_DISCONNECTED: "DISCONNECTED",
            DEVICE_INITIALIZING: "INITIALIZING",
            DEVICE_READY: "READY",
            DEVICE_ERROR: "ERROR",
            DEVICE_BUSY: "BUSY"
        }
        return status_map.get(self._status, "UNKNOWN")

    @property
    def info(self):
        """
        获取设备基本信息
        :return: 包含设备信息的字典
        """
        return {
            "device_id": self.device_id,
            "name": self.name,
            "status": self._status,
            "status_str": self.status,
            "last_updated": self._last_updated,
            "error_info": self._error_info
        }

    @property
    def error_info(self):
        """获取最后一次错误信息（只读）"""
        return self._error_info

    def initialize(self):
        """
        初始化设备（需子类实现具体逻辑）
        :return: 成功返回True，失败返回False
        """
        self._status = DEVICE_INITIALIZING
        self._error_info = ""  #　确保本次初始化过程的错误信息只反映当前状态
        try:
            # 示例：检查必要参数是否存在
            if not self._check_required_params():
                raise ValueError("[initialize] 缺少必要的设备参数")

            # 子类应重写此方法，实现硬件初始化（如引脚配置、通信握手等）
            self._initialize()

            # 初始化成功后更新状态
            self._status = DEVICE_READY
            self._last_updated = formatted_time(time.time())
            return True
        except Exception as e:
            self._error_info = f"[initialize] 初始化失败: {str(e)}"
            self._status = DEVICE_ERROR
            self._last_updated = formatted_time(time.time())
            return False

    def _check_required_params(self):
        """
        检查设备必要参数（子类可重写）
        :return: 存在必要参数返回True，否则False
        """
        # 示例：默认无需参数，子类可根据需求添加检查（如I2C设备需检查"address"）
        return True

    def _initialize(self):
        # 子类应重写此方法，实现具体初始化逻辑
        return None

    def read_data(self):
        """
        读取设备数据（需子类实现）
        :return: 数据（格式由子类定义）或None（失败）
        """
        if self._status != DEVICE_READY:
            self._error_info = f"无法读取：设备状态为{self.status}"
            return None

        self._status = DEVICE_BUSY
        try:
            data = self._read_data()  # 子类应重写此方法，实现具体数据读取逻辑
            self._status = DEVICE_READY
            self._last_updated = formatted_time(time.time())
            return data
        except Exception as e:
            self._status = DEVICE_ERROR
            self._error_info = f"读取失败: {str(e)}"
            return None

    def _read_data(self):
        # 子类应重写此方法，实现具体数据读取逻辑
        return None

    def write_command(self, command, params=None):
        """
        向设备发送指令（需子类实现）
        :param command: 指令名称（如"SET_POWER"、"MOVE"）
        :param params: 指令参数（可选）
        :return: 成功返回True，失败返回False
        """
        if self._status != DEVICE_READY:
            self._error_info = f"无法发送指令：设备状态为{self.status}"
            return False

        self._status = DEVICE_BUSY
        try:
            # 子类应重写此方法，实现具体指令发送逻辑
            result = True  # 示例：实际结果由子类填充
            self._status = DEVICE_READY
            self._last_updated = formatted_time(time.time())
            return result
        except Exception as e:
            self._status = DEVICE_ERROR
            self._error_info = f"指令发送失败: {str(e)}"
            return False

    def _write_command(self):
        # 子类应重写此方法，实现具体数据发送逻辑
        return None

    def reset(self):
        """
        重置设备（默认实现为重新初始化，子类可重写）
        :return: 成功返回True，失败返回False
        """
        # 强制设置为断开状态，中断可能的阻塞操作
        self._status = DEVICE_DISCONNECTED
        return self.initialize()


if __name__ == "__main__":
    d = Device('led1', name="UnknownDevice", params=None)
    d.initialize()
    d.write_command("on")
    print(f"d: {d}")
    print(f"d._status: {d._status}")  # 状态（序号）：私有变量
    print(f"d.status: {d.status}")  # 状态（序号）对应字符
    print(f"d.info: {d.info}")
    print(f"d.error_info: {d.error_info}")