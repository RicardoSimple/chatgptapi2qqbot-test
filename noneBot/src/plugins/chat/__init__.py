
import json
from nonebot import on_command, on_message
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.adapters import Event
import requests
import random
import re

return_for_empty = ["?","byd不输入内容是吧","请输入内容捏","1！5！","嗷呜~","你说话了吗？","嗨嗨嗨","哥们在这给你说唱","你想不想抽电子烟"]

pattern = re.compile(r"^chatGPT\s*(.*)$")  # 匹配以 chatGPT 开头的字符串，并获取后面的内容

chatgpt = on_command("gpt3", rule=to_me(), aliases={"gpt3", "chatgpt3"}, priority=10, block=True)
dialogue_history = []


@chatgpt.handle()
async def handle_function(event: Event):
    message = event.get_plaintext()
    
    if message:
        match = pattern.match(message.strip())
        if not match:
            # 如果匹配失败则结束命令处理
            await chatgpt.finish("命令格式错误，请输入 chatGPT + 需要查询的内容")
            return
        query = match.group(1)  # 获取正则匹配结果中第一个括号中的内容

        text = requestApi(message)
        print(text)
        await chatgpt.finish(text)
    else:
        random_reply = random.choice(return_for_empty)
        await chatgpt.finish(random_reply)


def requestApi(msg):
    msg_body = {
        "msg": msg
    }
    response = requests.get('http://ricardo-nonebot.azurewebsites.net/chat-api/?msg='+msg)
    result = json.loads(response.text)
    text = result['text']['message']['content']
    return text

class MsgItem:
    def __init__(self,role,content,name):
        self.role = role
        self.content = content
        self.name = name