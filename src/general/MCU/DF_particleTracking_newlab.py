# -*- coding: utf-8 -*-
"""
Created on Fri May 05 09:57:21 2017

@author: wmd22
"""
from nplab.datafile import DataFile



from nplab.instrument.spectrometer.seabreeze import OceanOpticsSpectrometer
# from nplab.instrument.light_sources.cube_laser import CubeLaser
from nplab.instrument.stage.prior import ProScan
from nplab.instrument.camera.lumenera import LumeneraCamera 
from nplab.instrument.spectrometer.spectrometer_aligner import SpectrometerAligner
from nplab.instrument.camera.camera_with_location import CameraWithLocation
from nplab.instrument.shutter.BX51_uniblitz import Uniblitz

from nplab.utils.array_with_attrs import ArrayWithAttrs

from particle_tracking_app.particle_tracking_wizard import TrackingWizard
import numpy as np
import time

import threading
# from TCP_Server import *
# import socket
from serial_server import *
from Tango import *

comm = Serial_Server()
comm.connect("COM14", "RS")
comm.main_loop()

# stage = ProScan("COM3", hardware_version = 2)
stage = Tango(port="COM9") # 1
cam = LumeneraCamera(1) # 1
# # cam.show_gui(True)
spec = OceanOpticsSpectrometer(0) # 1

CWL = CameraWithLocation(cam,stage) # 1
# CWL = CameraWithLocation(cam)
CWL.show_gui(blocking =False) # 1

# stage.show_gui(blocking = False) 
spec.show_gui(blocking = False) # 1
spec.set_integration_time(1000) # 1
spec.set_tec_temperature(-20) # 1

alinger = SpectrometerAligner(spec,stage) # 1
equipment_dict = {'spectrometer':spec, 
                    'alinger':alinger} # 1

wizard = TrackingWizard(CWL,equipment_dict,task_list = ['CWL.thumb_image']) # 1
# wizard = TrackingWizard(cam,equipment_dict,task_list = ['CWL.thumb_image'])
wizard.data_file.show_gui(blocking = False) # 1
wizard.show() # 1

def linear_scan(axis='x', step = 1, range_length=20, exposure=10, name='QDs_PL'):
    
    if axis =='x':
        x=step
        y=0
    elif axis =='y':
        x=0
        y=step
    else:
        raise Exception('Has to be specific about the axis!')
        
    new_group = spec.create_data_group(name)
    spec.set_integration_time(exposure)
    for i in range(range_length):
        stage.move_rel([x, y, 0])
        save_spectrum(name, new_group)      

def save_spectrum(name, group):
    # meta_data = spec.get_metadata(property_names=spec.metadata_property_names)
    metadata = spec.metadata
    attrs={'description':str('description')}
    metadata.update(attrs)
    if spec.averaging_enabled == True:
        spectrum = spec.read_averaged_spectrum(new_deque = new_deque)
    else:
        spectrum = spec.read_spectrum()
    group.create_dataset(name=name, data=spectrum, attrs=metadata)

def scan_z(steps_num=20, name='scan_z'):
    new_group = spec.create_data_group(name)
    for i in range(steps_num):
        stage.sm("b1")
        spectrum_name = name + f'-{i}'
        save_spectrum(spectrum_name, new_group)
        print(f"点 {i} / {steps_num-1} 采集完成")

