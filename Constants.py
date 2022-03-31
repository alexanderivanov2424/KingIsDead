import numpy as np

UNRESOLVED = -1
ENGLISH = 0
SCOTTISH = 1
WELSH = 2
FRENCH = 3

FACTION_NAMES = ["ENGLISH", "SCOTTISH", "WELSH", "FRENCH"]
FACTION_NAMES_L5 = ["ENGL ", "SCOTT", "WELSH", " FRN "]

NO_FOLLOWER = -1

NO_REGION = -1
MORAY = 0
STRATHCLYDE = 1
NORTHUMBRIA = 2
LANCASTER = 3
ESSEX = 4
WARWICK = 5
GWYNEDD = 6
DEVON = 7

REGION_NAMES = ["MORAY", "STRATHCLYDE", "NORTHUMBRIA", "LANCASTER", "ESSEX", "WARWICK", "GWYNEDD", "DEVON"]
REGION_NAMES_L14 = [n + " "*(11 - len(n)) for n in REGION_NAMES]

ENGLISH_START = ESSEX
SCOTTISH_START = MORAY
WELSH_START = GWYNEDD

CARD_ENGLISH_SUPPORT = 0
CARD_SCOTTISH_SUPPORT = 1
CARD_WELSH_SUPPORT = 2
CARD_MANOEUVRE = 3
CARD_OUTMANOEUVRE = 4
CARD_ASSEMBLE = 5
CARD_NEGOTIATE = 6

CARD_NAMES = ["English Support", "Scottish Support", "Welsh Support", "Manoeuvre", "Outmanoeuvre", "Assemble", "Negotiate"]

NO_WINNER = -1
NO_LAST_PLAYED = -1
PLAYER_1 = 0
PLAYER_2 = 1

MAP = np.zeros((8,8), dtype=np.int8)
pairs = []
pairs.append((MORAY,STRATHCLYDE))

pairs.append((STRATHCLYDE,LANCASTER))
pairs.append((STRATHCLYDE,NORTHUMBRIA))

pairs.append((LANCASTER,NORTHUMBRIA))
pairs.append((LANCASTER,GWYNEDD))
pairs.append((LANCASTER,WARWICK))

pairs.append((NORTHUMBRIA,WARWICK))
pairs.append((NORTHUMBRIA,ESSEX))

pairs.append((GWYNEDD,WARWICK))
pairs.append((GWYNEDD,DEVON))

pairs.append((WARWICK,ESSEX))
pairs.append((WARWICK,DEVON))

pairs.append((ESSEX,DEVON))

for p in pairs:
    MAP[p[0],p[1]] = 1
    MAP[p[1],p[0]] = 1


PRINT_TEXT = """
################################################################################
              #            \      /                              #
   1          #           \      /_ _ _       |                  #   5
  {struggle1} #        _| /            /      |    SUPPLY        #  {struggle5}
              #         _|   MORAY     |      |    {suply_num}   #
              #        / /\ {val_0}   /       |                  #
   2          #            \ _ _ _ _/_        | _ _ _ _ _ _ _ _  #   6
  {struggle2} #            |STRATHCLYDE \                        #  {struggle6}
              #           /   {val_1}    _\ _               N    #
              #         / _ _ _ _ _ _ _ /     \ _ _       __|__  #
   3          #              /        \ NORTHUMBRIA \       |    #   7
  {struggle3} #            / LANCASTER |  {val_2}   | _          #  {struggle7}
              #   _ _ _ _ |   {val_3}  |           /    \ _      #
              #   \        \  _ _ _ _ / _ _ _ _ _ /         \    #
   4          #    \ GWYNEDD \     WARWICK    /   ESSEX    /     #   8
  {struggle4} #   _ | {val_6}  \ _ {val_5}   |    {val_4} /_     #  {struggle8}
              #  /             /   \ _ _ _ _ /_             /    #
###############  \ _ _ _ _ _ /    DEVON         \ _ _ _ _ /      ###############
    (a,b,c)   #               _\  {val_7}    _ _ _ /        _ _  # Turn
a - ENGLISH   #       _ _ _ /          _ _ /          _ _ /      #   {turn}
b - SCOTTISH  #     / _ _ _ _ _ _ _ _/      _| \_ _ / FRANCE     # Last Played
c - WELSH     #                              \        {f}       #   {last_play}
################################################################################
     PLAYER 1          {crt_1}        #     PLAYER 2          {crt_2}
                                      #
"""
