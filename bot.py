from lib import itchat
from lib.itchat.content import TEXT
from gpt import chat, generate_img
from bot_memory import Bot_memory


@itchat.msg_register(TEXT)
def print_content(msg):
    print(msg['Text'])


# for private chat
@itchat.msg_register(TEXT)
def reply_msg(msg):
    message = msg['Text']
    msg_prefix = message[0]
    if msg_prefix in ['画', 'draw']:
        generate_img(message)
        itchat.send_image(fileDir="bot_draw_img.jpg", toUserName=msg['FromUserName'])
    else:
        user_msg = {"role": "user", "content": message}
        Bot_memory().save_memory(user_msg)
        messages = Bot_memory.memory_list
        try:
            bot_res = chat(messages=messages, maxtokens=3800)
            bot_msg = {"role": "system", "content": bot_res}
            Bot_memory().save_memory(bot_msg)
            itchat.send_msg(msg=bot_res, toUserName=msg['FromUserName'])

        except Exception as e:
            print(e)
            Bot_memory().clear_memory()

            user_msg = {"role": "user", "content": message}
            Bot_memory().save_memory(user_msg)
            messages = Bot_memory.memory_list
            bot_res = chat(messages=messages, maxtokens=3800)

            bot_msg = {"role": "system", "content": bot_res}
            Bot_memory().save_memory(bot_msg)
            itchat.send_msg(msg=bot_res, toUserName=msg['FromUserName'])


# for group chat
@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']: 
    if msg['isAt']:
        nickname = 'Warren Buffet'
        message = msg['Text']
        message = message.split(nickname)[1].strip()
        msg_prefix = message[0]
        if msg_prefix in ['画', 'draw']:
            generate_img(message)
            itchat.send_image(fileDir="bot_draw_img.jpg", toUserName=msg['FromUserName'])
        else:
            user_msg = {"role": "user", "content": message}
            Bot_memory().save_memory(user_msg)
            messages = Bot_memory.memory_list
            try:
                bot_res = chat(messages=messages, maxtokens=3800)
                bot_msg = {"role": "system", "content": bot_res}
                Bot_memory().save_memory(bot_msg)
                itchat.send_msg(msg=bot_res, toUserName=msg['FromUserName'])

            except Exception as e:
                print(e)
                Bot_memory().clear_memory()

                user_msg = {"role": "user", "content": message}
                Bot_memory().save_memory(user_msg)
                messages = Bot_memory.memory_list
                bot_res = chat(messages=messages, maxtokens=3800)

                bot_msg = {"role": "system", "content": bot_res}
                Bot_memory().save_memory(bot_msg)
                #print(Bot_memory.memory_list)
                itchat.send_msg(msg=bot_res, toUserName=msg['FromUserName'])


# 启动微信机器人
itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run()
