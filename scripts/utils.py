import json


"""
@brief:解析并返回settings.json文件内容
"""
def load_config():
    with open('/home/dumbo/yd_workspace/config/settings.json', 'r') as file:
        return json.load(file)
    

