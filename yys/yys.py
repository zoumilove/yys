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
            'lt_jg': [100, 150],
            'lt_jl': [100, 150],
        }

        self.event_list = {
            'qiling':['qiling_tz','qiling_sj','qiling_fq','qiling_jl'],
            'liaotu':['lt_ks','lt_jg','qiling_jl'],
        }

        self.thread_id = thread_id
        #设置默认功能和次数
        self.func=[{'description':'0 屏幕截图并保存','func_name':self.screenshotShowFunc,'count_default':'inf'},\
        {'description':'1 寮突','func_name':self.liaotufunc,'count_default':3000},\
        {'description':'2 御魂/御灵/活动爬塔','func_name':self.yuhunfunc,'count_default':3000},\
        {'description':'3 探索(单刷)','func_name':self.tansuofunc,'count_default':3000},\
        {'description':'4 契灵单刷','func_name':self.qilingfunc,'count_default':3000},\
        {'description':'5 御魂司机','func_name':self.yuhunfunc1,'count_default':3000},\
        {'description':'6 御魂打手','func_name':self.yuhunfunc2,'count_default':3000}]
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
        last_click=''
        cishu=0
        refresh=0
        new_msg = ""
        # # 截取模拟器屏幕 查看图片内容
        # import cv2,pyautogui
        # screen=action.screenshot(self.thread_id)
        # import numpy as np
        # frame = np.array(screen)
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # # # 显示图像
        # cv2.imshow('Screenshot', frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # return
        flag_list = {
            'lt_ks':False,
            'lt_jg':False,
            'qiling_jl':False
        }
        flagNum = 0

        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=action.screenshot(self.thread_id)
            for i in ['lt_ks','lt_jg','qiling_jl']:
                want=self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target=screen
                pts=action.locate(target,want,0)
                if not flag_list[i]:
                    if not len(pts)==0:
                        if last_click==i:
                            refresh=refresh+1
                        else:
                            refresh=0
                        
                        last_click=i
                        self.message_output(f"当前点击事件：{i}({self.click_name[i]})")
                        self.message_output(f"识别到的坐标点:{pts}")
                        # self.message_output(f"长度:{len(pts)}")
                        
                        if i=='lt_ks':
                            if refresh==0:
                                cishu=cishu+1
                            self.message_output('挑战次数：'+str(cishu))

                        flag_list[i] = True
                        flagNum = flagNum + 1
                        # self.message_output(f"flagNum:{flagNum}")

                        if i == 'qiling_jl':
                            flag_list = {
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

    ########################################################
    #御魂/御灵单刷
    def yuhunfunc(self):
        last_click=''
        cishu=0
        refresh=0
        
        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=action.screenshot(self.thread_id)
            
            #体力不足
            want = self.imgs['notili']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return

            for i in ['jujue','querenyuhun','zhidao','ying','jiangli','jiangli2','jixu','zhunbei','guanbi',\
                      'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai','yj_tz','hd_tz']:
                want=self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target=screen
                pts=action.locate(target,want,0)
                if not len(pts)==0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    self.message_output(i)
                    if i == 'tiaozhan' or i=='tiaozhan2' or i=='tiaozhan3' or i=='tancha' or i=='yj_tz' or i=='hd_tz':
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(500,800) / 100
                    else:
                        t = random.randint(15,30) / 100
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy,self.thread_id)
                    if self.sleep_fast(t): return
                    break
     
    ########################################################
    #探索单刷
    def tansuofunc(self):
        last_click=''
        cishu=0
        refresh=0
        right = (754, 420)
        
        boss_done=False
        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=action.screenshot(self.thread_id)
            
            #体力不足
            want = self.imgs['notili']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return

            want = self.imgs['queren']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            #x1,x2 = upleft, (965, 522)
            #target = action.cut(screen, x1, x2)
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('确认退出')
                try:
                    queding = pts[1]
                except:
                    queding = pts[0]
                xy = action.cheat(queding, w, h)
                action.touch(xy,self.thread_id)
                t = random.randint(15,30) / 100
                if self.sleep_fast(t): return

            
            #设定目标，开始查找
            #进入后
            want=self.imgs['guding']

            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                #self.message_output('正在地图中')
                for i in ['boss', 'jian','jian2','boss2']:
                    want = self.imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    target = screen
                    pts = action.locate(target,want,0)
                    if not len(pts) == 0:
                        if 'boss' in i:
                            boss_done=True
                            i='jian'
                        if last_click==i:
                            refresh=refresh+1
                        else:
                            refresh=0
                        last_click=i
                        #self.message_output('重复次数：',refresh)
                        if refresh>3:
                            self.message_output('进攻次数上限')
                            return
                        
                        self.message_output('点击小怪'+i)
                        xy = action.cheat(pts[0], w, h)
                        action.touch(xy,self.thread_id)
                        time.sleep(0.5)
                        break

                if len(pts)==0:
                    if not boss_done:
                        self.message_output('向右走')
                        xy = action.cheat(right, 10, 10)
                        action.touch(xy,self.thread_id)
                        t = random.randint(100,300) / 100
                        if self.sleep_fast(t): return
                        continue
                    else:
                        i='tuichu'
                        want = self.imgs[i]
                        size = want[0].shape
                        h, w , ___ = size
                        pts = action.locate(screen,want,0)
                        if not len(pts) == 0:
                            self.message_output('退出中'+i)
                            if len(pts) > 0:
                                queding = pts[0]  # 始终取第一个匹配点
                            else:
                                return  # 或 return
                            xy = action.cheat(queding, w, h)
                            action.touch(xy,self.thread_id)
                            t = random.randint(50,80) / 100
                            if self.sleep_fast(t): return
                    continue

            for i in ['jujue','querenyuhun',\
                      'tansuo','ying','jiangli','jixu','c28','ditu','ts_baoxiang','ts_hdjl']:
                want = self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    if refresh==0 and i=='tansuo':
                        cishu=cishu+1
                        self.message_output('探索次数：'+str(cishu)+'/'+str(self.cishu_max))
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    self.message_output(i)
                    xy = action.cheat(pts[0], w, h )
                    action.touch(xy,self.thread_id)
                    t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                    break


    ########################################################
    ########################################################
    #   契灵单刷
    #   操作逻辑
    #   1.点击挑战 "qiling_tz"
    #   2.结契失败（放弃结契）
    #   3.结契成功（继续挑战）
    def qilingfunc(self):
        last_click=''
        cishu=0
        refresh=0
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
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i

                    self.message_output(f"当前点击事件：{i}({self.click_name[i]})")
                    self.message_output(f"识别到的坐标点:{pts}")
                    self.message_output(f"长度:{len(pts)}")
                    
                    if i=='qiling_tz':
                        if refresh==0:
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
        last_click=''
        cishu=0
        refresh=0
        
        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=action.screenshot(self.thread_id)
            
            #体力不足
            want = self.imgs['notili']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return

            for i in ['jujue','querenyuhun','zhidao','ying','jiangli','jiangli2','jixu','zhunbei','guanbi',\
                      'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai','zd_tz']:
                want=self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target=screen
                pts=action.locate(target,want,0)
                if not len(pts)==0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    self.message_output(i)
                    if i == 'tiaozhan' or i=='tiaozhan2' or i=='tiaozhan3' or i=='tancha':
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(500,800) / 100
                    else:
                        t = random.randint(15,30) / 100
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy,self.thread_id)
                    if self.sleep_fast(t): return
                    break
     
        #御魂司机
   
    #御魂打手
    def yuhunfunc2(self):
        last_click=''
        cishu=0
        refresh=0
        
        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=action.screenshot(self.thread_id)
            
            #体力不足
            want = self.imgs['notili']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return

            for i in ['jujue','querenyuhun','zhidao','ying','jiangli','jiangli2','jixu','zhunbei','guanbi',\
                      'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai','zd_qd']:
                want=self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target=screen
                pts=action.locate(target,want,0)
                if not len(pts)==0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    self.message_output(i)
                    if i == 'tiaozhan' or i=='tiaozhan2' or i=='tiaozhan3' or i=='tancha':
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(500,800) / 100
                    else:
                        t = random.randint(15,30) / 100
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    action.touch(xy,self.thread_id)
                    if self.sleep_fast(t): return
                    break
     