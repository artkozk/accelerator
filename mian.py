import telebot
from telebot import types
import random
from config import token, admin

bot = telebot.TeleBot(token)
example_sum_1 = 0
example_sum_2 = 0
example_sum_3 = 0

example_sub_1 = 0
example_sub_2 = 0
example_sub_3 = 0

example_mul_1 = 0
example_mul_2 = 0
example_mul_3 = 0

example_share_1 = 0
example_share_2 = 0
example_share_3 = 0

true = 0
false = 0

al = 0
@bot.message_handler(commands=['start'])
def start(message):
    global user
    global username
    global u_id
    user = message.from_user.first_name
    username = message.from_user.username
    u_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    global_button_1 = types.KeyboardButton(text='начать тренировку')
    global_button_2 = types.KeyboardButton(text='посмотреть статистику')
    markup.add(global_button_1, global_button_2)
    bot.send_message(message.chat.id, f"Привет, {user}! Я телеграм-бот, который поможет ускорить твоё мышление, путём счёта в уме.", reply_markup=markup)
    bot.send_message(admin, text = f"в прогу зашёл @{username}")
    
@bot.message_handler(func=lambda message: message.text == 'посмотреть статистику')
def watch(message):
    bot.send_message(message.chat.id, text = f"Сложение-1: {example_sum_1}\nСложение-2: {example_sum_2}\nСложение-3: {example_sum_3}\n\nВычитание-1: {example_sub_1}\nВычитание-2: {example_sub_2}\nВычитание-3: {example_sub_3}\n\nУмножение-1: {example_mul_1}\nУмножени-2: {example_mul_2}\nУмножение-3: {example_mul_3}\n\nДеление-1: {example_share_1}\nДеление-2: {example_share_2}\nДеление-3: {example_share_3}\n\nНеправильно решённых примеров: {false}\nПравильно решённых примеров: {true}\nВсего решено примеров: {al}")
@bot.message_handler(func=lambda message: message.text == 'начать тренировку')
def start_training(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text='сложение')
    button_2 = types.KeyboardButton(text='вычитание')
    button_3 = types.KeyboardButton(text='умножение')
    button_4 = types.KeyboardButton(text='деление')
    markup.add(button_1, button_2, button_3, button_4)
    bot.send_message(message.chat.id, text='Выберите действие, которое будете выполнять', reply_markup=markup)
    bot.register_next_step_handler(message, symbols)

def symbols(message):
    action = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text='1')
    button_2 = types.KeyboardButton(text='2')
    button_3 = types.KeyboardButton(text='3')
    markup.add(button_1, button_2, button_3)
    bot.send_message(message.chat.id, f'Введите, из скольки символов должны состоять числа', reply_markup=markup)

    bot.register_next_step_handler(message, get_numbers_length, action)

def get_numbers_length(message, action):
    global us_symbols
    us_symbols = message.text
    random_numbers(message, action)

def random_numbers(message, action):
    if us_symbols in ['1', '2', '3']:
        global al
        global example_sum_1
        global example_sub_1
        global example_mul_1
        global example_share_1
        global example_sum_2
        global example_sub_2
        global example_mul_2
        global example_share_2
        global example_sum_3
        global example_sub_3
        global example_mul_3
        global example_share_3
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton(text='закончить')
        markup.add(button_1)
        al +=1

        if us_symbols == "1":
            
            if action == "сложение":
                example_sum_1 +=1
 
            elif action == "вычитание":
                example_sub_1 +=1

            elif action == "умножение":
                example_mul_1 +=1

            elif action == "деление":
                example_share_1 +=1

                
        elif us_symbols == "2":
            if action == "сложение":
                example_sum_2 +=1

            elif action == "вычитание":
                example_sub_2 +=1

            elif action == "умножение":
                example_mul_2 +=1

            elif action == "деление":
                example_share_2 +=1

        elif us_symbols == "3":
            if action == "сложение":
                example_sum_3 +=1

            elif action == "вычитание":
                example_sub_3 +=1
   
            elif action == "умножение":
                example_mul_3 +=1
              
            elif action == "деление":
                example_share_3 +=1
               
        first_symbol = random.randint(10**(int(us_symbols) - 1), 10**int(us_symbols) - 1)
        second_symbol = random.randint(10**(int(us_symbols) - 1), 10**int(us_symbols) - 1)
        bot.send_message(message.chat.id, text=f"{first_symbol} {get_operation_symbol(action)} {second_symbol} =", reply_markup=markup)
        bot.register_next_step_handler(message, actions, action, first_symbol, second_symbol)
    else:
        bot.send_message(message.chat.id, text="Извините, но в уме будет сложно посчитать больше 3 символов :(")

def get_operation_symbol(operation):
    if operation == 'сложение':
        return '+'
    elif operation == 'вычитание':
        return '-'
    elif operation == 'умножение':
        return '*'
    elif operation == 'деление':
        return '÷'

def actions(message, action, first_symbol, second_symbol):
    user_answer = message.text
    correct_answer = calculate_result(action, first_symbol, second_symbol)
    if user_answer == str(correct_answer):
        bot.send_message(message.chat.id, 'Правильно!')
        update_statistics(message.from_user.id, 'true')
        random_numbers(message, action)
    elif user_answer == 'закончить':
        start(message)
    else:
        bot.send_message(message.chat.id, f'Неправильно. Правильный ответ: {correct_answer}')
        update_statistics(message.from_user.id, 'false')
        random_numbers(message, action)

def calculate_result(action, first_symbol, second_symbol):
    if action == 'сложение':
        return first_symbol + second_symbol
    elif action == 'вычитание':
        return first_symbol - second_symbol
    elif action == 'умножение':
        return first_symbol * second_symbol
    elif action == 'деление':
        return first_symbol // second_symbol
def update_statistics(result):
    global false
    global true

    if result == 'true':
        true+=2
    else:
        false+=1

bot.polling()