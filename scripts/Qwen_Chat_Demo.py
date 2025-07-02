from utils import load_config
from openai import OpenAI


"""
@brief: 通过openai官方接口调用通义千问大模型
@last updated: 2025/1/3 
"""


# Loading Qwen API Parameter Settings
API_Config = load_config()


class QwenAIChat():
    """
    @brief: 构造函数
    """
    def __init__(self):
       # Loading Qwen Parameter Settings
        self.api_key = API_Config["Qwen"].get("api_key")
        self.base_url = API_Config["Qwen"].get("base_url")
        self.model = API_Config["Qwen"].get("model")
        self.max_tokens = API_Config["Qwen"].get("max_tokens")
        self.temperature = API_Config["Qwen"].get("temperature")
        self.conversation_history = []  # 用于存储对话历史


    """
    @brief: 启动开场白
    @return: 启动状态
    """
    def Launch(self):
        print("What can i help with?")
        return True
    

    """
    @brief: 退出开场白
    @return: 退出状态
    """
    def Exit(self):
        print("See you next time!")
        return False


    """
    @brief: 获取回答内容
    @return: 内容
    """
    def Get_Response(self,text):
        # 将用户输入添加到对话历史
        self.conversation_history.append({'role': 'user', 'content': text})

        client = OpenAI(
            api_key = self.api_key,
            base_url = self.base_url,)

        if not any(msg['role']=='system' for msg in self.conversation_history):
            self.conversation_history.insert(0,{'role':'system','content':'你是一个善于表达且严谨的小助手，名字叫塔可塔可，你回答问题会简洁清晰明白有重点。'})
        
        completion = client.chat.completions.create(
            model = self.model,
            messages = self.conversation_history,
            temperature = self.temperature,
            top_p = 0.8,)

        assistant_response = completion.choices[0].message.content
        self.conversation_history.append({'role':'assistant','content':assistant_response})

        return assistant_response
    
    

if __name__ == "__main__":
    Qwen = QwenAIChat()

    try:
        Status = Qwen.Launch()
        while Status:
            user_input = input("You:").strip()
            if user_input.lower() in ["exit", "quit", "bye", "再见"]:
                Status = Qwen.Exit()

            else:
                Answer = Qwen.Get_Response(user_input)
                print(f"Answer: {Answer}")

    except Exception as e:
        print(f"Can not Call API,something went wrong! Error:{e}")
