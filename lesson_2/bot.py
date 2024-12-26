# Импортирование необходимых библиотек
import telebot  # библиотека для работы с Telegram API
import json  # для работы с JSON файлами
import os  # для работы с операционной системой
import re  # для работы с регулярными выражениями
import threading  # для работы с многозадачностью
from datetime import datetime  # для работы с датой и временем

# Токен для Telegram-бота и канал для отправки сообщений
TOKEN = 'your_BOT_TOKEN'  # токен бота
CHANNEL_NAME = 'YOUR_CHANNEL'  # имя канала для отправки сообщений

# Имена файлов для хранения данных викторин и текстов
QUESTIONS_FILE = 'questions.json'  # файл с вопросами викторины
TEXTS_FILE = 'texts.json'  # файл с текстами для отправки

# Разрешённые часы для отправки сообщений (с 9:00 до 19:00)
ALLOWED_HOURS = range(9, 20)

# Функция для загрузки JSON файлов
def load_file(file_name):
    # Проверяем, существует ли файл
    if os.path.exists(file_name):
        # Если файл существует, открываем его и загружаем содержимое как JSON
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}  # Возвращаем пустой словарь, если файл не найден

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Загрузка данных викторин и текстов
questions = load_file(QUESTIONS_FILE)
texts = load_file(TEXTS_FILE)

# Индекс текущего вопроса викторины
quiz_index = 0

# Функция для отправки викторины в канал
def send_quiz():
    global quiz_index  # Используем глобальную переменную для изменения индекса викторины

    if not questions:  # Если викторины отсутствуют, выводим сообщение
        print("Викторин нет")
        return
    
    # Получаем данные текущего вопроса
    question_data = questions[quiz_index]
    try:
        # Отправляем викторину в канал
        bot.send_poll(
            chat_id=CHANNEL_NAME,
            question=question_data["question"],  # Вопрос
            options=question_data['options'],  # Варианты ответа
            is_anonymous=True,  # Анонимность опроса
            type="quiz",  # Тип отправляемого опроса
            correct_option_id=question_data["currentOption"]  # Правильный ответ
        )
        print(f"Викторина отправлена: {question_data['question']}")
        # Переходим к следующему вопросу (с циклом)
        quiz_index = (quiz_index + 1) % len(questions)
    except Exception as e:  # Обработка ошибок при отправке
        print(f"Ошибка при отправке: {e}")

# Индекс текущего текста
text_index = 0

# Функция для экранирования специальных символов в тексте (для Markdown)
def escape_markdown(text):
    return re.sub(r'([\\*_{}[\]()#+\-.!])', r'\\\1', text)

# Функция для отправки текста в канал
def send_text():
    global text_index  # Используем глобальную переменную для изменения индекса текста

    if not texts:  # Если текстов нет, выводим сообщение
        print("Текстов нет")
        return   
    try:
        # Получаем данные текущего текста
        text_data = texts[text_index]  
        hedaing = text_data['heading']
        text = text_data['text']
        # Отправляем текст в канал с использованием MarkdownV2
        bot.send_message(
            chat_id=CHANNEL_NAME,
            text=f"*{escape_markdown(hedaing)}*\n\n||{escape_markdown(text)}||\n\n[➡️*Подпишись*](https://t.me/lessonchan)",
            parse_mode='MarkdownV2',  # Использование MarkdownV2 для форматирования
            disable_web_page_preview=True  # Отключение предпросмотра веб-страниц
        )
        print(f"Текст отправлен: {hedaing}")
        # Переходим к следующему тексту (с циклом)
        text_index = (text_index + 1) % len(texts)
    except Exception as e:  # Обработка ошибок при отправке
        print(f"Ошибка при отправке: {e}")

# Функция для планирования задач (отправка викторины и текста)
def schedule_tasks():
    # Если текущее время в пределах разрешённых часов
    if datetime.now().hour in ALLOWED_HOURS:
        send_quiz()  # Отправить викторину
        send_text()  # Отправить текст
    else:
        print("Сейчас не время для квиза")
    
    # Запускаем задачу снова через 5 минут
    threading.Timer(5 * 60, schedule_tasks).start()

# Главная функция для запуска бота
if __name__ == "__main__":
    try:
        schedule_tasks()  # Запуск планирования задач
        bot.polling()  # Начало работы бота, ожидание сообщений
    except KeyboardInterrupt:  # Обработка остановки бота вручную
        print("Бот остановлен вручную.")
    except Exception as e:  # Обработка других ошибок
        print(f"Ошибка: {e}")
