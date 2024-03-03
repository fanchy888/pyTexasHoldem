import random


class NormalSet:
    COLORS = ['club', 'diamond', 'heart', 'spade']
    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


class TexasPokerSet:
    COLORS = ['club', 'diamond', 'heart', 'spade']
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Deck:
    def __init__(self, poser_set=TexasPokerSet):
        self.poker_set = poser_set
        self.color_cnt = len(self.poker_set.COLORS)
        self.value_cnt = len(self.poker_set.VALUES)
        self.total = self.value_cnt * self.color_cnt
        self._cards = []
        self._used = []
        for color in range(self.color_cnt):
            for value in range(self.value_cnt):
                card = Card(color, value, self.poker_set)
                self._cards.append(card)

    def __str__(self):
        return ','.join([c.__str__() for c in self._cards])

    def reset(self):
        while self._used:
            self._cards.append(self._used.pop())

    def order(self):
        self._cards.sort(key=lambda x: (x.color, x.value))

    def shuffle(self):
        print('shuffling...')
        random.shuffle(self._cards)

    def pick(self):
        c = self._cards.pop()
        self._used.append(c)
        return c

    def find(self, color, value):
        return Card(color, value, self.poker_set)


class Card:
    def __init__(self, color, value, poker_set):
        self.poker_set = poker_set
        self.color = color
        self.value = value

    @property
    def display_value(self):
        return self.poker_set.VALUES[self.value]

    @property
    def display_color(self):
        return self.poker_set.COLORS[self.color]

    def __str__(self):
        return f"{self.display_color}:{self.display_value}"

    def __lt__(self, other):
        return self.value < other.value if self.value != other.value else self.color < other.color

    def __gt__(self, other):
        return self.value > other.value if self.value != other.value else self.color > other.color

    def __eq__(self, other):
        return self.value == other.value and self.color == self.color
