from deck import Deck, TexasPokerSet
from poker.player import Player


class TexasPokerTable:  # 记录牌局状态
    START = 'start'
    CALL = 'call'
    RAISE = 'raise'
    FOLD = 'fold'
    CHECK = 'check'
    OK = 'ok'

    def __init__(self, players):
        self.players = players
        self.total_players = len(players)
        self.deck = Deck()
        self.state = 0
        self.dealer = 0
        self.in_turn = 0
        self.pot = {}
        self.pool = []
        self.base_bet = 5
        self.current_bet = 0
        self.started = False
        self.final_result = None
        self.mode = 'bet'

    @property
    def active_player(self):
        return self.players[self.in_turn]

    @property
    def small_blind_player(self):
        return (self.dealer + 1) % self.total_players

    @property
    def big_blind_player(self):
        return (self.dealer + 2) % self.total_players

    @property
    def is_waiting_for_action(self):
        return self.state in [0, 2, 3, 5, 6, 8, 9, 11, 12, 13]

    @property
    def valid_actions(self):
        if self.is_waiting_for_action:
            if not self.started:
                return [self.START]
            elif self.mode == 'bet':
                return [self.RAISE, self.FOLD, self.CALL, self.CHECK]
            elif self.mode == 'after':
                return [self.FOLD, self.CHECK, self.CALL]
            elif self.mode == 'finish':
                return [self.OK]
        else:
            return []

    def begin_bet(self):
        self.mode = 'bet'

    def after_bet(self):
        self.mode = 'after'

    def terminate(self):
        self.mode = 'finish'

    def all_acted(self):
        for p in self.players:
            if not p.folded:
                if not p.acted:
                    return False
        return True

    def all_ready(self):
        for p in self.players:
            if not p.acted:
                return False
        return True

    def clear_status(self):
        for player in self.players:
            player.clear_status()

    def round_start(self):
        self.in_turn = self.dealer
        self.next_turn()

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
        print("player fold", self.active_player.name)
        self.active_player.fold()

    def _bet(self, amount):
        print("player betting", self.active_player.player_id, amount)
        self.pot[self.active_player.player_id] += amount
        self.active_player.set_bet(amount)

    def _check(self):
        print("player check", self.active_player.name)

    def player_ready(self, player_id):
        print("player ready", self.players[player_id].name)
        self.players[player_id].act()

    def ready(self):
        self.started = False
        self.final_result = None
        self.deck.shuffle()
        self.in_turn = self.dealer
        self.pot = {i: 0 for i in range(self.total_players)}
        self.current_bet = 0
        self.pool = []
        for p in self.players:
            p.ready()

    def start(self):
        self.started = True
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
        if action['action'] == self.CALL:
            self._call()
        elif action['action'] == self.RAISE:
            self._raise(action['amount'])
        elif action['action'] == self.FOLD:
            self._fold()
        elif action['action'] == self.CHECK:
            self._check()
        else:
            print("not supported", action)
            self._check()
        self.active_player.act()
        self.next_turn()

    def flop(self):
        if len(self.pool) < 5:
            card = self.deck.pick()
            self.pool.append(card)

    def check_finish(self):
        finished = len([p for p in self.players if not p.folded]) == 1
        return finished

    def showdown(self):
        alive_players = [player for player in self.players if not player.folded]
        if not self.check_finish():
            for player in alive_players:
                player.cal_max_rank(self.pool)

            alive_players.sort(key=lambda x: x.rank)
        self.final_result = alive_players
        # print('final result========')
        # for c in self.pool:
        #     print(c)
        # for a in self.final_result:
        #     print(a.name, a.rank, [c.__str__() for c in a.cards])
        #     for c in a.final_cards:
        #         print(c)
        #     print('-------')

    def end(self):
        self.dealer = (self.dealer + 1) % self.total_players
        self.state = 0
        self.started = False
        self.deck.reset()

    def info(self):
        print('---info---')
        print(self.state)
        print(self.pot, self.current_bet)
        print(self.pool)
        print(self.active_player.name)
        print('==========')
