# 设备控制核心模块
from app.communication.uart import UARTCommunication
from app.hardware.led import LEDController
from app.logger import print_level
import time

class DeviceController:
    """设备控制器，协调所有模块工作"""
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.comm = None
        self.led = None
        self.running = False
        self.executed_sessions = {}  # 格式: {session_id: {"command": "on", "executed": True}}
        self.cfg.max_session_records = 100  # 最大保留记录数
        self.cleanup_interval = 120  # 清理间隔（秒），每2分钟检查一次
        self.last_cleanup_time = time.time()  # 上次清理时间
        
        # 初始化硬件和通信
        self._initialize_components()

    def _initialize_components(self):
        """初始化所有组件"""
        # 初始化LED
        self.led = LEDController(self.cfg.led_pin)
        
        # 初始化UART通信
        self.comm = UARTCommunication(self.cfg)
        # 初始化其他硬件可以在这里添加

    def _process_session_command(self, cmd):
        """处理带会话编号的指令"""
        try:
            parts = cmd.split(";")
            # session_command的形式为：SESSION:xxx;CMD:xxx
            if len(parts) == 2 and parts[0].startswith("SESSION:") and parts[1].startswith("CMD:"):
                session_id = int(parts[0].split(":")[1])
                actual_cmd = parts[1].split(":")[1]
                
                print_level(4, 'cmd: session', f"处理会话 {session_id} 的指令: {actual_cmd}")
                
                # 记录该会话的执行状态
                self.executed_sessions[session_id] = {
                    "command": actual_cmd,
                    "executed": False
                }
                
                # 执行指令并获取响应
                response_msg, executed = self._execute_command(actual_cmd)
                
                # 更新该会话的执行状态
                self.executed_sessions[session_id].update({
                    "executed": executed
                })
                print_level(6, 'rslt', "cmd处理状态: {executed}")
                
                # 发送响应
                self.comm.send_response(session_id, response_msg)
                return True
        except (ValueError, IndexError) as e:
            error_msg = f"SESSION:ERROR;MSG:Invalid command format - {str(e)}"
            self.comm.send_data(error_msg)
            print_level(1, 'error: session', f"解析指令错误: {str(e)}")
        return False

    def _process_inquiry(self, cmd):
        """处理询问指令"""
        try:
            # 标准格式：INQUIRE:SESSION:xxx
            parts = cmd.split(":")
            if len(parts) == 3 and parts[0] == "INQUIRE" and parts[1] == "SESSION":
                session_id = int(cmd.split(":")[2])
                
                print_level(4, 'cmd: inquiry', f"收到会话 {session_id} 的询问")
                
                # 检查该会话是否存在于执行记录中
                if session_id in self.executed_sessions:
                    # 会话存在于记录中
                    session_data = self.executed_sessions[session_id]
                    if session_data["executed"] is True:
                        response_msg = f"SESSION:{session_id};STATUS:EXECUTED;MSG:Success"
                        self.comm.send_response(session_id, response_msg)
                        print_level(6, 'rslt', f"会话 {session_id} 已执行完")
                    else:
                        response_msg = f"SESSION:{session_id};STATUS:RETRYING;MSG:Not executed properly, retrying..."
                        self.comm.send_response(session_id, response_msg)
                        full_cmd = f"SESSION:{session_id};CMD:{session_data['command']}"
                        self._process_session_command(full_cmd)
                        print_level(6, 'rslt', f"会话 {session_id} 未正常执行完毕，正在重试")
                else:
                    # 会话不存在于记录中
                    response_msg = f"SESSION:{session_id};STATUS:NOT_FOUND;MSG:Please resend command"
                    self.comm.send_data(msg)
                    print_level(5, 'rslt', f"会话 {session_id} 不存在于记录中，请重新发送指令...")
                
        except (ValueError, IndexError) as e:
            error_msg = f"SESSION:ERROR;MSG:Invalid inquiry format - {str(e)}"
            self.comm.send_data(error_msg)
            print_level(1, 'error: inquiry', f"解析指令错误: {str(e)}")
        return False

    def _execute_command(self, cmd, reexecute=False):
        """执行具体指令"""
        processed_cmd = cmd.strip().lower()
        action = "重新执行" if reexecute else "执行"
        
        if processed_cmd.startswith("led off"):
            self.led.off()
            msg = f"LED turned off{' (re-executed)' if reexecute else ''}"
            executed = True
            print_level(5, 'exec', f"{action}指令: LED已关闭")
            return msg, executed
        elif processed_cmd.startswith("led on"):
            self.led.on()
            msg = f"LED turned on{' (re-executed)' if reexecute else ''}"
            executed = True
            print_level(5, 'exec', f"{action}指令: LED已点亮")
            return msg, executed
        else:
            msg = f"Unknown command: {processed_cmd}"
            executed = True
            print_level(5, 'exec', f"{action}指令: {msg}")
            return msg, executed

    def _process_legacy_command(self, cmd):
        """处理普通指令（兼容旧格式，转换为标准化格式）"""
        # 自动分配临时会话ID
        temp_session = int(time.time() % 10000)  # 简单生成临时会话ID
        standard_cmd = f"SESSION:{temp_session};CMD:{cmd}"
        print_level(4, 'cmd: legc', f"转换旧格式指令为标准格式: {standard_cmd}")
        return self._process_session_command(standard_cmd)
    
    def _cleanup_expired_sessions(self):
        """清理过期会话记录：保留最近N条，或超过指定时间的记录"""
        current_time = time.time()
        
        # 仅在达到清理间隔时执行（避免频繁操作）
        if current_time - self.last_cleanup_time < self.cleanup_interval:
            return
        
        # 情况1：按容量清理（超过最大记录数时）
        if len(self.cfg.executed_sessions) > self.cfg.max_session_records:
            # 按会话ID排序（假设session_id递增，代表时间顺序）
            sorted_session_ids = sorted(self.executed_sessions.keys())
            # 计算需要删除的旧记录数量
            num_to_remove = len(self.executed_sessions) - self.max_session_records
            # 删除最旧的N条记录
            for session_id in sorted_session_ids[:num_to_remove]:
                del self.executed_sessions[session_id]
            print_level(2, 'clr', f"清理了 {num_to_remove} 条旧会话记录，当前保留 {self.max_session_records} 条")
        
        # 情况2：按时间清理（可选，例如删除超过24小时的记录）
        # 需在executed_sessions中添加"timestamp"字段记录时间
        # 此处略，可根据需求扩展
        
        # 更新最后清理时间
        self.last_cleanup_time = current_time
        
    def start_main_loop(self):
        """启动主循环"""
        self.running = True
        print_level(1, 'main', "主循环启动...")
        
        try:
            while self.running:
                # 定期清理过期会话记录
                self._cleanup_expired_sessions()
            
                # 读取指令
                recv = None
                if self.comm and self.comm.initialized:
                    recv = self.comm.receive_data()
                else:
                    print_level(2, 'uart', "等待UART初始化完成...")
                    time.sleep(1)
                    continue
                
                # 根据指令进行操作
                if recv is not None:
                    print_level(3, 'recv', f"收到指令: {recv}")
                    
                    # 处理不同类型的指令
                    if recv.startswith("SESSION:"):
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
                            elif part.startswith("CMD:"):
                                status = part.split(":")[1]
                        self._process_session_command(recv)
                    else:
                        self._process_legacy_command(recv)
                
                time.sleep(0.01)
                
        except Exception as e:
            print_level(1, 'main', f"主循环错误: {e}")
        finally:
            print_level(1, 'main', f"主循环错误: {e}")
            self.cleanup()

    def stop_main_loop(self):
        """停止主循环"""
        self.running = False
        print_level(1, 'main', "主循环已停止")

    def cleanup(self):
        """清理资源"""
        self.stop_main_loop()
        if self.led:
            self.led.off()  # 确保LED关闭
        if self.comm:
            self.comm.close()  # 关闭UART
        print_level(1, 'main', "资源已清理")