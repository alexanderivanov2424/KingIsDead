import numpy as np

from GameState import *
from Constants import *
from search import runDFS, runRandomDFS


s = GameState()

s.struggles = np.array([MORAY, STRATHCLYDE, WARWICK, NORTHUMBRIA, DEVON, GWYNEDD, LANCASTER, ESSEX])
s.current_struggle = 6

s.regions = np.zeros((8,3), dtype=np.int8)
s.regions[LANCASTER,ENGLISH] = 1
s.regions[LANCASTER,SCOTTISH] = 1
s.regions[LANCASTER,WELSH] = 2
s.regions[ESSEX,ENGLISH] = 1
s.regions[ESSEX,SCOTTISH] = 2
s.regions[ESSEX,WELSH] = 0


s.resolved_regions[MORAY] = SCOTTISH
s.resolved_regions[STRATHCLYDE] = SCOTTISH
s.resolved_regions[NORTHUMBRIA] = SCOTTISH
s.resolved_regions[LANCASTER] = UNRESOLVED
s.resolved_regions[ESSEX] = UNRESOLVED
s.resolved_regions[WARWICK] = ENGLISH
s.resolved_regions[GWYNEDD] = WELSH
s.resolved_regions[DEVON] = ENGLISH

s.supply[ENGLISH] = 10 # didn't actually matter how many of each there were for this game so setting to 10
s.supply[SCOTTISH] = 10
s.supply[WELSH] = 10

s.player_turn = PLAYER_1
s.last_to_play = PLAYER_2

s.player_cards[PLAYER_1] = np.zeros(7, dtype=np.int8)
s.player_cards[PLAYER_1, CARD_ENGLISH_SUPPORT] = 1
s.player_cards[PLAYER_1, CARD_MANOEUVRE] = 1
s.player_cards[PLAYER_2] = np.zeros(7, dtype=np.int8)
s.player_cards[PLAYER_2, CARD_SCOTTISH_SUPPORT] = 0
s.player_cards[PLAYER_2, CARD_WELSH_SUPPORT] = 1
s.player_cards[PLAYER_2, CARD_MANOEUVRE] = 1
s.player_cards[PLAYER_2, CARD_ASSEMBLE] = 1

s.player_followers[PLAYER_1,ENGLISH] = 2
s.player_followers[PLAYER_1,SCOTTISH] = 3
s.player_followers[PLAYER_1,WELSH] = 3

s.player_followers[PLAYER_2,ENGLISH] = 5
s.player_followers[PLAYER_2,SCOTTISH] = 1
s.player_followers[PLAYER_2,WELSH] = 1

print(s)

# s = GameState(rand_init=True)
# states, actions, winner = runDFS(s)
states, actions, winner = runRandomDFS(s, branching=10)

print(f"Winner will be {'Player 1' if winner == PLAYER_1 else 'player 2'}")

for s,a in zip(states, actions):
    print(a)
    print(s)



assert(isEndGameState(s))
winner, win_type, coronation_rankings = winStats(s)
print(win_type)
print(" ".join(coronation_rankings))
print(f"Winner: {'Player 1' if winner == PLAYER_1 else 'player 2'}")
