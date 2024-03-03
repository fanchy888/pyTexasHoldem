from poker.game import Game


if __name__ == '__main__':

    game = Game()
    for i in range(5):
        game.join_player()

    game.init_table()
    game.prepare()
    game.ready()

    if game.player_move(0, action={'action': 'start'}):
        game.controller_move()
    print('pre fold==========================')
    if game.player_move(3, {'action': 'raise', 'amount': 10}):
        game.controller_move()
    if game.player_move(4, {'action': 'raise', 'amount': 10}):
        game.controller_move()
    if game.player_move(0, {'action': 'raise', 'amount': 10}):
        game.controller_move()
    if game.player_move(1, {'action': 'raise', 'amount': 10}):
        game.controller_move()

    if game.player_move(2, {'action': 'raise', 'amount': 10}):
        game.controller_move()

    print('---')
    if game.player_move(3, {'action': 'call'}):
        game.controller_move()
    if game.player_move(4, {'action': 'call'}):
        game.controller_move()
    if game.player_move(0, {'action': 'call'}):
        game.controller_move()
    if game.player_move(5, {'action': 'call'}):
        game.controller_move()
    if game.player_move(1, {'action': 'call'}):
        game.controller_move()
    if game.player_move(2, {'action': 'raise'}):
        game.controller_move()

    print('fold======================')
    if game.player_move(1, {'action': 'check'}):
        game.controller_move()
    if game.player_move(2, {'action': 'check'}):
        game.controller_move()
    if game.player_move(3, {'action': 'check'}):
        game.controller_move()
    if game.player_move(4, {'action': 'raise', 'amount': 5}):
        game.controller_move()
    if game.player_move(0, {'action': 'raise', 'amount': 5}):
        game.controller_move()

    print("---")
    if game.player_move(1, {'action': 'fold'}):
        game.controller_move()
    if game.player_move(2, {'action': 'fold'}):
        game.controller_move()
    if game.player_move(3, {'action': 'fold'}):
        game.controller_move()
    if game.player_move(4, {'action': 'fold'}):
        game.controller_move()
    if game.player_move(0, {'action': 'check', 'amount': 5}):
        game.controller_move()

    if game.player_move(2, {'action': 'ok'}):
        game.controller_move()
    if game.player_move(4, {'action': 'ok'}):
        game.controller_move()
    if game.player_move(0, {'action': 'check'}):
        game.controller_move()

    if game.player_move(3, {'action': 'check'}):
        game.controller_move()
    if game.player_move(4, {'action': 'check'}):
        game.controller_move()
    if game.player_move(0, {'action': 'check'}):
        game.controller_move()

    if game.player_move(3, {'action': 'check'}):
        game.controller_move()
    if game.player_move(4, {'action': 'check'}):
        game.controller_move()
    if game.player_move(0, {'action': 'check'}):
        game.controller_move()

    if game.player_move(3, {'action': 'check'}):
        game.controller_move()
    if game.player_move(4, {'action': 'check'}):
        game.controller_move()
    if game.player_move(0, {'action': 'check'}):
        game.controller_move()

