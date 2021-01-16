from telebot import TeleBot
from game import Game
from random import Random
from player import Player

bot = TeleBot('1015483974:AAFiuGMQB1CewhRP4JFbamvUZBjP9z3ytmw')

word = ''
game = Game(word, 6)
users = []
host = 0
player = 0
random = Random()


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.from_user.id, 'Привет')
    global users
    if len(users) >= 2:
        bot.send_message(message.from_user.id, 'Достигнуто максимальное количество игроков!')
        return
    users.append(Player(message.from_user.id, 0, message.from_user.username))
    if len(users) == 1:
        bot.send_message(message.from_user.id, 'Участников слишком мало, ожидайте')
    if len(users) == 2:
        global host, player
        host = 1
        player = 1 - host
        bot.send_message(users[host].id, 'Загадывайте слово')
        bot.send_message(users[player].id, 'Вы отгадываете слово. Подождите пока второй участник загадает слово')
        bot.register_next_step_handler(message, set_word2)


def set_word2(message):
    global word, game
    if message.from_user.id == users[host].id:
        word = message.text
        game = Game(word, 6)
        bot.send_message(users[host].id, 'Ваше слово загадано')
        bot.send_message(users[player].id, 'Второй участник загадал слово. Можете отгадывать')
        a = game.get_mask()
        b = game.lives
        bot.send_message(users[player].id, a + '\n' + str(b))
        bot.send_message(users[host].id, a + '\n' + str(b))


@bot.message_handler(commands=['play'])
def play(message):
    bot.send_message(message.from_user.id, 'Введите слово')


@bot.message_handler(func=lambda x:len(x.text)==1)
def abc(message):
    global host, player
    if game.game_over():
        bot.send_message(message.from_user.id, 'Начните игру')
        player = host
        host = 1 - player
        bot.send_message(users[host].id, 'Загадывайте слово')
        bot.send_message(users[player].id, 'Вы отгадываете слово. Подождите пока второй участник загадает слово')
        bot.register_next_step_handler(message, set_word2)
        return
    game.move(message.text[0])
    a = game.get_mask()
    b = game.lives
    bot.send_message(message.from_user.id, a + '\n' + str(b))
    bot.send_message(users[host].id, a + '\n' + str(b))
    if game.is_dead():
        bot.send_message(message.from_user.id, 'Вы проиграли! Попробуйте ещё раз')
        bot.send_message(message.from_user.id, 'Слово было: ' + word)
        if (users[player].points == 2 or users[host].points == 2) and player == 1:
            if users[player].points == 2 and users[host].points < 2:
                bot.send_message(users[player].id,
                                 'Поздравляю, вы набрали максимальное количество очков и выграли раунд!')
                bot.send_message(users[host].id, 'К сожалению, вы проиграли текущий раунд, так как ваш оппонент набрал '
                                                 'максимальное количество очков!')
            if users[host].points == 2 and users[player].points < 2:
                bot.send_message(users[host].id,
                                 'Поздравляю, вы набрали максимальное количество очков и выграли раунд!')
                bot.send_message(users[player].id, 'К сожалению, вы проиграли текущий раунд, так как ваш оппонент набрал '
                                                 'максимальное количество очков!')
            if users[player].points == 2 and users[host].points == 2:
                bot.send_message(users[player].id, 'Поздравляю, победила дружба :)')
                bot.send_message(users[host].id, 'Поздравляю, победила дружба :)')
            users[player].points = 0
            users[host].points = 0
        player = host
        host = 1 - player
        bot.send_message(users[host].id, 'Загадывайте слово')
        bot.send_message(users[player].id, 'Вы отгадываете слово. Подождите пока второй участник загадает слово')
        bot.register_next_step_handler(message, set_word2)
        return
    if game.is_won():
        bot.send_message(message.from_user.id, 'Поздравляю, вы выиграли!')
        users[player].points += 1
        bot.send_message(users[player].id, 'Ваши очки: ' + str(users[player].points))
        bot.send_message(users[host].id, 'Ваши очки: ' + str(users[host].points))
        if (users[player].points == 2 or users[host].points == 2) and player == 1:
            if users[player].points == 2 and users[host].points < 2:
                bot.send_message(users[player].id,
                                 'Поздравляю, вы набрали максимальное количество очков и выграли раунд!')
                bot.send_message(users[host].id, 'К сожалению, вы проиграли текущий раунд, так как ваш оппонент набрал '
                                                 'максимальное количество очков!')
            if users[host].points == 2 and users[player].points < 2:
                bot.send_message(users[host].id,
                                 'Поздравляю, вы набрали максимальное количество очков и выграли раунд!')
                bot.send_message(users[player].id, 'К сожалению, вы проиграли текущий раунд, так как ваш оппонент набрал '
                                                 'максимальное количество очков!')
            if users[player].points == 2 and users[host].points == 2:
                bot.send_message(users[player].id, 'Поздравляю, победила дружба :)')
                bot.send_message(users[host].id, 'Поздравляю, победила дружба :)')
            users[player].points = 0
            users[host].points = 0
        player = host
        host = 1 - player
        bot.send_message(users[host].id, 'Загадывайте слово')
        bot.send_message(users[player].id, 'Вы отгадываете слово. Подождите пока второй участник загадает слово')
        bot.register_next_step_handler(message, set_word2)
        return


bot.polling()
