import time

from poker.player import Player
from poker.state import FSM, ReadyState, BeginState, ActionState, FirstFlopState, FlopState, ShowdownState, \
    EndState, FireRound, PreFlopRound, BetRound, AfterBetRound
from poker.texas import TexasPokerTable


class Game:
    def __init__(self):
        self.table = None
        self.count = 0
        self.players = []
        self.fsm = FSM()

    def join_player(self, name=None):
        player_id = self.count
        if name is None:
            name = f'player {player_id}'
        self.players.append(Player(player_id, name))
        self.count += 1

    def init_table(self):
        self.table = TexasPokerTable(self.players)

    def prepare(self):
        states = [
            ReadyState(self.table),  # 准备
            BeginState(self.table),  # 盲注， 发牌
            PreFlopRound(self.table),   # 第一轮下注
            FireRound(self.table),  # 补齐
            FirstFlopState(self.table),  # 翻牌
            BetRound('round2', self.table),   # 第二轮下注
            AfterBetRound('round2 after', self.table),  # 补齐
            FlopState('turn', self.table),  # 翻
            BetRound('round3', self.table),   # 第三轮下注
            AfterBetRound('round3 after', self.table),  # 补齐
            FlopState('river', self.table),  # 最后一张
            BetRound('final round', self.table),
            AfterBetRound('final round after', self.table),
            ShowdownState(self.table),  # 结算
            EndState(self.table)
        ]
        total = len(states)
        for i, state in enumerate(states):
            next_ids = (i + 1) % total
            state.set_next(states[next_ids])
            self.fsm.add_state(state)

    def ready(self):
        self.fsm.start('ready')

    def check_authority(self, player_id, action):
        if action['action'] == self.table.OK and self.table.mode == 'finish':
            return True
        return action['action'] in self.table.valid_actions and \
            self.table.active_player.player_id == player_id and not self.table.active_player.acted

    def player_move(self, player_id, action):
        if not self.table.is_waiting_for_action:
            return False

        if not self.check_authority(player_id, action):
            return False

        if action['action'] == TexasPokerTable.START:
            self.table.start()
        elif action['action'] == TexasPokerTable.OK:
            self.table.player_ready(player_id)
        else:
            self.table.take_action(action)
        self.fsm.run()
        self.broadcast()
        return True

    def controller_move(self):  # blinds, flop, showdown
        while not self.table.is_waiting_for_action:
            self.fsm.run()
            self.broadcast()
            # update to client

    def broadcast(self):
        # call after move
        self.table.info()