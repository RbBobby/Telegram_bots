from telebot import types

def get_common_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_quiz = types.KeyboardButton("🏆Начать викторину")

    markup.row(btn_quiz)
    return markup

def get_quiz_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton("1")
    btn_2 = types.KeyboardButton("2")
    btn_3 = types.KeyboardButton("3")
    btn_4 = types.KeyboardButton("4")
    btn_5 = types.KeyboardButton("❌Завершить")
    markup.row(btn_1, btn_2)
    markup.row(btn_3, btn_4)
    markup.row(btn_5)
    return markup

def get_how_many_questions_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton("25 Вопросов")
    btn_2 = types.KeyboardButton("50 Вопросов")
    btn_3 = types.KeyboardButton("75 Вопросов")
    btn_4 = types.KeyboardButton("100 Вопросов")
    markup.row(btn_1, btn_2)
    markup.row(btn_3, btn_4)

    return markup