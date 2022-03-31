
from GameState import *
from Actions import *
from Constants import *


def runDFS(s): #return next states, next actions to take, final winner
    current_player = s.player_turn
    other_player = (PLAYER_1 + PLAYER_2) - current_player

    next_states = get_next_states(s)
    states = []
    actions = []

    states_to_no_winner = []
    actions_to_no_winner = []

    states_to_loss = []
    actions_to_loss = []

    for next in next_states:
        if isEndGameState(next) and whoIsWinner(next) == current_player:
            return [next], [next.action], current_player
        elif isEndGameState(next):
            if whoIsWinner(next) == NO_WINNER and len(actions_to_no_winner) < 1:
                states_to_no_winner = [next]
                actions_to_no_winner = [next.action]
            if whoIsWinner(next) == other_player and len(actions_to_loss) < 1:
                states_to_loss = [next]
                actions_to_loss = [next.action]
            continue

        states, actions, future_winner = getBestAction(next)

        if future_winner == current_player:
            return [next] + states, [next.action] + actions, current_player
        else:
            if future_winner == NO_WINNER and len(actions_to_no_winner) < len(actions) + 1:
                states_to_no_winner = [next] + states
                actions_to_no_winner = [next.action] + actions
            if future_winner == other_player and len(actions_to_loss) < len(actions) + 1:
                states_to_loss = [next] + states
                actions_to_loss = [next.action] + actions

    if len(states_to_no_winner) == 0:
        return states_to_loss, actions_to_loss, other_player
    else:
        return states_to_no_winner, actions_to_no_winner, NO_WINNER
