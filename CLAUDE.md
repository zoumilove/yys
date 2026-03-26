# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
本文档为 Claude Code 提供代码库操作指导。

## Project Overview / 项目概述

This is an automation script for the game **阴阳师 (Onmyoji/YYS)**. It uses image recognition (OpenCV template matching) to automate game tasks like dungeons, exploration, and events. Forked from lisai9093/YYS.
这是一个阴阳师游戏自动化脚本，通过图像识别（OpenCV 模板匹配）自动执行副本、探索等活动。

## Commands / 命令

### Running the Script / 运行脚本
- **Windows**: Double-click `start.bat` or run `python main.py`
  **Windows**: 双击 `start.bat` 或运行 `python main.py`
- **With game override**: `python main.py -game yys`
  **指定游戏**: `python main.py -game yys`

### Building Executable / 打包可执行文件
```batch
build.bat
```
Or manually / 手动: `pyinstaller yys_script.spec --clean`
Output / 输出: `dist/yys_script.exe`

### Dependencies / 依赖
```
pip install pyqt6 opencv-python numpy mss pyautogui pyinstaller
```

## Architecture / 架构

```
main.py          # PyQt6 GUI - creates tabs, threads, handles UI events
action.py        # Core automation layer - screenshot, touch, swipe, image matching
yys/yys.py       # Game-specific Worker class with task functions (dungeon, exploration, etc.)
yys/png/         # Template images for OpenCV matching (tiaozhan.png, jiangli.png, etc.)
config.ini       # Thread count, debug mode, game name
```

### Core Flow / 核心流程
1. `main.py` loads game module dynamically (`importlib.import_module(game_name)`)
   `main.py` 通过动态导入加载游戏模块
2. Each tab runs a `Worker` instance in a separate QThread
   每个标签页在独立 QThread 中运行 Worker 实例
3. Worker calls game-specific functions that use `action.py` primitives:
   Worker 调用游戏特定函数，使用 `action.py` 底层接口：
   - `action.screenshot(thread_id)` - capture screen (ADB or desktop) / 截图（ADB 或桌面）
   - `action.locate(screen, template)` - find template in screen via cv2.matchTemplate / 模板匹配
   - `action.touch(pos, thread_id)` - click (ADB tap or pyautogui) / 点击
   - `action.cheat(pos, w, h)` - add random offset to avoid detection / 随机偏移防检测

### Dual Backend / 双后端支持
- **ADB mode**: Connects to Android emulator via `adb shell screencap` and `adb shell input tap`
  **ADB 模式**: 通过 ADB 连接安卓模拟器
- **Desktop mode**: Uses `mss` for screenshot and `pyautogui` for click; window must be at top-left of primary screen
  **桌面模式**: 使用 mss 截图 + pyautogui 点击，窗口需放在主屏幕左上角

### Game Image Templates / 游戏图像模板
Templates in `yys/png/` are matched with 0.95 threshold. Key templates:
`yys/png/` 下的模板以 0.95 阈值匹配。关键模板：
- `tiaozhan`, `tiaozhan2`, `tiaozhan3` - challenge buttons / 挑战按钮
- `jiangli`, `jiangli2` - rewards / 奖励结算
- `hd_tz` - **activity challenge** (must be re-captured each event) / **活动挑战**（每期活动需重新截图）
- `notili` - insufficient stamina / 体力不足
- `guding` - fixed position marker on exploration map / 探索地图固定位置标记

When a new event tower (爬塔) starts, recapture `hd_tz.png` by: run screenshot function → manually crop the challenge button → save to `yys/png/hd_tz.png`.
新活动爬塔开始时，更新 `hd_tz.png`：运行截图功能 → 手动裁剪挑战按钮区域 → 保存到 `yys/png/hd_tz.png`。

### Game Settings / 游戏设置
Disable "战斗结算个性化" in-game to prevent stuck on completion screen.
关闭游戏内"战斗结算个性化"选项，避免卡在结算界面。

## Configuration / 配置

`config.ini`:
- `Nthread` - number of concurrent game tabs (default 5) / 并发标签页数量（默认 5）
- `debug` - enable debug mode / 开启调试模式
- `game` - game folder name (default `yys`) / 游戏文件夹名（默认 `yys`）

## Supported Tasks / 支持的任务

Each task function is defined in `Worker.func` list with description and default count:
每个任务函数在 `Worker.func` 列表中定义，包含描述和默认次数：
0. Screen capture (debug) / 屏幕截图（调试）
1. 寮突 (guild battle) / 寮突（公会战）
2. 御魂/御灵/活动爬塔 (souls/dungeon/event tower) / 御魂/御灵/活动爬塔
3. 探索单刷 (exploration solo) / 探索单刷
4. 契灵单刷 (soul summoning solo) / 契灵单刷
5. 御魂司机 (souls driver) / 御魂司机
6. 御魂打手 (souls fighter) / 御魂打手
7. 探索组队司机 (exploration driver) / 探索组队司机
8. 探索组队打手 (exploration fighter) / 探索组队打手
