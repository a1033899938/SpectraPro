@echo off
REM 调试输出
echo Starting batch file...


REM 确保 Anaconda 路径正确
echo Activating conda environment...
call D:\anaconda3\Scripts\activate.bat D:\anaconda3
call conda activate NanoPhotonics
if errorlevel 1 (
    echo Failed to activate conda environment...
    pause
    exit /b 1
)


REM 更改工作目录到 Python 脚本所在目录
cd /d D:\GitProject\SpectraPro\ui


REM 显示文件路径
echo Setting environment...
set PYTHONPATH=D:\GitProject\SpectraPro
echo Current path...:%PYTHONPATH%


REM 运行 Python 模块
python -m ui.main

if errorlevel 1 (
    echo Python script execution failed...
    pause
    exit /b 1
)

REM 保持命令提示符窗口打开
echo Script completed...
cmd /k
