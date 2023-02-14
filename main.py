from keyboard import sender
from vk_api.longpoll import VkLongPoll, VkEventType
from db import *
from VKBots import *

print('В конфиге можно включить или отключить debug инфу!')

for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        sender(user_id, msg.lower())
        if request == 'Start':
            creating_database()
            bot.write_msg(user_id, f'Привет, {bot.name(user_id)}')
            bot.find_user(user_id)
            bot.write_msg(event.user_id, f'Наидено нажми "Next"')
            bot.find_person(user_id, offset)

        elif request == 'Next':
            for i in line:
                offset += 1
                bot.find_person(user_id, offset)
                break

        else:
            bot.write_msg(event.user_id, 'Сообщение не понятно!')
            