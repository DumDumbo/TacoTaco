from utils import load_config
import dashscope
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)
import struct


API_Config = load_config()


"""
@brief: 实时语音识别回调函数类
"""
class MyRecognitionCallback(RecognitionCallback):
    def __init__(self):
        self.full_text = ""
        self.output_text_file = "output.txt"


    def on_open(self)-> None:
        print("WebSocket链接成功")


    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if sentence and "text" in sentence:
            print(f"实时结果: {sentence['text']}")
            self.full_text = sentence['text']
        else:
            print("收到空结果")


    def on_complete(self)-> None:
        with open(self.output_text_file,"w") as file:
            file.write(self.full_text)
        print(f"Result saved to {self.output_text_file}.")


    def on_error(self, error: Exception) -> None:
        print(f"发生错误: {error}")
        
    def on_close(self) -> None:
        print("服务已关闭")

        

"""
@brief: 语音转文本类
"""
class Speech2Text():
    """
    @brief: 构造函数
    """
    def __init__(self):
        super().__init__()  # 确保初始化
        self.s2t_api_key = API_Config["speech2text"].get("api_key")
        self.s2t_model = API_Config["speech2text"].get("model")
        self.s2t_sample_rate = API_Config["speech2text"].get("sample_rate")
        self.s2t_format = API_Config["speech2text"].get("format")

        dashscope.api_key = self.s2t_api_key

        self.recognition = Recognition(
            model=self.s2t_model,
            format=self.s2t_format,
            sample_rate=self.s2t_sample_rate,
            language_hints = ['zh','en'],
            callback=MyRecognitionCallback())

    
    """
    @brief: 开始识别函数
    """
    def start_identifying(self):
        self.recognition.start()
        print("语音识别已开启")
        
    """
    @brief: 停止识别函数
    """
    def stop_identifying(self):
        self.recognition.stop()
        print("语音识别已停止")

    """
    @brief: 将音频数据发送至服务器
    """
    def send_audio_data2server(self, data):
        frame_bytes = struct.pack('<{}h'.format(len(data)), *data)
        self.recognition.send_audio_frame(frame_bytes)








if __name__ == "__main__":
    pass
