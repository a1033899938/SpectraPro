"""
Author: Junjie-Xie
Updated: 2025/9/1
Functions: 
"""
from machine import Pin, PWM
import time, math

class STEPPER_MOTOR:
    """步进电机控制器，封装LED相关操作"""

    def __init__(self, pin_En, pin_In1, pin_In2, pin_In3, pin_In4, freq=10000, current_ratio=1):
        self.pin_en = Pin(pin_En, Pin.OUT)
        self.pin_in1 = Pin(pin_In1, Pin.OUT)
        self.pin_in2 = Pin(pin_In2, Pin.OUT)
        self.pin_in3 = Pin(pin_In3, Pin.OUT)
        self.pin_in4 = Pin(pin_In4, Pin.OUT)

        # 初始化PWM
        self.pwm_in1 = PWM(self.pin_in1, freq=freq, duty=0)
        self.pwm_in2 = PWM(self.pin_in2, freq=freq, duty=0)
        self.pwm_in3 = PWM(self.pin_in3, freq=freq, duty=0)
        self.pwm_in4 = PWM(self.pin_in4, freq=freq, duty=0)

        # 启用电机
        self.pin_en.on()

        # 电流控制参数
        self.current_ratio = current_ratio
        self.idle_current_ratio = 0  # 空闲时电流设为0（无电流）
        self.direction = 1
        self.is_moving = False
        self.microsteps_per_cycle = 10
        self.step_index = 0

    def _set_microstep(self, step_angle, moving=True):
        """【内部方法】设置微步角度，控制电机线圈电流（核心驱动逻辑）"""
        self.is_moving = moving

        # 空闲状态且无保持电流时，关闭所有PWM
        if not moving and self.idle_current_ratio == 0:
            self.pwm_in1.duty(0)
            self.pwm_in2.duty(0)
            self.pwm_in3.duty(0)
            self.pwm_in4.duty(0)
            return

        # 根据当前方向调整角度（实现顺时针/逆时针切换）
        adjusted_angle = step_angle

        # 计算正弦/余弦值（用于2相4线步进电机的微步电流分配）
        angle_rad = adjusted_angle * 2 * math.pi
        a = math.sin(angle_rad)
        b = math.cos(angle_rad)

        # 选择电流比例（运行时用设定值，空闲时用低电流）
        current_ratio = self.current_ratio if moving else self.idle_current_ratio

        # 过零点电流优化（避免电机卡顿，过零点降低10%~40%电流）
        abs_angle = abs(adjusted_angle % 1)  # 取0~1范围的绝对值（周期内角度）
        if 0.45 < abs_angle < 0.55 or 0.95 < abs_angle or abs_angle < 0.05:
            current_reduction = 0.8  # 过零点电流衰减40%
        else:
            current_reduction = 1  # 非过零点衰减10%

        # 计算PWM占空比（0~1023，ESP32/ESP8266 PWM默认精度）
        duty_a_plus = max(0, min(1023, int((a if a > 0 else 0) * 1023 * current_ratio * current_reduction)))
        duty_a_minus = max(0, min(1023, int((-a if a < 0 else 0) * 1023 * current_ratio * current_reduction)))
        duty_b_plus = max(0, min(1023, int((b if b > 0 else 0) * 1023 * current_ratio * current_reduction)))
        duty_b_minus = max(0, min(1023, int((-b if b < 0 else 0) * 1023 * current_ratio * current_reduction)))

        # 应用PWM占空比到电机引脚
        self.pwm_in1.duty(duty_a_plus)
        self.pwm_in2.duty(duty_a_minus)
        self.pwm_in3.duty(duty_b_plus)
        self.pwm_in4.duty(duty_b_minus)

    def spin_single_step(self, duration=0.0005):
        """顺时针连续旋转（松开按键时需调用stop()停止）"""
        self.is_moving = True
        # 计算当前微步角度并驱动
        angle = self.step_index / self.microsteps_per_cycle
        self._set_microstep(angle, moving=True)
        # 更新微步索引（循环递增，避免溢出）
        if self.direction == 1:
            self.step_index = (self.step_index + 1) % self.microsteps_per_cycle
        else:
            self.step_index = (self.step_index - 1) % self.microsteps_per_cycle
        # 控制旋转速度（延时越短，速度越快，需根据电机负载调整）
        time.sleep(duration)
        # 完成后停止电机
        self.stop()

    def spin_steps(self, steps, duration=0.0005):
        """顺时针旋转指定步数（精确控制，完成后自动停止）
        Args:
            steps: 旋转步数（1步=1微步，需根据需求换算成实际角度）
            duration: 每步延时（控制速度）
        """
        if steps <= 0:
            print("步数需为正整数")
            return
        self.is_moving = True
        print(f"{'顺' if self.direction==1 else '逆'}旋转{steps}步")
        for _ in range(steps):
            angle = self.step_index / self.microsteps_per_cycle
            self._set_microstep(angle, moving=True)
            if self.direction == 1:
                self.step_index = (self.step_index + 1) % self.microsteps_per_cycle
            else:
                self.step_index = (self.step_index - 1) % self.microsteps_per_cycle
            time.sleep(duration)
        # 完成后停止电机
        self.stop()

    def stop(self):
        """停止电机并切断电流（进入低功耗状态）"""
        self.is_moving = False
        # 强制空闲电流为0，确保 _set_microstep 不生成电流
        original_idle_ratio = self.idle_current_ratio  # 暂存原配置（可选，如需恢复）
        self.idle_current_ratio = 0
        self._set_microstep(0, moving=False)
        # 恢复原空闲电流比例（若后续需要保持位置，可加这行；仅停止则无需）
        # self.idle_current_ratio = original_idle_ratio

        # 手动关闭PWM（顺序调整：先关PWM，再确保无残留）
        self.pwm_in1.duty(0)
        self.pwm_in2.duty(0)
        self.pwm_in3.duty(0)
        self.pwm_in4.duty(0)
        print("电机已停止，电流已切断")

    def set_idle_current(self, ratio):
        """设置空闲时电流比例（0~1，用于电机保持位置，0=无保持力）"""
        if 0 <= ratio <= 1:
            self.idle_current_ratio = ratio
            print(f"空闲电流比例已设置为: {ratio}")
        else:
            print("电流比例需在0~1之间")