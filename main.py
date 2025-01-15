from Found_interface import *
from Users_interface import *
from bot_settings import *
# Файл для хранения данных

Hello = False
print("Программа начала работу")

data = load_data()

# Пример обновления
@bot.message_handler(commands=['start'])
def main(message):
    global Hello
    print(message.from_user.username, 'запустил бота')
    if message.from_user.username in data["founders"]:
        if not Hello:
            bot.send_message(
                message.chat.id,
                '👋 Привет, Луиза! Добро пожаловать! 😊'
            )
            Hello = True

        # Создаем кнопки для основного меню
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('➕ Добавить/изменить', callback_data='f_btn1')
        btn2 = types.InlineKeyboardButton('📊 Таблица посылок', callback_data='f_btn2')
        markup.add(btn1, btn2)

        # Отправляем сообщение с клавиатурой
        bot.send_message(
            message.chat.id,
            "🔍 <b>Выберите операцию:</b>",
            reply_markup=markup,
            parse_mode='html'
        )
        main_found()
    else:
        if not Hello:
            username = message.from_user.username
            if username in data["users_and_packages"]:
                greating_text = '👋 Здравствуйте!'
            else:
                greating_text = '👋 Здравствуйте! \n☺️ <b>Я ваш бот-помощник.\n\nПеред началом работы с ботом 📲, если вы используете его впервые, рекомендуем заглянуть в вкладку с туториалами 📚 для удобства!</b>'
            bot.send_message(
                message.chat.id,
                greating_text,
                parse_mode='html'
            )
            Hello = True

        # Создаем кнопки для основного меню
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('✉️ Код', callback_data='btn1')
        btn2 = types.InlineKeyboardButton('👜 Мой лист', callback_data='btn2')
        btn3 = types.InlineKeyboardButton('📞 Инфо', callback_data='btn3')
        btn4 = types.InlineKeyboardButton('📚 Туториалы', url='https://t.me/arscargo')
        markup.add(btn1, btn2, btn3, btn4)

        # Отправляем сообщение с клавиатурой
        bot.send_message(
            message.chat.id,
            "🔍 <b>Выберите операцию:</b>",
            reply_markup=markup,
            parse_mode='html'
        )
        main_user()


if __name__ == "__main__":

    bot.infinity_polling()