def line_scan(axis='x', step=2, range_val=100, exposure=500, name='hBN_line_scan', check_freq=None, just_move=False, start_point='center'):
    """
    执行一维直线扫描，可选择沿X轴或Y轴
    
    参数:
    axis (str): 扫描轴，'x' 或 'y'
    step (float): 扫描步长
    range_val (float): 扫描总范围
    exposure (int): 曝光时间（毫秒）
    name (str): 数据组名称
    check_freq (int): 检查频率，每隔多少步提示用户确认
    just_move (bool): 是否仅移动不采集数据
    start_point (str): 起始点位置，'center' 或 'corner'
    """
    # 确保所有数组使用浮点数类型
    range_val = float(range_val)
    step = float(step)
    initial_position_rel = np.zeros(3, dtype=float)  # 初始位置
    current_position = np.zeros(3, dtype=float)  # 当前位置追踪
    
    if not just_move:
        new_group = spec.create_data_group(name)
        print(f"创建数据组: {name}")
        spec.set_integration_time(exposure)
        print(f"设置积分时间: {exposure} ms")
    
    # 计算步数并确保为整数（向上取整）
    step_times = int(np.ceil(range_val / step))
    
    # 确定扫描轴的索引
    axis_idx = 0 if axis.lower() == 'x' else 1
    
    if start_point == 'center':
        # 移动到扫描区域起点（中心左侧或下侧）
        start_move = np.zeros(3, dtype=float)
        start_move[axis_idx] = -range_val / 2
        stage.move_rel(start_move)
        current_position += start_move
        print(f"移动到起始点: {axis.upper()}方向偏移量 == {start_move[axis_idx]}")
    elif start_point == 'corner':
        pass  # 假设当前位置已经是起点
    else:
        print("start_point 必须是 'center' 或 'corner'")
        return
    
    try:
        # 沿指定轴进行扫描
        for i in range(step_times):
            # 移动到下一个点
            point_move = np.zeros(3, dtype=float)
            point_move[axis_idx] = step
            stage.move_rel(point_move)
            current_position += point_move
            
            if not just_move:
                spectrum_name = name + f'-{axis}{i}'
                save_spectrum(spectrum_name, new_group)
                print(f"点 {i} / {step_times-1} 采集完成")
            else:
                user_input = input(f"点 {i} / {step_times-1} 已到达。按Enter继续，输入q退出: ")
                if user_input.lower() == 'q':
                    raise KeyboardInterrupt
            
            # 检查是否需要用户确认
            if check_freq is not None and not just_move and (i+1) % check_freq == 0 and i < step_times - 1:
                # 回到初始位置
                move_to_initial = initial_position_rel - current_position
                stage.move_rel(move_to_initial)
                
                user_input = input(f"点 {i+1}/{step_times} 扫描完成。按Enter继续，输入q退出: ")
                
                # 回到当前点
                stage.move_rel(-move_to_initial)
                
                if user_input.lower() == 'q':
                    raise KeyboardInterrupt
        
        # 扫描完成后回到初始位置
        move_to_initial = initial_position_rel - current_position
        stage.move_rel(move_to_initial)
        print(f"直线扫描完成，已回到初始位置")
        
    except KeyboardInterrupt:
        # 计算从当前位置回到初始位置的偏移
        move_to_initial = initial_position_rel - current_position
        stage.move_rel(move_to_initial)
        print(f"扫描已中断，已回到初始位置")
        
def mapping(step_xy=[2, 2], range_xy=[110, 130], exposure=500, name='hBN_afterSEM_mapping', check_time=None, just_move=True, point_now='center', stage=stage):
    stage.joystick_off()
    
    # 确保所有数组使用浮点数类型
    range_xy = np.array(range_xy, dtype=float)
    range_xy = range_xy/1000  # um转换为mm
    step_xy = np.array(step_xy, dtype=float)
    step_xy = step_xy/1000  # um转换为mm
    initial_position_rel = np.zeros(3, dtype=float)  # 初始位置，明确使用float
    current_position = np.zeros(3, dtype=float)  # 当前位置追踪，明确使用float
    
    if not just_move:
        new_group = spec.create_data_group(name)
        print(f"Create data group : {name}")
        spec.set_integration_time(exposure)
        print(f"Set integration time == {exposure}")
    
    # 计算步数并确保为整数（向上取整）
    step_times_xy = np.ceil(range_xy / step_xy).astype(int)
    
    if point_now == 'center':
        # 移动到扫描区域左下角
        corner_move_x = -1*range_xy[0]/2
        corner_move_y = -1*range_xy[1]/2
        corner_move = np.array([corner_move_x, corner_move_y, 0], dtype=float)
        stage.move_rel(corner_move)
        current_position += corner_move
        print(f"Move to corner: corner_move_x == {corner_move_x}, corner_move_y == {corner_move_y}")
    elif point_now == 'corner':
        pass
    else:
        print("Point now must be 'center' or '(left_bottom)corner'.")
        
    start_time = time.time()
    
    try:
        for i in range(step_times_xy[0]+1):
            if i != 0:
                # 移动到下一列
                column_move = np.array([step_xy[0], 0, 0], dtype=float)
                stage.move_rel(column_move)
                current_position += column_move
            
            if not just_move:
                new_column_group = new_group.create_group(f'x-{i}')
            
            # 扫描当前列
            for j in range(step_times_xy[1]+1):
                if j != 0: 
                    # 移动到下一个点
                    point_move = np.array([0, step_xy[1], 0], dtype=float)
                    stage.move_rel(point_move)
                    current_position += point_move
                
                if not just_move:
                    spectrum_name = name + f'-x{i}-y{j}'
                    save_spectrum(spectrum_name, new_column_group)
                    print(f"i: {i} in {step_times_xy[0]}, j: {j} in {step_times_xy[1]}")
                else:
                    user_input = input(f"按Enter继续，输入q退出: ")
                    if user_input.lower() == 'q':
                        raise KeyboardInterrupt
                
                now_time = time.time()
                during_time = now_time - start_time
                print(f"Time: {during_time:2f}")
                # 检查是否需要用户确认
                if check_time is not None and during_time >= check_time*60 is not None and not just_move:
                    # 回到初始位置
                    move_to_initial = initial_position_rel - current_position
                    stage.move_rel(move_to_initial)
                    
                    user_input = input(f"列 {i}/{step_times_xy[0]} 扫描完成。按Enter继续，输入j解锁joystick，输入q退出: ")
                    
                    if user_input.lower() == 'j':
                        stage.joystick_on()
                        user_input = input(f"joystick已解锁。按Enter继续扫描，输入q退出: ")
                        stage.joystick_off()
                        
                    # 回到当前列的位置
                    stage.move_rel(-move_to_initial)
                    
                    start_time = time.time()
                    if user_input.lower() == 'q':
                        raise KeyboardInterrupt
                        
            # 每行扫完后，回到行初始位置Y坐标
            row_reset = np.array([0, -1*step_times_xy[1]*step_xy[1], 0], dtype=float)
            stage.move_rel(row_reset)
            current_position += row_reset
            
            print(f"\n")
        else:
            move_to_initial = initial_position_rel - current_position
            stage.move_rel(move_to_initial)
            stage.joystick_on()
    except KeyboardInterrupt:
        # 计算从当前位置回到初始位置的偏移
        move_to_initial = initial_position_rel - current_position
        stage.move_rel(move_to_initial)
        stage.joystick_on()
        print(f"中断扫描，已回到初始位置")
    

