from game import Game
word = "abba"
lives = 5
ch = 'A'
game = Game(word, lives)
print (game.get_word())
print (game.get_mask())
print (game.move(ch))
print (game.get_mask())