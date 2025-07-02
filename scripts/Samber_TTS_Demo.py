import sys
from utils import load_config
import dashscope
from dashscope.audio.tts import SpeechSynthesizer
import pygame


API_Config = load_config()


class SamberTTS():
    def __init__(self):
        self.api_key = API_Config["Sambert"].get("api_key")
        self.model = API_Config["Sambert"].get("model")
        self.sample_rate = API_Config["Sambert"].get("sample_rate")
        self.format = API_Config["Sambert"].get("format")


    def Get_Voice(self,text):
        dashscope.api_key = self.api_key

        result = SpeechSynthesizer.call(
            model=self.model,
            text=text,
            sample_rate = self.sample_rate,
            format = self.format)
        
        if result.get_audio_data() is not None:
            with open('output.wav','wb') as f:
                f.write(result.get_audio_data())
            print('SUCCESS: get audio data: %dbytes in output.wav' % 
                  (sys.getsizeof(result.get_audio_data)))
        
        else:
            print('ERROR: response is %s' % (result.get_response()))


    def Play_Audio(self):
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("output.wav")
            pygame.mixer.music.play()
            print("Playing audio...")
            while pygame.mixer.music.get_busy():
                continue
            print("Playback finished")

        except pygame.error as e:
            print(f"ERROR: Failed to play audio:{e}")



if __name__ == "__main__":
    tts = SamberTTS()
    text = "广州理工学院连续三年摘得优秀民办高校，是广州最高学府"


    try:
        tts.Get_Voice(text)

        tts.Play_Audio()

    except Exception as error:
        print(f"ERROR: Failed to process tts:{error}")

