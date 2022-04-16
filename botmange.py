import telebot
from telebot import types
import dbmanage
import temp

token = temp.bottoken
bot = telebot.TeleBot(token)
link: str
idflat: str


@bot.message_handler(commands=['start'])
def start_function(message):
    user_id = message.from_user.id
    username = message.from_user.username
    count_1room = dbmanage.count_flats(1)
    count_2room = dbmanage.count_flats(2)
    count_3room = dbmanage.count_flats(3)
    dbmanage.set_user(user_id, username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton(f"Однакомнатные квартиры ({count_1room})")
    but2 = types.KeyboardButton(f"Двухкомнатные квартиры ({count_2room})")
    but3 = types.KeyboardButton(f"Трехкомнатные квартиры ({count_3room})")
    markup.add(but1, but2, but3)
    bot.send_message(user_id, "Поиск аренды квартир в Минске", reply_markup=markup)


@bot.message_handler(content_types='text')
def button_message(message):
    global link
    global idflat
    user_id = message.from_user.id
    countflats = dbmanage.count_save_flats(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Дальше")
    but2 = types.KeyboardButton("Сохранить")
    but3 = types.KeyboardButton("Ссылка")
    but4 = types.KeyboardButton("/start")
    but5 = types.KeyboardButton(f"Сохраненные ({countflats})")
    markup.add(but1, but2, but3, but4, but5)
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but6 = types.KeyboardButton("Следущая")
    but7 = types.KeyboardButton("Удалить")
    but8 = types.KeyboardButton("/start")
    markup1.add(but6, but7, but8)
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but9 = types.KeyboardButton("/start")
    markup2.add(but9)


    def choose_flat(room):
        global idflat
        global link
        dbmanage.data_select(room)
        mess = dbmanage.get_data()
        link = mess[5]
        idflat = mess[0]
        agency = dbmanage.check_agency(mess[4])
        bot.send_message(user_id, f'{mess[2]}\n{mess[3]}\n{mess[4]}\n{agency}', reply_markup=markup)

    if "Однакомнатные квартиры" in message.text:
        choose_flat(1)
    elif "Двухкомнатные квартиры" in message.text:
        choose_flat(2)
    elif "Трехкомнатные квартиры" in message.text:
        choose_flat(3)

    elif message.text == "Дальше":
        mess = dbmanage.get_data()
        link = mess[5]
        idflat = mess[0]
        agency = dbmanage.check_agency(mess[4])
        bot.send_message(user_id, f'{mess[2]}\n{mess[3]}\n{mess[4]}\n{agency}', reply_markup=markup)
    elif message.text == "Ссылка":
        bot.send_message(user_id, f'{link}', reply_markup=markup)
    elif message.text == "Сохранить":
        flats = dbmanage.select_save_flat(user_id)
        if idflat in flats:
            bot.send_message(user_id, 'Уже сохранено', reply_markup=markup)
        else:
            dbmanage.save_flat(idflat, user_id)
            bot.send_message(user_id, 'Cохранено', reply_markup=markup)
    elif "Сохраненные" in message.text:
        messflats = dbmanage.get_save_flats_for_user(user_id)
        idflat = messflats[4]
        bot.send_message(user_id, f'{messflats[0]}\n{messflats[1]}\n{messflats[2]}\n{messflats[3]}',
                         reply_markup=markup1)
    elif message.text == "Следущая":
        messflats = dbmanage.get_next_save_flats()
        if messflats is None:
            bot.send_message(user_id, 'В вашем списке сохраненных квартир ничего не осталось', reply_markup=markup2)
        else:
            idflat = messflats[4]
            bot.send_message(user_id, f'{messflats[0]}\n{messflats[1]}\n{messflats[2]}\n{messflats[3]}',
                             reply_markup=markup1)
    elif message.text == "Удалить":
        print(idflat)
        dbmanage.delete_flat(user_id, idflat)
        bot.send_message(user_id, 'Удалено', reply_markup=markup1)


bot.infinity_polling()
