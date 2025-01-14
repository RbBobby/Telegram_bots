import random
import re
from telebot import TeleBot
from telebot.types import ReplyKeyboardRemove
from load import load_questions
import keyboard

COUNT_OF_QUESTIONS = 100
questions = load_questions()  # Загружаем вопросы
size_questions = len(questions)
user_states = {}  # Состояния пользователей
random_unique_array = {}
count_of_question = 0


def escape_markdown(text: str) -> str:
    """
    Экранирует специальные символы для MarkdownV2.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(rf"([{re.escape(escape_chars)}])", r"\\\1", text)


def select_mode(bot: TeleBot, message) -> None:
    """
    Показывает пользователю выбор режима викторины.
    """
    bot.send_message(
        message.chat.id,
        "Выберите режим викторины:",
        reply_markup=keyboard.get_how_many_questions_keyboard()
    )


def start_game(bot: TeleBot, message, count: int) -> None:
    """
    Начинает викторину с заданным количеством вопросов.
    """
    global random_unique_array, count_of_question
    count_of_question = count
    user_id = message.chat.id

    # Удаляем клавиатуру и приветствуем пользователя
    bot.send_message(user_id, "Начинаем викторину!", reply_markup=ReplyKeyboardRemove())

    # Устанавливаем начальное состояние пользователя
    user_states[user_id] = {"current_question": 0, "score": 0}
    random_unique_array = random.sample(range(size_questions), size_questions)

    send_question(bot, user_id)


def send_question(bot: TeleBot, chat_id: int) -> None:
    """
    Отправляет текущий вопрос пользователю.
    """
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "Ошибка: состояние пользователя не найдено.")
        return

    if state["current_question"] < count_of_question:
        question_index = random_unique_array[state["current_question"]]
        question_data = questions[question_index]

        question_text = (
            f"Вопрос №{state['current_question'] + 1} из {count_of_question}.\n\n"
            f"{question_data['question']}\n"
        )
        options_text = "\n".join(
            [f"{i + 1}) {option}" for i, option in enumerate(question_data["options"])]
        )

        bot.send_message(
            chat_id,
            f"<b>{question_text}</b>{options_text}",
            parse_mode="HTML",
            reply_markup=keyboard.get_quiz_keyboard()
        )
    else:
        close_game(bot, chat_id)
        user_states.pop(chat_id, None)  # Удаляем состояние пользователя


def close_game(bot: TeleBot, chat_id: int) -> None:
    """
    Завершает викторину и отправляет результат.
    """
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "Ошибка: состояние пользователя не найдено.")
        return

    bot.send_message(
        chat_id,
        f"Викторина завершена! Ваш результат: {state['score']} из {count_of_question}.",
        reply_markup=keyboard.get_common_keyboard()
    )


def handle_answer(bot: TeleBot, message) -> None:
    """
    Обрабатывает ответ пользователя и переходит к следующему вопросу.
    """
    state = user_states.get(message.chat.id)
    if not state:
        bot.send_message(message.chat.id, "Ошибка: состояние пользователя не найдено.")
        return

    question_index = random_unique_array[state["current_question"]]
    question_data = questions[question_index]

    if int(message.text) - 1 == question_data["correctOption"]:
        state["score"] += 1
        bot.send_message(message.chat.id, "✅ Правильно!")
    else:
        correct_option = question_data["options"][question_data["correctOption"]]
        bot.send_message(message.chat.id, f"❌ Неправильно. Правильный ответ: {correct_option}")

    state["current_question"] += 1
    send_question(bot, message.chat.id)
