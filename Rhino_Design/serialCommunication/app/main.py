# 主程序入口
from app.controller import DeviceController
from app.config import Config


def main():
    try:
        # 初始化配置
        cfg = Config()
        
        # 初始化设备控制器
        controller = DeviceController(cfg)
        
        # 启动主循环
        controller.start_main_loop()
        
    except KeyboardInterrupt:
        print("用户中断程序")
    finally:
        # 无论程序正常结束还是异常退出，都确保清理资源
        if 'controller' in locals():
            controller.cleanup()
            print_level(1, "main: uart", f"清理资源完毕")

if __name__ == "__main__":
    main()
