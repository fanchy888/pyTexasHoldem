
class FSM(object):
    def __init__(self):
        self.states = {}
        self.current_state = None

    def start(self, name):
        self.change_state(name)

    def add_state(self, state):
        self.states[state.name] = state

    def run(self):
        if self.current_state is None:
            return
        self.current_state.run()
        next_state = self.current_state.check()
        if next_state is not None and self.current_state.name != next_state:
            self.change_state(next_state)

    def change_state(self, next_state):
        if self.current_state is not None:
            self.current_state.stop()
        self.current_state = self.states[next_state]
        self.current_state.start()


class State:
    def __init__(self, name):
        self.name = name
        self.next_state = None

    def set_next(self, next_state):
        self.next_state = next_state

    def start(self):
        pass

    def check(self):
        pass

    def stop(self):
        pass

    def run(self):
        print('state', self.name)
        self._run()

    def _run(self):
        pass


class ReadyState(State):
    def __init__(self, table):
        super().__init__('ready')
        self.table = table

    def start(self):
        self.table.state = 0
        self.table.ready()

    def check(self):
        if self.table.started:
            return self.next_state.name
        return None

    def stop(self):
        self.table.state = 1


class BeginState(State):
    def __init__(self, table):
        super().__init__('start')
        self.table = table

    def start(self):
        self.table.set_blind()

    def check(self):
        if self.table.started and self.table.state == 1:
            return self.next_state.name
        return None

    def stop(self):
        self.table.dispatch_cards()
        self.table.state = 2


class ActionState(State):
    def __init__(self, name, table):
        super().__init__(name)
        self.table = table

    def check(self):

        if self.table.all_acted():
            return self.next_state.name
        return None

    def stop(self):
        self.table.clear_status()
        self.table.state += 1


class PreFlopRound(ActionState):
    def __init__(self, table):
        super().__init__('pre flop round', table)

    def start(self):
        self.table.clear_status()
        self.table.begin_bet()
        self.table.in_turn = self.table.big_blind_player
        self.table.next_turn()


class FireRound(ActionState):
    def __init__(self, table):
        super().__init__('fire', table)

    def start(self):
        self.table.in_turn = self.table.big_blind_player
        self.table.active_player.act()
        self.table.next_turn()
        self.table.after_bet()


class BetRound(ActionState):
    def start(self):
        self.table.begin_bet()
        self.table.round_start()


class AfterBetRound(ActionState):
    def start(self):
        self.table.begin_bet()
        self.table.round_start()

    def check(self):
        if self.table.check_finish():
            return 'show down'
        return super().check()


class FirstFlopState(State):
    def __init__(self, table):
        super().__init__('first flop')
        self.table = table

    def check(self):
        if self.table.state == 4:
            return self.next_state.name
        return None

    def stop(self):
        self.table.flop()
        self.table.flop()
        self.table.flop()
        self.table.clear_status()
        self.table.state += 1


class FlopState(State):
    def __init__(self, name, table):
        super().__init__(name)
        self.table = table

    def check(self):
        if self.table.state >= 7:
            return self.next_state.name
        return None

    def stop(self):
        self.table.flop()
        self.table.state += 1


class ShowdownState(State):
    def __init__(self, table):
        super().__init__('show down')
        self.table = table

    def start(self):
        self.table.state = 13
        self.table.terminate()
        self.table.showdown()

    def check(self):
        if self.table.all_ready():
            return self.next_state.name
        return None


class EndState(State):
    def __init__(self, table):
        super().__init__('end')
        self.table = table

    def start(self):
        self.table.end()


