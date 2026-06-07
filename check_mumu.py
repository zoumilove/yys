import os
import subprocess

# MuMu模拟器ADB路径
MUMU_PATHS = [
    "D:\\mumu\\MuMuPlayer\\nx_main\\adb.exe",
    "C:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe",
    "D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe",
]
LD_PATH = "C:\\leidian\\LDPlayer9\\adb.exe"

# 检查模拟器ADB路径
def find_adb():
    print("=== 检查模拟器安装 ===")
    if os.path.isfile(LD_PATH):
        print(f"✓ 找到雷电模拟器 ADB: {LD_PATH}")
        return LD_PATH
    for path in MUMU_PATHS:
        if os.path.isfile(path):
            print(f"✓ 找到MuMu ADB: {path}")
            return path
    print("✗ 未找到模拟器ADB，尝试使用PATH中的adb")
    return "adb"

# 检查ADB设备
def check_adb_devices(adb_path):
    print("\n=== 检查ADB设备 ===")
    try:
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=5)
        print(result.stdout)
        lines = [l for l in result.stdout.strip().splitlines()[1:] if l.strip()]
        devices = [l.split()[0] for l in lines if len(l.split()) == 2 and 'offline' not in l]
        if devices:
            print(f"✓ 检测到 {len(devices)} 个设备: {devices}")
        else:
            print("✗ 未检测到已连接设备")
        return devices
    except Exception as e:
        print(f"✗ ADB命令执行失败: {e}")
        return []

# 自动扫描MuMu端口并连接（起始端口不固定，+32，扫描42个）
def scan_mumu_ports(adb_path):
    print("\n=== 扫描MuMu端口（16384起，+32，共42个）===")
    found = []
    for port in range(16384, 16384+32*42, 32):
        ip = f"127.0.0.1:{port}"
        try:
            result = subprocess.run(
                [adb_path, "connect", ip],
                capture_output=True, text=True, timeout=3
            )
            out = result.stdout.strip()
            if 'connected' in out.lower() and 'cannot' not in out.lower():
                print(f"✓ 端口 {port} 连接成功: {out}")
                found.append(port)
            else:
                print(f"  端口 {port}: {out}")
        except Exception as e:
            print(f"  端口 {port}: {e}")
    if not found:
        print("✗ 未找到可用的MuMu模拟器端口")
    return found

# 检查指定端口是否开放（通过netstat）
def check_port_open(port):
    try:
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True, timeout=5
        )
        return str(port) in result.stdout
    except:
        return False

if __name__ == "__main__":
    adb_path = find_adb()

    # 先检查已有设备
    devices = check_adb_devices(adb_path)

    # 如果没有设备，尝试扫描MuMu端口
    if not devices:
        ports = scan_mumu_ports(adb_path)
        if ports:
            print(f"\n已连接端口: {ports}")
            check_adb_devices(adb_path)

    print("\n=== 检查完成 ===")
