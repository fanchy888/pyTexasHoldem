from deck import Deck
from poker_set import TexasPokerSet


class TexasPokerTable:
    def __init__(self, players):
        self.players = players
        self.total_players = len(players)
        self.deck = Deck()
        self.state = 0
        self.dealer = -1
        self.in_turn = 0
        self.pot = {}
        self.pool = []
        self.base_bet = 5
        self.current_bet = 0

    @property
    def active_player(self):
        return self.players[self.in_turn]

    @property
    def small_blind_player(self):
        return (self.dealer + 1) % self.total_players

    @property
    def big_blind_player(self):
        return (self.dealer + 2) % self.total_players

    def clear_status(self):
        for player in self.players:
            player.clear_status()
        self.in_turn = self.dealer
        self.next_turn()
        self.current_bet = 0

    def next_turn(self):
        for i in range(1, self.total_players):
            self.in_turn += 1
            self.in_turn %= self.total_players
            if not self.players[self.in_turn].folded:
                break

    def _call(self):
        player_id = self.active_player.player_id
        print("player call", player_id, self.current_bet)
        amount = self.current_bet - self.pot[player_id]
        self._bet(amount)

    def _raise(self, amount):
        player_id = self.active_player.player_id
        print("player raise", player_id, amount)
        self.current_bet += amount
        amount2bet = self.current_bet - self.pot[player_id]
        self._bet(amount2bet)

    def _fold(self):
        self.active_player.fold()

    def _bet(self, amount):
        print("player betting", self.active_player.player_id, amount)
        self.pot[self.active_player.player_id] += amount
        self.active_player.set_bet(amount)

    def _check(self):
        print("player check", self.active_player)

    def ready(self):
        self.deck.reset()
        self.deck.shuffle()
        self.dealer = (self.dealer + 1) % self.total_players
        self.in_turn = self.dealer
        self.pot = {i: 0 for i in range(self.total_players)}
        self.current_bet = 0

    def start(self):
        self.next_turn()

    def set_blind(self):
        self._bet(self.base_bet)
        self.next_turn()

        self._bet(self.base_bet * 2)
        self.current_bet = self.base_bet * 2
        self.next_turn()

    def dispatch_cards(self):
        for i in range(self.total_players):
            player_idx = (self.small_blind_player + i) % self.total_players
            cards = [self.deck.pick()]
            print('giving card to player', player_idx)
            self.players[player_idx].get_cards(cards)

    def take_action(self, action):
        if action['action'] == 'call':
            self._call()
        elif action['action'] == 'raise':
            self._raise(action['amount'])
        elif action['action'] == 'fold':
            self._fold()
        else:
            self._check()
        self.next_turn()

    def flop(self):
        if len(self.pool) < 5:
            c = self.deck.pick()
            self.pool.append(c)

    def showdown(self):
        alive_players = [p for p in self.players if not p.folded]



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
        self.cnt_of_same_value = sorted(list(value_distribute.values()))

    def is_royal(self):
        return self.is_straight_flush() and self.values[0] == 8

    def is_straight_flush(self):
        return self.is_straight() and self.is_flush()

    def is_four(self):
        return self.cnt_of_same_value[-1] == 4

    def is_full_house(self):
        return self.value_cnt == 2 and self.cnt_of_same_value[-1] == 3

    def is_flush(self):
        return self.color_cnt == 1

    def is_straight(self):
        special_straight = [i for i in range(self.size-1)]  # 2,3,4,5,A
        special_straight.append(12)

        return self.value_cnt == self.size and \
            (self.values == special_straight or self.values[-1] - self.values[0] + 1 == self.size)

    def is_three(self):
        return self.value_cnt == 3 and self.cnt_of_same_value[-1] == 3

    def is_two_pair(self):
        return self.value_cnt == 3 and self.cnt_of_same_value[-1] == 2

    def is_one_pair(self):
        return self.value_cnt == 4

    def rank(self):
        if self.is_royal():
            return 9
        elif self.is_straight_flush():
            return 8
        elif self.is_four():
            return 7
        elif self.is_full_house():
            return 6
        elif self.is_flush():
            return 5
        elif self.is_straight():
            return 4
        elif self.is_three():
            return 3
        elif self.is_two_pair():
            return 2
        elif self.is_one_pair():
            return 1
        else:
            return 0


if __name__ == '__main__':
    d = Deck()
    d.shuffle()
    cards1 = [d.pick() for i in [0, 1, 2, 3, 12]]
    for card in cards1:
        print(card)
    p = HandChecker(cards1)
    print(p.rank())

    cards1 = [d.pick() for i in [0, 1, 2, 3, 12]]
    for card in cards1:
        print(card)
    p = HandChecker(cards1)
    print(p.rank())
