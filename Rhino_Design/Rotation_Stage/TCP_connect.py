import socket
import threading
import time


def is_port_available(ip, port):
    """检查指定IP和端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:
            temp_socket.bind((ip, port))
        return True
    except OSError as e:
        print(f"端口检查失败: {e}")
        return False


def handle_client(client_socket, client_address):
    """处理客户端连接"""
    print(f"已接受来自 {client_address} 的连接")

    try:
        # 发送欢迎消息
        client_socket.sendall('This is server'.encode())

        # 接收并验证第一个消息
        data = client_socket.recv(1024)
        if not data:
            print(f"客户端 {client_address} 未发送数据就关闭了连接")
            return

        first_message = data.decode()
        print(f"收到客户端 {client_address} 的第一条消息: {first_message}")

        # 检查消息是否包含"Hulab"
        if "Hulab" not in first_message:
            print(f"来自 {client_address} 的消息不包含'Hulab'，拒绝连接")
            # client_socket.sendall("Connection rejected: Message does not contain 'Hulab'".encode())
            return

        print(f"来自 {client_address} 的消息验证通过")

        # 创建接收和发送线程
        receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
        send_thread = threading.Thread(target=send_data, args=(client_socket,))

        # 设置为守护线程，主线程退出时自动终止
        receive_thread.daemon = True
        send_thread.daemon = True

        # 启动线程
        receive_thread.start()
        send_thread.start()

        # 等待线程结束
        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"处理客户端连接时出错: {e}")
    finally:
        # 确保客户端套接字关闭
        try:
            client_socket.close()
        except:
            pass
        print(f"与 {client_address} 的连接已关闭")


def receive_data(client_socket):
    """接收客户端数据"""
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("客户端关闭了连接")
                break
            print(f"收到: {data.decode()}")
        except Exception as e:
            print(f"接收数据时出错: {e}")
            break


def send_data(client_socket):
    """发送数据到客户端"""
    while True:
        try:
            message = input("输入要发送的消息 (输入'exit'退出): ")
            if message.lower() == 'exit':
                client_socket.close()
                break
            client_socket.sendall(message.encode())
        except Exception as e:
            print(f"发送数据时出错: {e}")
            break


# 监听的 IP 地址和端口
server_ip = '192.168.21.177'
server_port = 7788

# 检查端口是否可用
if not is_port_available(server_ip, server_port):
    print(f"端口 {server_port} 已被占用")

    # 提供更详细的端口占用信息
    try:
        import subprocess

        print("正在查询端口占用详情...")
        output = subprocess.check_output(f"netstat -ano | findstr :{server_port}", shell=True).decode()
        print("端口占用详情:")
        print(output)
    except Exception:
        print(f"无法查询端口占用信息")

    # 询问用户是否继续
    if not input("是否尝试继续启动服务器? (y/n): ").lower().startswith('y'):
        exit(1)

# 创建 TCP 套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 设置套接字选项，允许地址重用
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定地址和端口
server_socket.bind((server_ip, server_port))

# 开始监听
server_socket.listen(1)
print(f"服务器正在监听 {server_ip}:{server_port}")

try:
    while True:
        # 接受客户端连接（不再验证客户端IP）
        client_socket, client_address = server_socket.accept()

        # 处理客户端连接
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )
        client_thread.daemon = True
        client_thread.start()

except KeyboardInterrupt:
    print("\n正在关闭服务器...")
finally:
    # 确保服务器套接字关闭
    server_socket.close()
    print(f"服务器已关闭，端口 {server_port} 已释放")