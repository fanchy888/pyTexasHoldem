from deck import Deck, TexasPokerSet
from poker.player import Player


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
        for p in self.players:
            p.ready()

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
            cards = [self.deck.pick(), self.deck.pick()]
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
        self.active_player.act()
        self.next_turn()

    def flop(self):
        if len(self.pool) < 5:
            c = self.deck.pick()
            self.pool.append(c)

    def showdown(self):
        alive_players = [player for player in self.players if not player.folded]
        for player in alive_players:
            player.cal_max_rank(self.pool)

        alive_players.sort(key=lambda x: x.rank)
        return alive_players[-1].rank


if __name__ == '__main__':
    ps = [Player(i) for i in range(5)]
    game = TexasPokerTable(ps)
    game.ready()
    game.dispatch_cards()
    for i in range(5):
        game.flop()
    res = game.showdown()
    for r in res:
        print(r.rank)
        for c in r.final_cards:
            print(c)