import vk_api
import requests
import datetime
from config import user_token, g_token, offset, line
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from db import *

# ===========================================================================
# ================= Создаем класс сбора и обработки данных ==================

class VKBot:
# ===========================================================================
# ====================== Инициализация бота по токену =======================
    def __init__(self):
        if debug == True:
            print('(BOT) = Запушен и работает =')
        self.vk = vk_api.VkApi(token=g_token)  # авторизация по токену, группа
        self.longpoll = VkLongPoll(self.vk)  # Bots Long Poll API
# ===========================================================================
# ========================= отправка сообщения ==============================

    def write_msg(self, user_id, message):
        '''отправка сообщений'''
        self.vk.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7)
            })
        # DEBUG  
        if debug == True:
            print(f'(write_msg) {user_id}: {message}')
# ===========================================================================
# ============================ получаем имя =================================

    def name(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        info_dict = response['response']
        for a in info_dict:
            for key, value in a.items():
                fname = a.get('fname')
                return fname
        # DEBUG  
        if debug == True:
            print(f'(name) Пишет пользователь с именем: {fname}')
# ===========================================================================
# ============================ получаем пол =================================

    def get_sex(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'sex',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        info_list = response['response']
        for a in info_list:  # 1 = male (М) ; 2 = female (Ж)
            if a.get('sex') == 2:
                find_sex = 1
                return find_sex
            elif a.get('sex') == 1:
                find_sex = 2
                return find_sex
        # DEBUG        
        if debug == True:
            if find_sex == 1:
                pol = 'М'
            elif find_sex == 2:
                pol = 'Ж'
            print(f'(get_sex) Пол: {pol}')
# ===========================================================================
# ============================ возраст от ===================================            

    def get_age_ot(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        info_list = response['response']
        for a in info_list:
            date = a.get('bdate')
        date_list = date.split('.')
        if len(date_list) == 3:
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            return year_now - year
        elif len(date_list) == 2 or date not in info_list:
            self.write_msg(user_id, 'Введите возраст от (мин 16 лет): ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    return age
        # DEBUG        
        if debug == True:
            print(f'(get_age_ot) Возраст от :{age}')    
# ===========================================================================
# ============================ возраст до ===================================

    def get_age_do(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        info_list = response['response']
        for a in info_list:
            date = a.get('bdate')
        date_list = date.split('.')
        if len(date_list) == 3:
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            return year_now - year
        elif len(date_list) == 2 or date not in info_list:
            self.write_msg(user_id, 'Введите возраст до (максимум 65 лет): ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    return age
        # DEBUG        
        if debug == True:
            print(f'(get_age_do) Возраст до :{age}')    
# ===========================================================================
# ============== Получение id по названию города нужен ниже =================

    def cities(self, city_name):
        url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': user_token,
                  'country_id': 1,
                  'q': f'{city_name}',
                  'need_all': 0,
                  'count': 1000,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        info_list = response['response']
        list_city = info_list['items']
        for a in list_city:
            fcn = a.get('title')
            if fcn == city_name:
                id_city = a.get('id')
                return int(id_city)    
        # DEBUG        
        if debug == True:
            print(f'(cities) ok')     
# ===========================================================================
# ==================== Получение инфо о городе пользователя =================

    def find_city(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        info_dict = response['response']
        for i in info_dict:
            if 'city' in i:
                city = i.get('city')
                id = str(city.get('id'))
                return id
            elif 'city' not in i:
                self.write_msg(user_id, 'Введите название вашего города: ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        city_name = event.text
                        id_city = self.cities(city_name)
                        if id_city != '' or id_city != None:
                            return str(id_city)
                        else:
                            break
        # DEBUG        
        if debug == True:
            print(f'(find_city) Город:{city_name} ID:{id_city}')   
# ===========================================================================
# =========================== Поиск человека ================================

    def find_user(self, user_id):
        '''Ищем людей по ID'''
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': self.get_sex(user_id),
                  'age_from': self.get_age_ot(user_id),
                  'age_to': self.get_age_do(user_id),
                  'city': self.find_city(user_id),
                  'fields': 'is_closed, id, fname, lname',
                  'status': '1' or '6',
                  'count': 1000}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        dict_1 = resp_json['response']
        list_1 = dict_1['items']
        for person_dict in list_1:
            if person_dict.get('is_closed') == False:
                vk_id = str(person_dict.get('id'))
                fname = person_dict.get('fname')
                lname = person_dict.get('lname')
                vk_link = 'vk.com/id' + str(person_dict.get('id'))
                # записываем в базу (db.py Таблица:users)
                insert_data_users(vk_id, fname, lname, vk_link) 
            else:
                continue
        return f'Поиск завершён'
# ===========================================================================
# ======================== Работы с фотографиями ============================

    def get_photo_id(self, user_id):
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': user_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        dict_photos = dict()
        resp_json = resp.json()
        dict_1 = resp_json['response']
        list_1 = dict_1['items']
        for i in list_1:
            photo_id = str(i.get('id'))
            i_likes = i.get('likes')
            if i_likes.get('count'):
                likes = i_likes.get('count')
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        return list_of_ids

    def get_photo(self, user_id, num):
        list = self.get_photo_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == num:
                return i[1]

    def send_photo(self, user_id, message, offset, num):
        self.vk.method('messages.send', {
        'user_id': user_id,
        'access_token': user_token,
        'message': message,
        'attachment': f'photo{self.person_id(offset)}_{self.get_photo(self.person_id(offset),num)}',
        'random_id': 0
        })

# ===========================================================================
# ======================== Поиск пользователя ===============================
    def find_person(self, user_id, offset):
        '''Поиск пользователя'''
        self.write_msg(user_id, self.found_person_info(offset))
        self.person_id(offset)
        insert_data_ch_users(self.person_id(offset), offset) 
        self.get_photo_id(self.person_id(offset))
        if Count_photo > 1:
            for i in range(1, Count_photo):
                self.send_photo(user_id, f'Фото {i}', offset, i)
            else:
                self.write_msg(user_id, f'Больше фотографий нет')
        else:
            self.send_photo(user_id, f'Фото {i}', offset, Count_photo)
# ===========================================================================
# ======================== Инфо о пользователе ==============================

    def found_person_info(self, offset):
        tuple_person = select(offset)
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return f'{list_person[0]} {list_person[1]}, ссылка - {list_person[3]}'
# ===========================================================================
# ========================== Инфо по ID =====================================

    def person_id(self, offset):
        tuple_person = select(offset)
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return str(list_person[2])
        

bot = VKBot()
