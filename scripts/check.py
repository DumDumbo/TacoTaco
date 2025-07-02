import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    print("可用的音频设备列表：\n")

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"设备索引: {i}")
        print(f"设备名称: {device_info['name']}")
        print(f"输入通道数: {device_info.get('maxInputChannels', 0)}")
        print(f"输出通道数: {device_info.get('maxOutputChannels', 0)}")
        print(f"默认采样率: {device_info['defaultSampleRate']} Hz")
        print("-" * 40)

    p.terminate()

list_audio_devices()
