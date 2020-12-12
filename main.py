from telebot import TeleBot
from game import

bot = TeleBot('1015483974:AAFiuGMQB1CewhRP4JFbamvUZBjP9z3ytmw')

word = ''
game = Game(word, 6)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.from_user.id, 'Привет')
    global game
    game = Game(word, 6)


@bot.message_handler(commands=['set_word'])
def set_word(message):
    bot.send_message(message.from_user.id, 'Введите слово')
    bot.register_next_step_handler(message, set_word2)


def set_word2(message):
    global word
    word = message.text


@bot.message_handler(commands=['play'])
def play(message):
    bot.send_message(message.from_user.id, 'Введите слово')


@bot.message_handler(func=lambda x:len(x.text)==1)
def abc(message):
    if game.game_over():
        bot.send_message(message.from_user.id, 'Начните игру')
        return
    game.move(message.text[0])
    a = game.get_mask()
    b = game.lives
    bot.send_message(message.from_user.id, a + '\n' + str(b))
    if game.is_dead():
        bot.send_message(message.from_user.id, 'Вы проиграли! Попробуйте ещё раз')
        return
    if game.is_won():
        bot.send_message(message.from_user.id, 'Поздравляю, вы выиграли!')
        return


bot.polling()
