class Game:
    def __init__(self, word, lives):
        self.word = word.upper()
        self.lives = lives
        self.guessed = [False] * len(word)

    def get_word(self):
        return self.word

    def get_mask(self):
        result = ""
        for i in range(len(self.word)):
            if not self.guessed[i]:
                result += "_ "
            if self.guessed[i]:
                result += self.word[i] + " "
        return result

    def move(self, ch):
        ch = ch.upper()
        if self.is_dead():
            return False
        if ch not in self.word:
            self.lives -= 1
            return False
        for i in range(len(self.word)):
            if ch == self.word[i]:
                self.guessed[i] = True
        return True

    def is_dead(self):
        return self.lives == 0

    def is_won(self):
        for i in self.guessed:
            if not i:
                return False
        return True

    def game_over(self):
        return self.is_dead() or self.is_won()
