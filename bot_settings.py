from telebot import *
import json
from bot_settings import *

bot = telebot.TeleBot('7220436614:AAE3cXVoJuxoNA3Ay3elUAAo-DV0pX84D70')

user_states = {}
# Имена основателей



def load_data():
    try:
        with open('data.json', 'r',encoding='utf-8') as file:
            data = json.load(file)  # Преобразует JSON в словарь
            return data
    except FileNotFoundError:
        return {}  # Если файл не найден, возвращаем пустой словарь

data = load_data()

# Запись данных в JSON-файл
def save_data(data):
    print('Все сохранено')
    with open('data.json', 'w',encoding='utf-8') as file:
        json.dump(data, file,ensure_ascii=False, indent=4)

def update_data(data):
    print('Все обновлено')
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def add_package_info(track_code, value):
    # Сначала загружаем существующие данные
    data = load_data()

    data["packages"][track_code] = value
    print('Добавлен', track_code, value)
    # Сохраняем обратно в JSON-файл
    save_data(data)


def map_status_to_text(status):
    status_mapping = {
        "1": "В обработке... 🔄",
        "2": "Поступил на склад в Китае 🏪",
        "3": "В пути 🚛",
        "4": "Готов к выдаче 📦",
    }
    return status_mapping.get(status, "Неизвестный статус")

