<h1 align="center">🌮 Taco Taco：Raspberry Pi AI 语音助手</h1>

<div align="center">

<a href="https://bailian.console.aliyun.com/">
  <img src="https://img.shields.io/badge/Made%20with-阿里百炼-orange?style=flat-square&logo=alibaba" alt="阿里百炼"/>
</a>
<a href="https://picovoice.ai/">
  <img src="https://img.shields.io/badge/Powered%20by-Picovoice-blue?style=flat-square&logo=picovoice" alt="Picovoice"/>
</a>
<a href="https://www.raspberrypi.com/products/raspberry-pi-5/">
  <img src="https://img.shields.io/badge/Platform-Raspberry%20Pi%205-lightgrey?style=flat-square&logo=raspberrypi" alt="Raspberry Pi"/>
</a>
<a href="./LICENSE">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
</a>

<i>🗣️本人菜鸟一枚，项目仍在学习和完善中，欢迎各位开发者多多指教 ⭐️</i>

</div>


> Taco Taco 是一个类比百度音箱的开源语音助手，基于 Raspberry Pi 5 和 Ubuntu 24.02 打造，集成唤醒词检测、语音识别、大语言模型、文本转语音等功能，通过调用多个 AI API 实现自然语音交互。


---
## 📁I. 项目文件说明
### i. `config/`
文件夹包含**TacoTaco**所需的音频文件、唤醒模型文件以及 API 设置信息。  
- 其中 `.wav` 是音频文件，用于系统提示音。  
- `*.pnn` 为唤醒模型文件  
- `settings.json` 存储各个 API 的配置信息，包括 `api_key`、`model`、`format` 等参数。
> **⚠️ 注意事项：** api_key需要修改为自己的api_key哟！


### ii. `scripts/`
文件夹用于存储python文件，包含**TacoTaco**相关的语音处理示例代码，包括：  
- **`wakeup_pvrecorder.py`**：语音唤醒及VAD检测Demo，负责检测特定唤醒词和语音获得检测。 
- **`realtime_speech2text_demo.py`**：实时语音转文本 Demo，实现语音识别并转换为文本。
- **`Qwen_Chat_Demo.py`**：LLM，大语言模型，输入用户文本信息---得到--->LLM输出文本
- **`tts_deSamber_TTS_Demo.py`**：文本转语音Demo，将LLM输出文本转换为语音输出。  
`utils.py` 包含用于解析 `settings.json` 的工具方法。


### iii. `sh/`  
文件夹用于存储自动化脚本。
- **`chatbot_auto_launch.sh`**：为Chatbot开机自启动脚本，其会自动检测WIFI连接情况。    
✅ If connected --> 启动脚本。  
❌ If not connected --> 播放网络检查提示音。

>  **⚠️ 注意事项：** 本人通过Ubuntu界面的Startup Applications设置了自动化脚本。因本人设置了用户锁屏，故需要在用户设置中勾选`开机自动登录选项，才可实现无障碍的自启动。


### iv. `src/`
文件夹用于存储C++、C语言文件，因Chatbot全部基于Python开发，故为空。


### v. `其余文件`
`requirments.txt`: 存储了Chatbot所需的第三方库信息。
`output.txt`: 实时语音转文本Demo所输出的信息将会转写于这里。
`output.wav`: TTL根据LLM的文本所生成的语音回复将会存储于这里。 


---
## 🚀 II.使用流程
### i. 开机自启动
开机自启动文件存储与`sh`文件夹中
该启动文件已添加进Ubuntu自带的应用程序APP：`Startup Applications（中文：启动应用程序）`中，从而可以实现开机自启动。
### ii. 人为启动
进入sh文件夹，在当前位置终端运行`./chatbot_auto_launch.sh`即可。


---
## 📝 III. API 说明
> 本项目集成了多个第三方平台的强大能力，以下是所用核心模块：

| 功能模块 | 技术平台 | 说明 |
|---------------------|--------------|---------------------------------------|
| 唤醒词 + VAD         | Picovoice   | 本地离线处理，低延迟、高准确性           |
| 语音识别（ASR）      | 阿里百炼      | 实时转录用户语音                        |
| 大语言模型（LLM）    | 阿里百炼      | 支持 Qwen / DeepSeek / LLaMA 等模型     |
| 文本转语音（TTS）    | 阿里百炼      | 生成自然语音回复，音色多样、可自定义      |


---
# 🙏致谢
> 感谢以上平台提供的优秀服务，使 Taco Taco 项目得以实现端到端的语音交互体验！


