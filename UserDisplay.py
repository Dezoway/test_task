from os import system
from pick import pick
from enum import Enum
import sqlite3


class Titles(Enum):
    TITLE_MAIN_MENU = '----------ПРОГРАММА ПОДСКАЗОК АДРЕСОВ----------'
    TITLE_SETTINGS_MENU = '----------НАСТРОЙКИ ПРОГРАММЫ----------'
    TITLE_ADDRESS_MENU = '----------ПОЛУЧЕНИЕ КООРДИНАТ ПО АДРЕСУ----------'
    TITL_SET_LANG = 'Выберите язык ответов от сервиса dadata'


class DataBase:
    def __new__(cls, *args, **kwargs):
        return None

    @staticmethod
    def load_data():
        return [x for x in sqlite3.connect('data.db').cursor().execute('SELECT * FROM user')][0]

    @staticmethod
    def change_data(string, string1, string2, string3):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        cursor.execute(f'UPDATE user SET "{string}" = "{string1}" WHERE "{string2}" = "{string3}";')
        connect.commit()
        connect.close()


class Display:
    def __new__(cls, *args, **kwargs):
        return None

    @staticmethod
    def main_menu_display():
        return ['Получить точные координаты',
                'Настройки программы',
                'Выход из программы']

    @staticmethod
    def settings_menu_display():
        return ['Изменить адрес(рекомендуется для опытных пользователей)',
                'Создать/изменить API ключ',
                'Выбор языка ответов',
                'Выход в главное меню']

    @staticmethod
    def change_url():
        return ['Текущий URL адрес: ', 'Введите URL адрес: ', 'URL адрес успешно изменен']

    @staticmethod
    def return_to_menu():
        return 'Нажмите Enter чтобы вернуться в меню'

    @staticmethod
    def change_api_key():
        return ['Ваш текущий API ключ ',
                'Введите API ключ полученный в личном кабинете сервиса dadata: ',
                'API ключ успешно изменен']

    @staticmethod
    def address():
        return['Введите адрес:', 'Выберите желаемый адрес из списка: ', 'Координаты адреса:']

    @staticmethod
    def change_language():
        return ['ru', 'en', 'Язык ответов успешно изменен']


import requests
import json


class Api:
    def __init__(self, url, api_key, lang):
        self.url = url
        self.api_key = api_key
        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {api_key}'
        }
        self.lang = lang

    def check_connect(self):
        status_code = requests.get(self.url, headers=self.headers).status_code
        if status_code == 200 and self.api_key:return True
        else:
            print('Некорректный API ключ либо некорректный URL адрес')
            return False

    def get_data(self, text):
        response = json.loads(requests.get(self.url, headers=self.headers,
                                params={'query': text, 'language': self.lang, 'count': 20}).text)
        return [x['unrestricted_value'] for x in response['suggestions']]

    def get_coords(self, text):
        response = json.loads(requests.get(self.url, headers = self.headers,
                                params={'query': text, 'language': self.lang, 'count': 1}).text)
        response = response['suggestions'][-1]['data']
        return response['geo_lat'], response['geo_lon']


class User:
    def __init__(self):
        self.url, self.api_key, self.lang = DataBase.load_data()
        self.navigation()

    def settings(self):
        item = (0, 0)
        while item[1] != 3:
            item = pick(options=Display.settings_menu_display(), title=Titles.TITLE_SETTINGS_MENU.value)
            if item[1] == 0:
                system('cls||clear')
                print(f'{Display.change_url()[0]}{self.url}')
                self.url = input(Display.change_url()[1])
                DataBase.change_data('url', self.url, 'language', self.lang)
                print(Display.change_url()[-1])
            elif item[1] == 1:
                system('cls||clear')
                print(f'{Display.change_api_key()[0]} {"не найден" if not self.api_key else self.api_key}')
                self.api_key = input(f'{Display.change_api_key()[1]}')
                DataBase.change_data('api_key', self.api_key, 'url', self.url)
                print(Display.change_api_key()[-1])
                input(Display.return_to_menu())
            elif item[1] == 2:
                item_lang = pick(options=Display.change_language()[:-1], title=Titles.TITL_SET_LANG.value)
                if item_lang[1] == 0:
                    self.lang = 'ru'
                    DataBase.change_data('language', 'ru', 'url', self.url)
                else:
                    self.lang = 'en'
                    DataBase.change_data('language', 'en', 'url', self.url)
                system('cls||clear')
                print(Display.change_language()[-1])
                input(Display.return_to_menu())

    def get_address(self):
        obj = Api(self.url, self.api_key, self.lang)
        system('cls||clear')
        print(Titles.TITLE_ADDRESS_MENU.value)
        if obj.check_connect():
            address = input(Display.address()[0])
            choice = pick(obj.get_data(address), title=Display.address()[1])
            print(f'{Display.address()[-1]}{obj.get_coords(choice[0])}')
            input(Display.return_to_menu())
        else:
            input(Display.return_to_menu())

    def navigation(self):
        item = (0, 0)
        while item[1] != 2:
            item = pick(options=Display.main_menu_display(), title=Titles.TITLE_MAIN_MENU.value)
            if item[1] == 0:
                self.get_address()

            if item[1] == 1:
                self.settings()
        system('cls||clear')



if __name__ == '__main__':
    User()
    exit(0)