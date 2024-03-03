from poker.deck import TexasPokerSet, Deck, Card


class HandChecker(TexasPokerSet):
    rank_order = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight",
                  "Flush", "Full House", "Four of a Kind", "Straight Flush"]

    def __init__(self, cards):
        self.cards = sorted(cards)
        self.size = len(self.cards)
        if self.size != 5:
            raise ValueError("card size must be 5")
        self.values = [c.value for c in self.cards]
        self.colors = [c.color for c in self.cards]
        self.color_cnt = len(set(self.colors))
        self.value_cnt = len(set(self.values))
        value_distribute = {}
        for c in self.cards:
            if c.value not in value_distribute:
                value_distribute[c.value] = 0
            value_distribute[c.value] += 1
        self.cnt_of_same_value = sorted(list(value_distribute.items()), key=lambda x: (x[1], x[0]))

    def is_royal(self):
        return self.is_straight_flush() and self.values[0] == 8

    def is_straight_flush(self):
        return self.is_straight() and self.is_flush()

    def is_four(self):
        return self.cnt_of_same_value[-1][1] == 4

    def is_full_house(self):
        return self.value_cnt == 2 and self.cnt_of_same_value[-1][1] == 3

    def is_flush(self):
        return self.color_cnt == 1

    def is_straight(self):
        special_straight = [i for i in range(self.size-1)]  # 2,3,4,5,A
        special_straight.append(12)

        return self.value_cnt == self.size and \
            (self.values == special_straight or self.values[-1] - self.values[0] + 1 == self.size)

    def is_three(self):
        return self.value_cnt == 3 and self.cnt_of_same_value[-1][1] == 3

    def is_two_pair(self):
        return self.value_cnt == 3 and self.cnt_of_same_value[-1][1] == 2

    def is_one_pair(self):
        return self.value_cnt == 4

    def rank(self):
        if self.is_royal():
            return 9, 0
        elif self.is_straight_flush():
            return 8, -1 if self.values[-1] == 12 and self.values[0] == 0 else self.values[-1]
        elif self.is_four():
            return 7, self.cnt_of_same_value[-1][0]
        elif self.is_full_house():
            return 6, self.cnt_of_same_value[-1][0]
        elif self.is_flush():
            return 5, tuple(self.values[::-1])
        elif self.is_straight():
            return 4, -1 if self.values[-1] == 12 and self.values[0] == 0 else self.values[-1]
        elif self.is_three():
            return 3, (self.cnt_of_same_value[-1][0], self.cnt_of_same_value[1][0], self.cnt_of_same_value[0][0])
        elif self.is_two_pair():
            return 2, (self.cnt_of_same_value[-1][0], self.cnt_of_same_value[1][0], self.cnt_of_same_value[0][0])
        elif self.is_one_pair():
            return 1, (self.cnt_of_same_value[-1][0], self.cnt_of_same_value[2][0], self.cnt_of_same_value[1][0],
                       self.cnt_of_same_value[0][0])
        else:
            return 0, tuple(self.values[::-1])


class Player:
    def __init__(self, player_id, name=''):
        self.player_id = player_id
        self.chips = 1000
        self.folded = False
        self.name = name
        self.acted = False
        self.cards = []
        self.rank = None
        self._result = []

    @property
    def final_cards(self):
        return self._result

    def ready(self):
        self.cards = []
        self.rank = None
        self.folded = False
        self.acted = False

    def act(self):
        self.acted = True

    def fold(self):
        self.folded = True

    def clear_status(self):
        self.acted = False

    def set_bet(self, amount):
        self.chips -= amount

    def get_cards(self, cards):
        self.cards = cards

    def cal_max_rank(self, pool):
        all_cards = self.cards + pool
        for i in range(7):
            for j in range(i+1, 7):
                cards = [c for k, c in enumerate(all_cards) if k != i and k != j]
                r = HandChecker(cards).rank()
                if self.rank is None:
                    self.rank = r
                    self._result = cards
                elif r[0] > self.rank[0]:
                    self.rank = r
                    self._result = cards
                elif r[0] == self.rank[0]:
                    if r[1] > self.rank[1]:
                        self.rank = r
                        self._result = cards


if __name__ == '__main__':
    p1 = Player(0)
    cards = [Card(1, 4, TexasPokerSet), Card(3, 8, TexasPokerSet)]
    p1.get_cards(cards)
    pool = [Card(3, 1, TexasPokerSet),
            Card(0, 4, TexasPokerSet),
            Card(1, 7, TexasPokerSet),
            Card(1, 3, TexasPokerSet),
            Card(0, 7, TexasPokerSet)]

    p1.cal_max_rank(pool)
    print([c.__str__() for c in p1.final_cards])