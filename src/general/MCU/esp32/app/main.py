# 主程序入口
from app.communication.serial_client import *
from app.config import Config
import time

def main():
    try:
        # 初始化配置
        cfg = Config()
        ser = Serial_Client(cfg)
        ser.connect()
        while True:
            ser._reading_thread()
    except KeyboardInterrupt:
        print("用户中断程序")
    except Exception as e:
        print(f"Error(main): {str(e)}")
    finally:
        pass

if __name__ == "__main__":
    main()
