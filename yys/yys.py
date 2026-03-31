import sys,random,time
from PyQt6.QtCore import QObject,pyqtSignal
import action
from enum import Enum
import cv2,pyautogui
import numpy as np

class Worker(QObject):
    finished = pyqtSignal(int)
    progress = pyqtSignal(str,int)
    
    def __init__(self,thread_id=None,index=None,cishu_max=None):
        super().__init__()
        self.game_name='yys'

        #事件点击名
        self.click_name = {
            'qiling_tz': '挑战',
            'qiling_jl': '奖励结算',
            'qiling_sj': '点击空白区域',
            'qiling_fq': '放弃结契',
            'lt_xz': '选择',
            'lt_ks': '开始',
            'lt_jg': '进攻',
            'lt_jl': '结算',
        }

        #随机范围
        self.random_time = {
            'qiling_tz': [50, 150],
            'qiling_jl': [60, 150],
            'qiling_sj': [100, 150],
            'qiling_fq': [100, 150],
            'lt_ks': [100, 150],
            'lt_xz': [100, 150],
            'lt_jg': [100, 150],
            'lt_jl': [100, 150],
        }

        self.event_list = {
            'qiling':['qiling_tz','qiling_sj','qiling_fq','qiling_jl'],
            'liaotu':['lt_xz','lt_ks','lt_jg','qiling_jl'],
        }

        self.thread_id = thread_id
        #设置默认功能和次数
        self.func=[{'description':'0 屏幕截图并保存','func_name':self.screenshotShowFunc,'count_default':'inf'},\
        {'description':'1 寮突','func_name':self.liaotufunc,'count_default':3000},\
        {'description':'2 御魂/御灵/活动爬塔','func_name':self.yuhunfunc,'count_default':3000},\
        {'description':'3 探索(单刷)','func_name':self.tansuofunc,'count_default':3000},\
        {'description':'4 契灵单刷','func_name':self.qilingfunc,'count_default':3000},\
        {'description':'5 御魂司机','func_name':self.yuhunfunc1,'count_default':3000},\
        {'description':'6 御魂打手','func_name':self.yuhunfunc2,'count_default':3000},\
        {'description':'7 探索组队（司机）','func_name':self.tansuo_driver_func,'count_default':3000},\
        {'description':'8 探索组队（打手）','func_name':self.tansuo_fighter_func,'count_default':3000}]
        #功能序号
        self.index=index
        self.cishu_max=cishu_max
        self.isRunning=False
        #读取文件
        self.imgs = action.load_imgs(self.game_name)

    def run(self):
        #self.progress.emit('Thread is '+str(self.thread_id),self.thread_id)
        #self.progress.emit('Call function index '+str(self.index)+' with max count of '+str(self.cishu_max),self.thread_id)
        command=self.func[self.index]['func_name']
        command()
        self.finished.emit(self.thread_id)
    
    def message_output(self,msg):
        self.progress.emit(msg,self.thread_id)
    
    #暂停并支持提前停止
    def sleep_fast(self,t=0):
        #return value indicates interrupt happens
        for t_count in range(round(t/0.1)):
            if not self.isRunning:
                return True
            time.sleep(0.1)
        return False
    
    # 截取模拟器屏幕 
    def screenshotShowFunc(self):
        # 截取模拟器屏幕 查看图片内容
        screen=action.screenshot(self.thread_id)
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # # 显示图像
        cv2.imshow('Screenshot', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return
    
    #   寮突
    def liaotufunc(self):
        cishu=0
        new_msg = ""
        flag_list = {
            'lt_xz':False,
            'lt_ks':False,
            'lt_jg':False,
            'qiling_jl':False
        }
        flagNum = 0

        while self.isRunning:   #直到取消，或者出错
            try:
                #截屏
                screen=action.screenshot(self.thread_id)
                for i in ['lt_xz','lt_ks','lt_jg','qiling_jl']:
                    want=self.imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    target=screen
                    pts=action.locate(target,want,0)
                    if not flag_list[i]:
                        if not len(pts)==0:
                            self.message_output(f"当前点击事件：{i}({self.click_name[i]})")
                            self.message_output(f"识别到的坐标点:{pts}")
                            # self.message_output(f"长度:{len(pts)}")

                            if i=='lt_ks' or i == 'lt_xz':
                                flag_list['lt_ks'] = True
                                flag_list['lt_xz'] = True
                                cishu=cishu+1
                                self.message_output('挑战次数：'+str(cishu))

                            flag_list[i] = True
                            flagNum = flagNum + 1
                            # self.message_output(f"flagNum:{flagNum}")

                            if i == 'qiling_jl':
                                flag_list = {
                                    'lt_xz':False,
                                    'lt_ks':False,
                                    'lt_jg':False,
                                    'qiling_jl':False
                                }

                            #获取随机数 延迟点击
                            random_time = self.random_time[i]
                            t = random.randint(random_time[0], random_time[1]) / 100
                            if cishu > self.cishu_max:
                                self.message_output('进攻次数上限')
                                return

                            xy = action.cheat(pts[0], w, h-10 )
                            action.touch(xy,self.thread_id)
                            if self.sleep_fast(t): return
                            break
            except Exception as e:
                import traceback
                self.message_output(f"错误：{type(e).__name__}: {e}")
                self.message_output(traceback.format_exc())
                return

    ########################################################
    #御魂/御灵单刷
    def yuhunfunc(self):
        cishu=0
        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=action.screenshot(self.thread_id)
            for i in ['jujue','querenyuhun','zhidao','ying','jiangli','jiangli2','jixu','zhunbei','guanbi',\
                      'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai','yj_tz','hd_tz']:
                want=self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target=screen
                pts=action.locate(target,want,0)
                if not len(pts)==0:
                    #self.message_output('重复次数：',refresh)
                    self.message_output(i)
                    if i == 'tiaozhan' or i=='tiaozhan2' or i=='tiaozhan3' or i=='tancha' or i=='yj_tz' or i=='hd_tz':
                        cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(500,800) / 100
                    else:
                        t = random.randint(15,30) / 100
                    if cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy,self.thread_id)
                    if self.sleep_fast(t): return
                    break

    #============================================================
    # 探索模块 - 配置定义
    #============================================================
    class TansuoMode:
        """探索模式配置"""
        SINGLE = 0      # 单刷
        DRIVER = 1     # 司机
        FIGHTER = 2    # 打手

    # 探索模式配置表
    TANSUO_CONFIG = {
        TansuoMode.SINGLE: {
            'count_key': 'tansuo',          # 计次图标
            'map_targets': ['boss', 'jian', 'jian2', 'boss2', 'ts_baoxiang'],
            'menu_targets': ['jujue', 'querenyuhun', 'tansuo', 'ying', 'jiangli', 'jixu', 'c28', 'ditu', 'ts_baoxiang', 'ts_hdjl'],
            'need_move': True,              # 需要随机移动
            'need_exit': True,              # 需要退出探索
            'max_refresh': 3000,
            'max_move': 3000,
        },
        TansuoMode.DRIVER: {
            'count_key': 'tansuo',
            'map_targets': ['kb', 'jian2', 'boss', 'jian', 'boss2', 'ts_baoxiang', 'hdjl'],
            'menu_targets': ['tansuo', 'jujue', 'querenyuhun', 'ying', 'jiangli', 'jixu', 'c28', 'ditu', 'ts_baoxiang', 'ts_hdjl', 'zd_qd', 'zd_tz', 'kb', 'zd_tz2', 'hdjl'],
            'need_move': True,
            'need_exit': False,
            'max_refresh': 3000,
            'max_move': 3000,
        },
        TansuoMode.FIGHTER: {
            'count_key': None,
            'map_targets': ['ts_baoxiang','hdjl'],
            'menu_targets': ['jujue', 'querenyuhun', 'ying', 'jiangli', 'jixu', 'ditu', 'ts_baoxiang', 'ts_hdjl', 'zd_qd','hdjl'],
            'need_move': False,
            'need_exit': False,
            'max_refresh': 3000,
            'max_move': 3000,
        },
    }

    def _tansuo_loop(self, mode):
        """探索主循环 - 统一的探索逻辑"""
        cfg = self.TANSUO_CONFIG[mode]
        cishu = 0
        refresh = 0
        last_click = ''
        move_count = 0
        boss_done = False
        move_directions = [(600, 200), (620, 200), (610, 200), (600, 220), (620, 220), (630, 220)]

        while self.isRunning:
            screen = action.screenshot(self.thread_id)

            # 体力检测
            if action.locate(screen, self.imgs.get('notili', [None]), 0):
                self.message_output('体力不足')
                return

            # 单刷专属：退出确认
            if mode == self.TansuoMode.SINGLE:
                pts = action.locate(screen, self.imgs.get('queren', [None]), 0)
                if pts:
                    self.message_output('确认退出')
                    h, w = self.imgs['queren'][0].shape[:-1]
                    xy = action.cheat(pts[1] if len(pts) > 1 else pts[0], w, h)
                    action.touch(xy, self.thread_id)
                    if self.sleep_fast(0.2): return
                    continue

            # 地图中小怪检测
            if action.locate(screen, self.imgs['guding'], 0):
                found, pts, h, w = self._find_img(screen, cfg['map_targets'])
                if not found:
                    self.message_output(f'地图无目标,need_move={cfg["need_move"]},boss_done={boss_done}')
                if found:
                    # if 'boss' in found:
                        # boss_done = True
                    if cfg['need_exit'] and refresh > 3:
                        self.message_output('重复点击过多，退出')
                        # boss_done = True
                    else:
                        self.message_output(f'点击{found}')
                        xy = action.cheat(pts, w, h)
                        action.touch(xy, self.thread_id)
                        if self.sleep_fast(0.5 if 'baoxiang' in found else 0.5): return
                    last_click = found
                    continue

                # 地图中未找到目标
                if cfg['need_move']:
                    if not boss_done:
                        move_count += 1
                        if move_count > cfg['max_move']:
                            self.message_output('移动次数过多，尝试退出探索')
                            # boss_done = True
                            if not cfg['need_exit']: continue
                        direction = random.choice(move_directions)
                        self.message_output(f'移动至:{direction}')
                        xy = action.cheat(direction, 30, 30)
                        action.touch(xy, self.thread_id)
                        if self.sleep_fast(0.3): return
                    elif cfg['need_exit']:
                        pts = action.locate(screen, self.imgs.get('tuichu', [None]), 0)
                        if pts:
                            self.message_output('退出探索')
                            xy = action.cheat(pts[0], w, h)
                            action.touch(xy, self.thread_id)
                            if self.sleep_fast(0.6): return
                            boss_done = False
                            move_count = 0
                # 检测到guding时表示在地图界面，无论是否找到目标都continue
                # 避免在地图上时误触菜单按钮
                continue

            # 结算/菜单界面
            found, pts, h, w = self._find_img(screen, cfg['menu_targets'])
            if found:
                new_refresh = refresh + 1 if last_click == found else 0
                # 计次
                if cfg['count_key'] and found == cfg['count_key'] and new_refresh == 0:
                    cishu += 1
                    self.message_output(f'探索次数：{cishu}/{self.cishu_max}')
                if new_refresh > cfg['max_refresh'] or cishu > self.cishu_max:
                    self.message_output('次数已达上限')
                    return
                self.message_output(found)
                xy = action.cheat(pts, w, h - 10)
                action.touch(xy, self.thread_id)
                t = random.randint(*self.random_time.get(found, [15, 30])) / 100
                last_click = found
                refresh = new_refresh
                if self.sleep_fast(t): return

    def _find_img(self, screen, targets):
        """在screen中查找targets列表中的第一个匹配图像，返回(name, pts, h, w)或(None, None, None, None)"""
        for name in targets:
            if name not in self.imgs:
                continue
            want = self.imgs[name]
            pts = action.locate(screen, want, 0)
            if pts:
                h, w = want[0].shape[:-1]
                return name, pts[0], h, w
        return None, None, None, None

    def tansuo_driver_func(self):
        """探索组队（司机）"""
        self._tansuo_loop(self.TansuoMode.DRIVER)

    def tansuo_fighter_func(self):
        """探索组队（打手）"""
        self._tansuo_loop(self.TansuoMode.FIGHTER)

    def tansuofunc(self):
        """探索单刷"""
        self._tansuo_loop(self.TansuoMode.SINGLE)


    ########################################################
    ########################################################
    #   契灵单刷
    #   操作逻辑
    #   1.点击挑战 "qiling_tz"
    #   2.结契失败（放弃结契）
    #   3.结契成功（继续挑战）
    def qilingfunc(self):
        cishu=0
        new_msg = ""
        # 截取模拟器屏幕 查看图片内容
        # import cv2,pyautogui
        # screen=action.screenshot(self.thread_id)
        # import numpy as np
        # frame = np.array(screen)
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # # 显示图像
        # cv2.imshow('Screenshot', frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # return

        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=action.screenshot(self.thread_id)
            for i in self.event_list['qiling']:
                want=self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target=screen
                pts=action.locate(target,want,0)
                if not len(pts)==0:
                    self.message_output(f"当前点击事件：{i}({self.click_name[i]})")
                    self.message_output(f"识别到的坐标点:{pts}")
                    self.message_output(f"长度:{len(pts)}")
                    
                    if i=='qiling_tz':
                        cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))

                    #获取随机数 延迟点击
                    random_time = self.random_time[i]
                    t = random.randint(random_time[0], random_time[1]) / 100
                    if cishu > self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy,self.thread_id)
                    if self.sleep_fast(t): return
                    break



    #御魂司机
    def yuhunfunc1(self):
        img_list = ['jujue','querenyuhun','zhidao','ying','jiangli','jiangli2','jixu','zhunbei','guanbi',
                     'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai','zd_tz']
        self._yuhun_common(img_list)

    #御魂打手
    def yuhunfunc2(self):
        img_list = ['jujue','querenyuhun','zhidao','ying','jiangli','jiangli2','jixu','zhunbei','guanbi',
                     'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai','zd_qd']
        self._yuhun_common(img_list)

    def _yuhun_common(self, img_list):
        cishu = 0
        tiaozhan_set = {'tiaozhan', 'tiaozhan2', 'tiaozhan3', 'tancha'}

        while self.isRunning:
            screen = action.screenshot(self.thread_id)
            for i in img_list:
                want = self.imgs[i]
                size = want[0].shape
                h, w, ___ = size
                target = screen
                pts = action.locate(target, want, 0)
                if pts:
                    self.message_output(i)
                    if i in tiaozhan_set:
                        cishu += 1
                        self.message_output(f'挑战次数：{cishu}/{self.cishu_max}')
                        t = random.randint(500, 800) / 100
                    else:
                        t = random.randint(15, 30) / 100
                    if cishu > self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h - 10)
                    action.touch(xy, self.thread_id)
                    if self.sleep_fast(t):
                        return
                    break



