import pandas as pd 
from chat import ChatAgent
import numpy as np

def split_usr_chat(chat):

    chat = chat.split('坐席:')

    user_chat = []
    for t in chat:
        if '用户:' in t:
            t = t.split('用户:')
            t = t[1:]
            
            user = ''
            for x in t:
                user += x
            user_chat.append(user)
    return user_chat


def eval(input):

    df = pd.read_excel(input, sheet_name='标注')

    all = df.to_dict(orient='records')

    result =[]

    for item in all:

        hos_name = item['hos_name']
        if pd.isna(hos_name):
            hos_name = ""
        hos_info = item['hos_info']
        if pd.isna(hos_info):
            hos_info = "未提供"
        user_info = item['user_info']
        if pd.isna(user_info):
            user_info = "未提供"

        agent = ChatAgent(hos_name=hos_name,hos_info=hos_info,user_info=user_info)

        valid = item['正负']
        if valid == 0:
            continue
        chat = item['录音转文字']
        user_chat = split_usr_chat(chat)


        chat_history = ""
        for user in user_chat:

            print(f'user:{user}')
            chat_history += f"用户:{user}\n"
            res = agent.chat(user)
            print(f"坐席：{res}")
            chat_history += f"坐席:{res}\n"
        
        item['chat_with_bot'] = chat_history
        result.append(item)
        
        

    df = pd.DataFrame(result)
    # 保存为 Excel 文件  
    output = input.replace('.xlsx', '_bot.xlsx')
    df.to_excel(output, index=False) 



if __name__ == "__main__":
    eval('resource/0926ma标注(2).xlsx')
