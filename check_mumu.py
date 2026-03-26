import os
import subprocess

# 检查MuMu模拟器是否安装
def check_mumu_installation():
    print("=== 检查MuMu模拟器安装 ===")
    
    # 检查默认安装路径
    default_paths = [
        "C:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe",
        "C:\\Program Files (x86)\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe",
        "D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe",
        "D:\\Program Files (x86)\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe"
    ]
    
    for path in default_paths:
        if os.path.exists(path):
            print(f"✓ 找到MuMu ADB: {path}")
            return path
    
    print("✗ 未找到MuMu ADB")
    return None

# 检查ADB设备
def check_adb_devices():
    print("\n=== 检查ADB设备 ===")
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=5)
        print("ADB devices output:")
        print(result.stdout)
        if "device" in result.stdout:
            print("✓ 检测到ADB设备")
        else:
            print("✗ 未检测到ADB设备")
    except Exception as e:
        print(f"✗ ADB命令执行失败: {e}")

# 检查端口是否开放
def check_port(port):
    print(f"\n=== 检查端口 {port} ===")
    try:
        result = subprocess.run(
            ["netstat", "-ano"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        if str(port) in result.stdout:
            print(f"✓ 端口 {port} 已开放")
        else:
            print(f"✗ 端口 {port} 未开放")
    except Exception as e:
        print(f"✗ 端口检查失败: {e}")

if __name__ == "__main__":
    adb_path = check_mumu_installation()
    check_adb_devices()
    check_port(16384)  # 默认MuMu端口
    check_port(26944)  # 可能的其他端口
    check_port(28206)  # 可能的其他端口
    
    print("\n=== 检查完成 ===")
    print("请确保:")
    print(1. "MuMu模拟器已安装")
    print(2. "MuMu模拟器正在运行")
    print(3. "ADB服务已启动")
    print(4. "MuMu模拟器的ADB端口正确")