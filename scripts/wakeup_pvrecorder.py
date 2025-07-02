#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pvporcupine
from pvrecorder import PvRecorder
from utils import load_config
import pygame
import time
import pvcobra
from collections import deque

# private
from realtime_speech2text_demo import Speech2Text
from Qwen_Chat_Demo import QwenAIChat
from Samber_TTS_Demo import SamberTTS

API_Config = load_config()


"""
@breif: 本文件为语音ai助手的核心文件,其集合了语音唤醒、语音活动检测、语音转文本、文本生成、文本转语音,语音播报所有任务流程。
@author: 也耶耶
@updated dated:  2025/4/12
@notes: 本应独立做一个启动文件,与语音唤醒和VAD检测代码解耦,但emmmm,再说吧


"""
class Awake():
    def __init__(self):
        """初始化参数"""
        self.access_key = API_Config["wakeup"].get("api_key")
        self.keywords = [API_Config["wakeup"].get("keywords"),] 
        self.keywords_path = [API_Config["wakeup"].get("keywords_path")]
        self.response_audio_file = [API_Config["wakeup"].get("response_audio_file")]
        
        """实例化类"""
        self.realtime_s2t = Speech2Text()
        self.Qwen = QwenAIChat()
        self.SamberTTS = SamberTTS()

        """状态变量"""
        self.state=0
        self.type = "Silent"
        self.last_speech_time = 0
        self.last_silent_time = None
        self.speech_timeout = 1.8
        self.silent_timeout = 7

        """音频采集滑动窗口变量"""
        self.window_size = 3                # 存储音频的数量
        self.vad_window = deque(maxlen=self.window_size)   # 存储最近三帧音频的vad
        self.frame_window = deque(maxlen=self.window_size) # 存储最近三帧音频
        self.audio_buffer = deque(maxlen=128)



        """实例化porcupine进行语音唤醒"""
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keywords=self.keywords,
            keyword_paths=self.keywords_path
        )

        """实例化PvRecorder进行音频输入"""
        self.recorder = PvRecorder(
            device_index=-1,  # -1 代表自动选择默认麦克风
            frame_length=self.porcupine.frame_length
        )

        """实例化Cobra进行VAD语言活动检测"""
        self.cobra = pvcobra.create(
                access_key=self.access_key
        )

        """初始化pygame进行音频播放"""
        pygame.mixer.init()


    
    """
    @breif:语言唤醒启动音
    """
    def _launch_response(self):
        """播放语音回应"""
        audio_file = API_Config["wakeup"].get("launch_audio_file")
        pygame.mixer.music.load(audio_file)
        self.audio_duration = pygame.mixer.Sound(audio_file).get_length()
        pygame.mixer.music.play()

        """音频播放中返回True, 播放完毕返回False"""
        while pygame.mixer_music.get_busy():
            time.sleep(0.1)
    

    """
    @breif:程序结束音
    """
    def _poweroff_response(self):
        """播放语音回应"""
        audio_file = API_Config["wakeup"].get("power_off_audio_file")
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        """等待音频播放完毕"""
        while pygame.mixer_music.get_busy():
            time.sleep(0.1)
            

        
    """
    @breif:静默超时
    """
    def _silent_timeout(self):
        self.state = 0
        self._poweroff_response()
        self.realtime_s2t.stop_identifying()
        print(f"静默超时")


    """
    @breif:发言超时
    """
    def _speech_timeout(self):
        self.realtime_s2t.stop_identifying()
        self.state = 2
        print(f"发言超时")
    

    """
    @breif:资源释放函数
    """
    def _clennup(self):
        """释放资源"""
        self.recorder.stop()
        self.porcupine.delete()
        self.recorder.delete()
        self.cobra.delete()           
        pygame.mixer.quit()



    """
    @breif:语音唤醒函数
    """
    def _voice_wakeup(self, audio_frame):
        keyword_index = self.porcupine.process(audio_frame)
        if keyword_index >= 0:
            print(f"检测到唤醒词：{self.keywords[keyword_index]}")
            
            self.last_silent_time = time.time()
            self.state = 1
            # 开启实时转语音模块
            self.realtime_s2t.start_identifying()
            self.recorder.stop()
            self._launch_response()
            self.recorder.start()




    """
    @breif:语音活动检测
    """
    def _voice_activity_detect(self, audio_frame):
        self.vad_window.append(self.cobra.process(audio_frame))   # 存储最近三帧音频的vad
        self.frame_window.append(audio_frame)
        if len(self.vad_window) == self.window_size:
            average_vad = sum(self.vad_window)/self.window_size
            return average_vad
        else:
            return 0.0
    

    """
    @breif:语音转文本
    """
    def _voice2text(self, audio_frame):
        voice_probability = self._voice_activity_detect(audio_frame)
        print(f"Voice_probability:{voice_probability}, Type:{self.type}, Last Speech:{time.time()-self.last_speech_time}, Last Silent:{time.time()-self.last_silent_time}")
        if voice_probability > 0.4:
            self.type = "Speaking"

            for frame in self.frame_window:
                self.audio_buffer.append(frame)
            self.frame_window.clear()


            if len(self.audio_buffer)>=self.window_size:
                for buffer in self.audio_buffer:
                    self.realtime_s2t.send_audio_data2server(buffer)
                self.audio_buffer.clear()
            
            self.last_speech_time = time.time()
            self.last_silent_time = time.time()
            


        else:
            # 判断状态(静默状态+静默超时，回退待唤醒)
            if self.type == "Silent" and time.time() - self.last_silent_time > self.silent_timeout:
                self._silent_timeout()
            
            # 判断状态（发言状态+发言超时，进入ai文本生成）
            elif self.type == "Speaking" and time.time()-self.last_speech_time > self.speech_timeout:
                self._speech_timeout()




    """
    @breif: 回复生成
    """
    def _generate_text(self):
        with open('output.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        response = self.Qwen.Get_Response(content)
        self.SamberTTS.Get_Voice(response)
        self.state = 3


    """
    @breif: 播放语音回复
    """
    def _reply_audio(self):
        try:
            self.recorder.stop()
            pygame.mixer.music.load("output.wav")
            pygame.mixer.music.play()
            print("Playing audio...")
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            self.recorder.start()
            self.state = 1
            self.type = "Silent"
            self.last_silent_time = time.time()
            self.realtime_s2t.start_identifying()

        except pygame.error as e:
            print(f"ERROR: Failed to play audio:{e}")
        


    """
    @breif:启动函数
    """
    def launch(self):
        print("开始监听唤醒词... (Ctrl+C 停止)")
        self.recorder.start()
    
        try:
            while True:
                audio_frame = self.recorder.read()  # 直接读取音频
                # print(f"State:{self.state}")
                
                if self.state == 0:
                    self._voice_wakeup(audio_frame)
                elif self.state == 1:
                    self._voice2text(audio_frame)
                elif self.state == 2:
                    self._generate_text()
                elif self.state == 3:
                    self._reply_audio()
                else:
                    pass

        except KeyboardInterrupt:
            print("停止监听")
            self._poweroff_response()
        finally:
            self._clennup()



if __name__ == "__main__":
    awake = Awake()
    awake.launch()
