from bot_settings import *

def main_found():
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        chat_id = call.message.chat.id
        data = load_data()
        if call.from_user.username in data["founders"]:
            if call.data == 'f_btn1':
                user_states[chat_id] = 'awaiting_input'
                bot.send_message(
                    chat_id,
                    (
                        "📩 *Введите данные о новой посылке:*\n\n"
                        "Формат:\n`Track-code` `Статус товара`\n\n"
                        "📍 *Доступные статусы:*\n"
                        "1️⃣ В обработке...\n"
                        "2️⃣ Поступил на склад в Китае 🏪\n"
                        "3️⃣ В пути 🚛\n"
                        "4️⃣ Готов к выдаче 📦\n\n"
                        "✏️ *Пример:* `3423 2`"
                    ),
                    parse_mode='Markdown'
                )


            elif call.data == 'f_btn2':
                # Загружаем данные из файла
                data = load_data()
                # Проверяем, есть ли данные
                if not data:
                    bot.send_message(chat_id, "❌ Нет данных для отправки.")
                    return

                # Создаем текстовый файл с данными
                filename = "List_cargo.txt"

                try:
                    with open(filename, "w", encoding="utf-8") as file:
                        for item in data["packages"]:
                            track_code = item
                            status = data["packages"][item]
                            file.write(f"{track_code}, {map_status_to_text(status)}\n")

                    # Отправляем текстовый файл пользователю

                    with open(filename, "rb") as file:
                        bot.send_document(chat_id, file)
                    bot.send_message(chat_id, "📄 Файл с данными успешно отправлен!")

                except Exception as e:
                    bot.send_message(chat_id, f"❌ Произошла ошибка при отправке файла: {e}")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        chat_id = message.chat.id
        if message.from_user.username in data["founders"]:
            if user_states.get(chat_id) == 'awaiting_input':
                try:
                    # Обработка пользовательского ввода
                    user_input = message.text.split(' ')
                    track_code = user_input[0]
                    delivery_status = user_input[1]

                    # Проверка корректности статуса
                    if delivery_status not in ["1", "2", "3", "4"]:
                        bot.send_message(
                            chat_id,
                            "❌ *Ошибка: неверный статус.*\n"
                            "📍 Пожалуйста, используйте статусы от 1 до 4.",
                            parse_mode="Markdown"
                        )
                        return

                    # Сохранение данных
                    add_package_info(track_code, delivery_status)

                    bot.send_message(
                        chat_id,
                        (
                            f"✅ *Данные успешно добавлены:*\n\n"
                            f"🔹 *Трек-код:* `{track_code}`\n"
                            f"📍 *Статус:* {map_status_to_text(delivery_status)}"
                        ),
                        parse_mode='Markdown'
                    )




                except Exception:

                    if user_input == ['0']:

                        bot.send_message(

                            chat_id,

                            (

                                f"✅ *Все данные успешно добавлены, проверьте список*"

                            ),

                            parse_mode='Markdown'

                        )

                        user_states[chat_id] = None

                    else:

                        bot.send_message(

                            chat_id,

                            "❌ *Ошибка: неверный формат ввода.*\n"
    
                            "📍 Используйте формат: `Track-code Статус`.",

                            parse_mode="Markdown"

                        )

            elif message.text == 'Таблица с данными':
                bot.send_message(chat_id, "📊 *Вы запросили таблицу с данными.*", parse_mode="Markdown")
            else:
                bot.send_message(chat_id, "👋 *Введите /start для начала работы с ботом.*", parse_mode="Markdown")


# Вспомогательная функция для преобразования статуса