def Rotation_Stage_move(degree, client_socket, timeout=10):
    rot_time = int(735*degree/5)
    velocity = 25
    print(f"R{rot_time},V{velocity},T{1}")
    start_time = time.time()
    is_sent = send_message(client_socket, initial_message=f"R{rot_time},V{velocity},T{1}")
    if not is_sent:
        return
    
    # 循环接收反馈，直到超时或收到完成消息
    while (time.time() - start_time) < timeout:
        try:
            # 接收消息（设置单次接收超时）
            recv_message = receive_message(client_socket, timeout=1)
            
            if not recv_message:
                continue
                
            # 验证消息时效性
            raw_message = validate_receive_message(recv_message, start_time)
            if raw_message == "Rotation Completed":
                print("收到设备完成反馈")
                return True
            else:
                print(f"收到非预期消息: {raw_message}")
                    
        except TimeoutError:
            # 单次接收超时，继续循环
            print("单次接收超时，继续等待...")
        except Exception as e:
            print(f"通信异常: {e}")
    
    # 超时处理
    print(f"等待设备反馈超时（{timeout}秒）")
    return False
    

def polarization(client_socket, step_degree=5, range_degree=[0, 360], exposure=1000, name = 'hBN_afterSEM'):
    new_group = spec.create_data_group(name)
    print(f"Create data group : {name}")
    spec.set_integration_time(exposure)
    print(f"Set integration time == {exposure}")
    
    degrees = range(range_degree[0], range_degree[1]+1, step_degree)
    
   
    for i, degree in enumerate(degrees):
        print(f"Rotation degree now: {degree}")
        if i != 0:
            # 发送旋转命令
            is_moved = Rotation_Stage_move(step_degree, client_socket)
            if not is_moved:
                return False
        spectrum_name = name + f'-d{str(degree)}'
        save_spectrum(spectrum_name, new_group)

def run_TCP(server_socket=None):
    if server_socket:
        server_socket.close()
    # 监听的 IP 地址和端口
    server_ip = '192.168.31.176'
    server_port = 7799
    
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
            print("无法查询端口占用信息")
    
        # 询问用户是否继续
        if not input("是否尝试继续启动服务器? (y/n): ").lower().startswith('y'):
            exit(1)
    
    # 创建 TCP 套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 设置套接字选项，允许地址重用
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Windows特定的keepalive参数
    server_socket.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60*1000, 30*1000))  # 1=启用，60秒无活动发送探测包，30秒间隔

    # 绑定地址和端口
    server_socket.bind((server_ip, server_port))
    
    # 开始监听
    server_socket.listen(5)
    print(f"服务器正在监听 {server_ip}:{server_port}")
    client_socket, client_address = accept_connections(server_socket)
    return server_socket, client_socket, client_address
    
def accept_connections(server_socket):
    try:
        def start_heartbeat(sock, interval=30):
            """启动心跳线程，定期发送心跳包"""
            import threading
            
            def heartbeat_loop():
                while True:
                    try:
                        time.sleep(interval)
                        sock.send(b"HEARTBEAT")
                        print("发送心跳包")
                    except Exception as e:
                        print(f"心跳发送失败: {e}")
                        break  # 退出线程，让主线程处理重连
            
            t = threading.Thread(target=heartbeat_loop, daemon=True)
            t.start()
            return t
        
        # 接受客户端连接
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket, client_address)
        start_heartbeat(client_socket)
        
    except KeyboardInterrupt:
        print("\n正在关闭服务器...")
    server_socket.close()
    return client_socket, client_address

# server_socket, client_socket, client_address = run_TCP()