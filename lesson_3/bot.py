import time
from telebot import TeleBot
import game
import keyboard

API_TOKEN = '7089320888:AAE2u7z__4Oe2cnHNdMG52sGfMv3wmIuTiU'

bot = TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    """Обработка команды /start."""
    user_id = message.chat.id
    bot.send_message(user_id, "Добро пожаловать в 🏆викторину", reply_markup=keyboard.get_common_keyboard())

@bot.message_handler(func=lambda message: message.text == "🏆Начать викторину")
def set_mode(message):
    """Выбор режима викторины."""
    game.select_mode(bot, message)

@bot.message_handler(func=lambda message: message.text in {"25 Вопросов", "50 Вопросов", "75 Вопросов", "100 Вопросов"})
def start_game(message):
    """Запуск игры с выбранным количеством вопросов."""
    try:
        question_count = int(message.text.split()[0])
        game.start_game(bot, message, question_count)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка в выборе количества вопросов. Попробуйте ещё раз.")

@bot.message_handler(func=lambda message: message.text in {"1", "2", "3", "4"})
def handle_answer(message):
    """Обработка ответов пользователя."""
    game.handle_answer(bot, message)

@bot.message_handler(func=lambda message: message.text == "❌Завершить")
def close_game(message):
    """Завершение текущей викторины."""
    try:
        game.close_game(bot, message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка завершения игры. Выберите опцию:", reply_markup=keyboard.get_common_keyboard())
        print(f"Ошибка завершения игры: {e}")

# Бесконечный цикл опроса
while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"Критическая ошибка: {e}. Перезапуск через 5 секунд...")
        time.sleep(5)
