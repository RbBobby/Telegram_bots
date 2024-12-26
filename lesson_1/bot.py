import telebot
import time 

TOKEN = 'YOUR_BOT_TOKEN'   # Вставьте сюда токен вашего бота
ADMIN_ID = 'YOUR_ADMIN_ID'  # Укажите ID администратора, куда будут отправляться сообщения

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        # Получаем ID чата пользователя
        chat_id = message.chat.id
        # Отправляем приветственное сообщение
        bot.send_message(chat_id, 'Привет! Отправь сюда то, что считаешь интересным')
    except Exception as e:
        # Логируем ошибку, если она возникла
        print(e)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        # Получаем ID чата пользователя
        chat_id = message.chat.id
        # Отправляем подтверждение пользователю
        bot.send_message(chat_id, 'Спасибо, ваше сообщение отправлено!')
        # Отправляем текст администраторам
        bot.send_message(ADMIN_ID, 'Получено новое сообщение от @' + str(message.chat.username))
        bot.send_message(ADMIN_ID, message.text)
    except Exception as e:
        # Логируем ошибку, если она возникла
        print(e)

# Обработчик фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Получаем ID чата пользователя
        chat_id = message.chat.id
        # Если вместе с фото есть подпись, используем ее, иначе указываем, что текста нет
        caption = message.caption if message.caption else "Фото без текста"
        # Отправляем подтверждение пользователю
        bot.send_message(chat_id, 'Спасибо, ваше фото отправлено!')
        # Отправляем фото и текст администраторам
        bot.send_message(ADMIN_ID, f"Получено новое сообщение от @{str(message.chat.username)}: {caption}")
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id)
    except Exception as e:
        # Логируем ошибку, если она возникла
        print(e)

# Обработчик видео
@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        # Получаем ID чата пользователя
        chat_id = message.chat.id
        # Если вместе с видео есть подпись, используем ее, иначе указываем, что текста нет
        caption = message.caption if message.caption else "Видео без текста"
        # Отправляем подтверждение пользователю
        bot.send_message(chat_id, 'Спасибо, ваше видео отправлено!')
        # Отправляем видео и текст администраторам
        bot.send_message(ADMIN_ID, f"Получено новое сообщение от @{str(message.chat.username)}: {caption}")
        bot.send_video(ADMIN_ID, message.video.file_id)
    except Exception as e:
        # Логируем ошибку, если она возникла
        print(e)

# Основной цикл для запуска бота
while True:
    try:
        # Запускаем polling для обработки входящих сообщений
        bot.polling()
    except Exception as e:
        # Логируем исключение при ошибках
        print(f"Возникло исключение: {e}")
        # Ждем 5 секунд перед повторной попыткой
        time.sleep(5)