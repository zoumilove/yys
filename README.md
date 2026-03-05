源码地址 https://github.com/lisai9093/YYS.git
本人根据自己习惯 做了些修改
大家有兴趣研究的 可以去看lisai9093大佬的源码哈

# 1. 安装python
运行python-3.9.5-amd64.exe进入安装 记得勾选左下角ADD path 选项添加环境变量

# 2. 配置程序环境
安装完后打开终端win+r 输入cmd 或者在电脑左下角直接搜索cmd
分别执行以下指令 复制粘贴到终端执行即可
## 这个是将镜像源替换为阿里的 这样执行后续指令 下载会更快
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/<br/>

## 这些是运行所需的库
pip install opencv-python<br/>
pip install pyautogui<br/>
pip install mss<br/>
pip install pyqt6<br/>
pip install cv2<br/>


# 3. 运行脚本
Windows系统直接双击运行`start.bat`。推荐使用雷电模拟器因为会自动设置ADB地址，MuMu模拟器会相对麻烦一些需要手动输入ADB端口。<br/>

在挂机刷活动爬塔的时候 每一期都需要重新截取活动挑战按钮的图片 通过 运行脚本界面0 屏幕截图在这个截取的图内自己另外截一次图qq截图啊微信截图啊 截取挑战按钮部分字样 然后另存到yys/png文件夹下 替换掉hd_tz.png这张图片

# 4. 游戏设置
关闭游戏里的“战斗结算个性化”选项，否则刷御魂副本会卡在结算界面：
<img width="596" alt="image" src="https://github.com/user-attachments/assets/c0bc662c-682e-4200-8fed-6df0cff03666" />
