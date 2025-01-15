# Импорт настроек бота из файла bot_settings
from bot_settings import *

phone_num = ''

btn1 = False
btn2_1 = False
btn2_3 = False
def main_user():
    # Обработка callback-запросов
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        chat_id = call.message.chat.id  # Получаем ID чата пользователя
        data = load_data()
        global btn1, btn2, btn2_1, btn2_3

        if call.data == 'btn1':
            username = call.from_user.username
            user_states[chat_id] = 'awaiting_phone_input'
            print(f'Пользователь {username} получает код')# Устанавливаем состояние для пользователя
            bot.send_message(
                chat_id,
                '📞 Пожалуйста, введите номер телефона в формате: <em>87077777777</em>',
                parse_mode='html'
            )
            btn1 = True

        elif call.data == 'btn2_1':
            username = call.from_user.username
            print(f'Пользователь {username} добавляет товар')
            user_states[chat_id] = 'awaiting_code_input'
            bot.send_message(
                chat_id,
                '✉️ Пожалуйста, введите трек-код вашей посылки.\n⚠️ Убедитесь, что код указан правильно!',
                parse_mode='html'
            )
            btn2_1 = True

        elif call.data == 'btn2_2':
            username = call.from_user.username
            print(f'Пользователь {username} смотрит свои товары')
            if username in data["users_and_packages"] and len(data["users_and_packages"][username]) != 0:
                result = [
                    f"{i + 1}# 📦 <b>Товар по трек-коду:</b> <code>{p}</code>\n"
                    f"📍 <b>Статус:</b> {map_status_to_text(data['packages'][p])}\n"
                    for i, p in enumerate(data["users_and_packages"][username])
                ]
                bot.send_message(
                    chat_id,
                    f"✅ <b>Ваши товары:</b>\n\n" + "\n".join(result),
                    parse_mode='html'
                )
            else:
                bot.send_message(
                    chat_id,
                    '🚫 <b>Вас нет в базе данных или ваш лист пуст.</b>\n'
                    'Добавьте товары в свой список! \n(если не помогло обратитесь в поддержку!)',
                    parse_mode='html'
                )


        elif call.data == 'btn2_3':

            username = call.from_user.username
            print(f'Пользователь {username} подверждает получение')
            if username in data["users_and_packages"] and len(data["users_and_packages"][username]) != 0:

                markup_mini = types.InlineKeyboardMarkup()

                for track_code in data["users_and_packages"][username]:
                    text = '🔄'
                    if data['packages'][track_code] == "4":
                        text = '✅'
                    button = types.InlineKeyboardButton(

                        text=f"{text} {track_code}",

                        callback_data=f"track_{track_code}"

                    )

                    markup_mini.add(button)

                bot.send_message(

                    chat_id,

                    "Пожалуйста, выберите товары, получение которых вы хотите подтвердить 📦\n\n✅ - прибыл на склад\n🔄 - в процессе доставки",

                    reply_markup=markup_mini

                )

            else:

                bot.send_message(chat_id, '🚫 <b>Вас нет в базе данных или ваш лист пуст.</b>\n'
                    'Добавьте товары в свой список! \n(если не помогло обратитесь в поддержку!)',
                    parse_mode='html')

            user_states[chat_id] = 'awaiting_confirmation'

        elif call.data == 'btn2':
            btn2 = True
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('➕ Добавить', callback_data='btn2_1'),
                types.InlineKeyboardButton('📜 Товары', callback_data='btn2_2'),
                types.InlineKeyboardButton('✅ Подтвердить', callback_data='btn2_3')
            )
            bot.send_message(chat_id, "Выберите операцию:", reply_markup=markup)

        elif call.data == 'btn3':
            bot.send_message(
                chat_id,
                '🏢 <b>Адрес пункта выдачи:</b>\nпроспект Райымбека 512\n'
                '📱 <b>Контакты (WhatsApp):</b> +7 776 609 09 46',
                parse_mode='html'
            )

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        global phone_num, btn1, btn2_1, btn2_3
        chat_id = message.chat.id  # Получаем ID чата пользователя
        data = load_data()

        if btn1 and user_states.get(chat_id) == 'awaiting_phone_input':
            phone_num = message.text
            username = message.from_user.username

            if phone_num not in data['users']:
                data['users'].append(phone_num)
                number_q = f"{len(data['users']):02}"
            else:
                number_q = f"{data['users'].index(phone_num) + 1:02}"

            bot.send_message(
                chat_id,
                f"✅ <b>Ваш код:</b>\n"
                f"广东省广州市荔湾区站前路 57-3 国际 \n6777 库房Almaty-123-{number_q} 李生 \n15649133333 ({phone_num})",
                parse_mode='html'
            )
            bot.send_message(chat_id, '📋 Пример правильной вставки кода:')
            bot.send_photo(chat_id, photo=open('WhatsApp Image 2024-12-23 at 21.43.37.jpeg', 'rb'))
            print(f'Пользователь {username} успешно получил код')
            user_states[chat_id] = None
            btn1 = False
            save_data(data)

        elif btn2_1 and user_states.get(chat_id) == 'awaiting_code_input':
            track_code = message.text
            username = message.from_user.username

            if username not in data["users_and_packages"]:
                data["users_and_packages"][username] = []
                update_data(data)

            if track_code in data["users_and_packages"][username]:
                bot.send_message(
                    chat_id,
                    '📦 <b>Этот трек-код уже добавлен в ваш список!</b>',
                    parse_mode='html'
                )
            else:
                data["users_and_packages"][username].append(track_code)
                update_data(data)
                if track_code not in data['packages']:
                    add_package_info(track_code, '1')

                bot.send_message(
                    chat_id,
                    '🎉 <b>Посылка успешно добавлена в ваш список товаров!</b>',
                    parse_mode='html'
                )
                print(f'Пользователь {username} успешно добавил товар')
            btn2_1 = False




        else:
            bot.send_message(chat_id, "📝 Введите /start, чтобы начать.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("track_"))
def handle_track_button(call):
    data = load_data()
    username = call.from_user.username
    track_code = str(call.data.split("_")[1])
    print(data["users_and_packages"][username])
    if track_code in data["users_and_packages"][username]:
        data["users_and_packages"][username].remove(track_code)
        del data["packages"][track_code]
        bot.send_message(call.message.chat.id, f"Товар с трек-кодом {track_code} успешно удален из списка")
        update_data(data)
    else:
        bot.send_message(call.message.chat.id, f"Товар с трек-кодом {track_code} уже удален или отсутсвует в списке (проверьте свой список)")
