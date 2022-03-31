import numpy as np
from functools import cmp_to_key
import copy as cp

from Actions import *
from Constants import *

"""
TODO:
maybe a nice print
"""

class GameState:

    def __init__(self, rand_init=False):
        self.struggles = np.arange(8) # values 1-8
        self.locked_struggles = np.zeros(8, dtype=np.int8) # 1 if locked
        self.current_struggle = 0

        self.regions = np.zeros((8,3), dtype=np.int8) #number of followers in each region
        self.resolved_regions = -1 * np.ones(8, dtype=np.int8) #-1 if not resolved, otherwise 0,1,2,3 for factions
        self.regions_adjacent = MAP

        self.supply = np.zeros(3, dtype=np.int8) #number of followers in supply

        self.player_turn = PLAYER_1 # 0 or 1
        self.last_to_play = PLAYER_2 # NO_LAST_PLAYED

        self.player_cards = np.ones((2,7), dtype=np.int8) #amount of each card
        self.player_cards[:,CARD_ASSEMBLE] = 2
        self.player_followers = np.zeros((2,3), dtype=np.int8) #followers of each faction

        self.passes = 0 #number of passes in a row so far

        """
        0 :: manoeuvre or outmanoeuvre
        1 :: region 1
        2 :: region 2
        3,4,5 :: amounts from region 1 to region 2
        6,7,8 :: amounts from region 2 to region 1
        """

        self.last_manoeuvre = np.zeros(9, dtype=np.int8)

        self.action = None #action that was taken to get to this state

        if rand_init:
            np.random.shuffle(self.struggles)

            self.regions[ESSEX,ENGLISH] = 2
            self.regions[MORAY,SCOTTISH] = 2
            self.regions[GWYNEDD,WELSH] = 2


            followers = np.array([ENGLISH for _ in range(14)] + [SCOTTISH for _ in range(14)] + [WELSH for _ in range(14)], dtype=np.int8)
            np.random.shuffle(followers)
            self.player_followers[PLAYER_1,followers[0]] += 1
            self.player_followers[PLAYER_1,followers[1]] += 1
            self.player_followers[PLAYER_2,followers[2]] += 1
            self.player_followers[PLAYER_2,followers[3]] += 1

            r = 0
            for i in range(4,len(followers)):
                if r < 8:
                    self.regions[r, followers[i]] += 1
                    if np.sum(self.regions[r]) == 4:
                        r += 1
                else:
                    self.supply[followers[i]] += 1

    def correctSupply(self):
        self.supply[ENGLISH] = 16 - np.sum(self.regions[:,ENGLISH]) - np.sum(self.player_followers[:,ENGLISH])
        self.supply[SCOTTISH] = 16 - np.sum(self.regions[:,SCOTTISH]) - np.sum(self.player_followers[:,SCOTTISH])
        self.supply[WELSH] = 16 - np.sum(self.regions[:,WELSH]) - np.sum(self.player_followers[:,WELSH])

    def copy(self):
        s = GameState()
        s.struggles = np.copy(self.struggles)
        s.locked_struggles = np.copy(self.locked_struggles)
        s.current_struggle = np.copy(self.current_struggle)
        s.regions = np.copy(self.regions)
        s.resolved_regions = np.copy(self.resolved_regions)
        s.regions_adjacent = np.copy(self.regions_adjacent)
        s.supply = np.copy(self.supply)

        s.player_turn = self.player_turn
        s.last_to_play = self.last_to_play
        s.player_cards = np.copy(self.player_cards)
        s.player_followers = np.copy(self.player_followers)

        s.passes = self.passes
        s.last_manoeuvre = np.copy(self.last_manoeuvre)

        s.action = cp.deepcopy(self.action)
        return s

    def __str__(self):
        struggle1 = REGION_NAMES_L14[self.struggles[0]]
        struggle2 = REGION_NAMES_L14[self.struggles[1]]
        struggle3 = REGION_NAMES_L14[self.struggles[2]]
        struggle4 = REGION_NAMES_L14[self.struggles[3]]
        struggle5 = REGION_NAMES_L14[self.struggles[4]]
        struggle6 = REGION_NAMES_L14[self.struggles[5]]
        struggle7 = REGION_NAMES_L14[self.struggles[6]]
        struggle8 = REGION_NAMES_L14[self.struggles[7]]

        val = ["" for _ in range(8)]
        for R in range(8):
            if self.resolved_regions[R] == UNRESOLVED:
                val[R] = f"({self.regions[R,ENGLISH]},{self.regions[R,SCOTTISH]},{self.regions[R,WELSH]})"
            else:
                val[R] = "(" + FACTION_NAMES_L5[self.resolved_regions[R]] + ")"

        suply_num = f"({self.supply[ENGLISH]},{self.supply[SCOTTISH]},{self.supply[WELSH]})"
        while len(suply_num) < 11:
            suply_num += " "
        f = "(" + str(3 - np.sum(self.resolved_regions == FRENCH)) + ")"
        turn = "PLAYER 1" if self.player_turn == PLAYER_1 else "PLAYER 2"
        last_play = "PLAYER 1" if self.last_to_play == PLAYER_1 else "PLAYER 2"

        crt_1 = f"({self.player_followers[PLAYER_1,ENGLISH]},{self.player_followers[PLAYER_1,SCOTTISH]},{self.player_followers[PLAYER_1,WELSH]})"
        crt_2 = f"({self.player_followers[PLAYER_2,ENGLISH]},{self.player_followers[PLAYER_2,SCOTTISH]},{self.player_followers[PLAYER_2,WELSH]})"

        r = PRINT_TEXT.format(struggle1 = struggle1,
                              struggle2 = struggle2,
                              struggle3 = struggle3,
                              struggle4 = struggle4,
                              struggle5 = struggle5,
                              struggle6 = struggle6,
                              struggle7 = struggle7,
                              struggle8 = struggle8,
                              val_0 = val[0],
                              val_1 = val[1],
                              val_2 = val[2],
                              val_3 = val[3],
                              val_4 = val[4],
                              val_5 = val[5],
                              val_6 = val[6],
                              val_7 = val[7],
                              suply_num = suply_num,
                              f = f,
                              turn = turn,
                              last_play = last_play,
                              crt_1 = crt_1,
                              crt_2 = crt_2)

        p1_cards = []
        for i in range(7):
            if self.player_cards[PLAYER_1,i] == 1:
                p1_cards.append(CARD_NAMES[i])
            elif self.player_cards[PLAYER_1,i] > 0:
                p1_cards.append(CARD_NAMES[i] + "     x" + str(self.player_cards[PLAYER_1,i]))


        p2_cards = []
        for i in range(7):
            if self.player_cards[PLAYER_2,i] == 1:
                p2_cards.append(CARD_NAMES[i])
            elif self.player_cards[PLAYER_2,i] > 0:
                p2_cards.append(CARD_NAMES[i] + "     x" + str(self.player_cards[PLAYER_2,i]))

        N = max(len(p1_cards), len(p2_cards))
        p1_cards.extend(["" for _ in range(N - len(p1_cards))])
        p2_cards.extend(["" for _ in range(N - len(p2_cards))])

        for card_p1, card_p2 in zip(p1_cards, p2_cards):
            r += f"{'    ' + card_p1 + ' '*(34 - len(card_p1))}#{'    ' + card_p2 + ' '*(38 - len(card_p2))}\n"
        r += " "*38 + "#" + " "*38 + "\n"
        return r


def summonFollower(s, zero_last_manoeuvre=True):
    next_states = []
    for r in range(8):
        for f in range(3):
            if s.resolved_regions[r] == UNRESOLVED and s.regions[r,f] > 0:
                next = s.copy()
                next.regions[r,f] -= 1
                next.player_followers[next.player_turn, f] += 1
                next.last_to_play = next.player_turn
                next.action.summon_region = r
                next.action.summon = f
                next.player_turn = (PLAYER_1 + PLAYER_2) - next.player_turn
                next.passes = 0
                if zero_last_manoeuvre:
                    next.last_manoeuvre = np.zeros(9)
                next_states.append(next)
    if len(next_states) == 0:
        assert(False, "unable to summon followers from this state")
    return next_states

def playEnglishSupport(s):

    if s.player_cards[s.player_turn, CARD_ENGLISH_SUPPORT] == 0:
        return []

    next_states = []
    n = min(s.supply[ENGLISH], 2)

    if n == 0:
        next = s.copy()
        next.player_cards[s.player_turn, CARD_ENGLISH_SUPPORT] -= 1
        next.action = ActionEnglishSupport(NO_REGION,0)
        next_states.extend(summonFollower(next))
        return next_states

    for source in range(8):
        if s.resolved_regions[source] != ENGLISH:
            continue
        for r in range(8):
            if s.resolved_regions[r] != UNRESOLVED: # must be resolved
                continue
            if s.regions_adjacent[source,r] == 0: # not adjacent
                continue

            next = s.copy()
            next.supply[ENGLISH] -= n
            next.regions[r,ENGLISH] += n
            next.player_cards[s.player_turn, CARD_ENGLISH_SUPPORT] -= 1
            next.action = ActionEnglishSupport(r,n)
            next_states.extend(summonFollower(next))

    if s.resolved_regions[ENGLISH_START] == UNRESOLVED:
        for r in range(8):
            if s.resolved_regions[r] != UNRESOLVED: # not resolved
                continue
            if s.regions_adjacent[ENGLISH_START,r] == 0: # not adjacent
                continue

            next = s.copy()
            next.supply[ENGLISH] -= n
            next.regions[r,ENGLISH] += n
            next.player_cards[s.player_turn, CARD_ENGLISH_SUPPORT] -= 1
            next.action = ActionEnglishSupport(r,n)
            next_states.extend(summonFollower(next))

    if len(next_states) == 0:
        next = s.copy()
        next.player_cards[s.player_turn, CARD_ENGLISH_SUPPORT] -= 1
        next.action = ActionEnglishSupport(NO_REGION,0)
        next_states.extend(summonFollower(next))
        return next_states

    return next_states

def playScottishSupport(s):
    if s.player_cards[s.player_turn, CARD_SCOTTISH_SUPPORT] == 0:
        return []

    next_states = []
    n = min(s.supply[SCOTTISH], 2)

    if n == 0:
        next = s.copy()
        next.player_cards[s.player_turn, CARD_SCOTTISH_SUPPORT] -= 1
        next.action = ActionScottishSupport(NO_REGION,0)
        next_states.extend(summonFollower(next))
        return next_states

    for source in range(8):
        if s.resolved_regions[source] != SCOTTISH:
            continue
        for r in range(8):
            if s.resolved_regions[r] != UNRESOLVED: # must be resolved
                continue
            if s.regions_adjacent[source,r] == 0: # not adjacent
                continue

            next = s.copy()
            next.supply[SCOTTISH] -= n
            next.regions[r,SCOTTISH] += n
            next.player_cards[s.player_turn, CARD_SCOTTISH_SUPPORT] -= 1
            next.action = ActionScottishSupport(r,n)
            next_states.extend(summonFollower(next))

    if s.resolved_regions[SCOTTISH_START] == UNRESOLVED:
        for r in range(8):
            if s.resolved_regions[r] != UNRESOLVED: # not resolved
                continue
            if s.regions_adjacent[SCOTTISH_START,r] == 0: # not adjacent
                continue

            next = s.copy()
            next.supply[SCOTTISH] -= n
            next.regions[r,SCOTTISH] += n
            next.player_cards[s.player_turn, CARD_SCOTTISH_SUPPORT] -= 1
            next.action = ActionScottishSupport(r,n)
            next_states.extend(summonFollower(next))

    if len(next_states) == 0:
        next = s.copy()
        next.player_cards[s.player_turn, CARD_SCOTTISH_SUPPORT] -= 1
        next.action = ActionScottishSupport(NO_REGION,0)
        next_states.extend(summonFollower(next))
        return next_states

    return next_states

def playWelshSupport(s):
    if s.player_cards[s.player_turn, CARD_WELSH_SUPPORT] == 0:
        return []

    next_states = []
    n = min(s.supply[WELSH], 2)

    if n == 0:
        next = s.copy()
        next.player_cards[s.player_turn, CARD_WELSH_SUPPORT] -= 1
        next.action = ActionWelshSupport(NO_REGION,0)
        next_states.extend(summonFollower(next))
        return next_states

    for source in range(8):
        if s.resolved_regions[source] != WELSH:
            continue
        for r in range(8):
            if s.resolved_regions[r] != UNRESOLVED: # must be resolved
                continue
            if s.regions_adjacent[source,r] == 0: # not adjacent
                continue

            next = s.copy()
            next.supply[WELSH] -= n
            next.regions[r,WELSH] += n
            next.player_cards[s.player_turn, CARD_WELSH_SUPPORT] -= 1
            next.action = ActionWelshSupport(r,n)
            next_states.extend(summonFollower(next))

    if s.resolved_regions[WELSH_START] == UNRESOLVED:
        for r in range(8):
            if s.resolved_regions[r] != UNRESOLVED: # not resolved
                continue
            if s.regions_adjacent[WELSH_START,r] == 0: # not adjacent
                continue

            next = s.copy()
            next.supply[WELSH] -= n
            next.regions[r,WELSH] += n
            next.player_cards[s.player_turn, CARD_WELSH_SUPPORT] -= 1
            next.action = ActionWelshSupport(r,n)
            next_states.extend(summonFollower(next))

    if len(next_states) == 0:
        next = s.copy()
        next.player_cards[s.player_turn, CARD_WELSH_SUPPORT] -= 1
        next.action = ActionWelshSupport(NO_REGION,0)
        next_states.extend(summonFollower(next))
        return next_states

    return next_states

def playAssemble(s):
    if s.player_cards[s.player_turn, CARD_ASSEMBLE] == 0:
        return []

    next_states = []

    for r1 in range(8) if s.supply[ENGLISH] > 0 else [NO_REGION]:
        if s.resolved_regions[r1] != UNRESOLVED:
            continue
        for r2 in range(8) if s.supply[SCOTTISH] > 0 else [NO_REGION]:
            if s.resolved_regions[r2] != UNRESOLVED:
                continue
            for r3 in range(8) if s.supply[WELSH] > 0 else [NO_REGION]:
                if s.resolved_regions[r3] != UNRESOLVED:
                    continue

                next = s.copy()
                if r1 != NO_REGION:
                    next.supply[ENGLISH] -= 1
                    next.regions[r1,ENGLISH] += 1
                if r2 != NO_REGION:
                    next.supply[SCOTTISH] -= 1
                    next.regions[r2,SCOTTISH] += 1
                if r3 != NO_REGION:
                    next.supply[WELSH] -= 1
                    next.regions[r3,WELSH] += 1

                next.player_cards[s.player_turn, CARD_ASSEMBLE] -= 1
                next.action = ActionAssemble(r1, r2, r3)
                next_states.extend(summonFollower(next))
    return next_states


def playNegotiate(s):
    if s.player_cards[s.player_turn, CARD_NEGOTIATE] == 0:
        return []

    next_states = []
    for c1 in range(s.current_struggle, 8):
        if s.locked_struggles[c1] == 1:
            continue
        for c2 in range(s.current_struggle, 8):
            if s.locked_struggles[c2] == 1:
                continue
            if c1 == c2:
                continue

            next = s.copy()
            t = next.struggles[c1]
            next.struggles[c1] = next.struggles[c2]
            next.struggles[c2] = t
            next.locked_struggles[c1] = 1
            next.player_cards[s.player_turn, CARD_NEGOTIATE] -= 1
            next.action = ActionNegotiate(next.struggles[c1], c1, next.struggles[c2], c2)
            next_states.extend(summonFollower(next))

    if len(next_states) == 0:
        next = s.copy()
        next.player_cards[s.player_turn, CARD_NEGOTIATE] -= 1
        next.action = ActionNegotiate(NO_REGION, -1, NO_REGION, -1)
        next_states.extend(summonFollower(next))
    return next_states

def playManoeuvre(s):
    if s.player_cards[s.player_turn, CARD_MANOEUVRE] == 0:
        return []

    next_states = []
    num_valid_regions = np.sum((np.sum(s.regions,axis=1) > 0) * (s.resolved_regions == UNRESOLVED))
    if num_valid_regions >= 2:
        for r1 in range(7):
            if s.resolved_regions[r1] != UNRESOLVED:
                continue
            for r2 in range(r1+1,8):
                if s.resolved_regions[r2] != UNRESOLVED:
                    continue

                for f1 in range(3):
                    if s.regions[r1,f1] == 0:
                        continue

                    for f2 in range(3):
                        if s.regions[r2,f2] == 0:
                            continue

                        comp = np.array([0, r1, r2] + [1 if i == f2 else 0 for i in range(3)] + [1 if i == f1 else 0 for i in range(3)], dtype=np.int8)
                        if np.array_equal(comp, s.last_manoeuvre):
                            continue

                        next = s.copy()
                        next.regions[r1,f1]-=1
                        next.regions[r2,f1]+=1
                        next.regions[r2,f2]-=1
                        next.regions[r1,f2]+=1
                        next.last_manoeuvre = np.array([0, r1, r2] + [1 if i == f1 else 0 for i in range(3)] + [1 if i == f2 else 0 for i in range(3)], dtype=np.int8)
                        next.player_cards[s.player_turn, CARD_MANOEUVRE] -= 1
                        next.action = ActionManoeuvre(r1, f1, r2, f2)
                        next_states.extend(summonFollower(next, zero_last_manoeuvre=False))
    else:
        next = s.copy()
        next.player_cards[s.player_turn, CARD_MANOEUVRE] -= 1
        next.action = ActionManoeuvre(NO_REGION, NO_FOLLOWER, NO_REGION, NO_FOLLOWER)
        next_states.extend(summonFollower(next))

    return next_states


def playOutmanoeuvre(s):
    if s.player_cards[s.player_turn, CARD_OUTMANOEUVRE] == 0:
        return []
    next_states = []

    for r1 in range(8):
        if s.resolved_regions[r1] != UNRESOLVED or np.sum(s.regions[r1]) < 2:
            continue
        for r2 in range(8):
            if s.resolved_regions[r2] != UNRESOLVED  or np.sum(s.regions[r1]) < 1:
                continue
            if s.regions_adjacent[r1,r2] == 0:
                continue

            for f1 in range(3):
                if s.regions[r1,f1] == 0:
                    continue

                for f2 in range(3):
                    if (s.regions[r1] - np.array([1 if i == f1 else 0 for i in range(3)], dtype=np.int8))[f2] == 0:
                        continue

                    for f3 in range(3):
                        if s.regions[r2,f3] == 0:
                            continue

                        source = np.array([1 if i == f1 else 0 for i in range(3)], dtype=np.int8) + np.array([1 if i == f2 else 0 for i in range(3)], dtype=np.int8)
                        dest = np.array([1 if i == f3 else 0 for i in range(3)])

                        comp = np.concatenate((np.array([1, r2, r1], dtype=np.int8),source,dest))
                        if np.array_equal(comp, s.last_manoeuvre):
                            continue

                        next = s.copy()
                        next.regions[r1,f1]-=1
                        next.regions[r1,f2]-=1
                        next.regions[r2,f1]+=1
                        next.regions[r2,f2]+=1

                        next.regions[r2,f3]-=1
                        next.regions[r1,f3]+=1
                        next.last_manoeuvre = np.concatenate((np.array([1, r1, r2], dtype=np.int8),source,dest))
                        next.player_cards[s.player_turn, CARD_OUTMANOEUVRE] -= 1
                        next.action = ActionOutmanoeuvre(r1, f1, f2, r2, f3)
                        next_states.extend(summonFollower(next, zero_last_manoeuvre=False))

    if len(next_states) != 0:
        return next_states

    for r1 in range(7):
        if s.resolved_regions[r1] != UNRESOLVED or np.sum(s.regions[r1]) < 1:
            continue
        for r2 in range(r1+1,8):
            if s.resolved_regions[r2] != UNRESOLVED  or np.sum(s.regions[r1]) < 1:
                continue
            if s.regions_adjacent[r1,r2] == 0:
                continue

            for f1 in range(3):
                if s.regions[r1,f1] == 0:
                    continue

                for f2 in range(3):
                    if s.regions[r2,f2] == 0:
                        continue

                    source = np.array([1 if i == f1 else 0 for i in range(3)], dtype=np.int8)
                    dest = np.array([1 if i == f2 else 0 for i in range(3)], dtype=np.int8)

                    comp = np.concatenate((np.array([1, r1, r2], dtype=np.int8),dest,source))
                    if np.array_equal(comp, s.last_manoeuvre):
                        continue

                    next = s.copy()
                    next.regions[r1,f1]-=1
                    next.regions[r2,f1]+=1

                    next.regions[r2,f2]-=1
                    next.regions[r1,f2]+=1
                    next.last_manoeuvre = np.concatenate((np.array([1, r1, r2], dtype=np.int8),source,dest))
                    next.player_cards[s.player_turn, CARD_OUTMANOEUVRE] -= 1
                    next.action = ActionOutmanoeuvre(r1, f1, NO_FOLLOWER, r2, f3)
                    next_states.extend(summonFollower(next, zero_last_manoeuvre=False))

    if len(next_states) != 0:
        return next_states

    next = s.copy()
    next.player_cards[s.player_turn, CARD_OUTMANOEUVRE] -= 1
    next.action = ActionOutmanoeuvre(NO_REGION, NO_FOLLOWER, NO_FOLLOWER, NO_REGION, NO_FOLLOWER)
    next_states.extend(summonFollower(next))

    return next_states


def playPass(s):
    next_states = []
    if s.passes == 0:
        next = s.copy()
        next.passes = 1
        next.player_turn = (PLAYER_1 + PLAYER_2) - next.player_turn
        next.action = ActionPass()
        next_states.append(next)
    if s.passes == 1:
        next = s.copy()
        r = next.struggles[next.current_struggle]
        factions = next.regions[r]
        if np.sum(factions == np.max(factions)) >= 2:
            next.resolved_regions[r] = FRENCH
        else:
            next.resolved_regions[r] = np.argmax(factions)
        next.supply += next.regions[r]
        next.regions[r] = 0
        next.current_struggle += 1
        next.passes = 0
        next.player_turn = (PLAYER_1 + PLAYER_2) - next.player_turn
        next.action = ActionPass()
        next_states.append(next)
    return next_states

def get_next_states(s):
    next_states = []
    cards = [playEnglishSupport, playScottishSupport, playWelshSupport, playManoeuvre, playOutmanoeuvre, playAssemble, playNegotiate]
    for card in cards:
        next_states.extend(card(s))
    next_states.extend(playPass(s))
    return next_states

def isEndGameState(s):
    if np.sum(s.resolved_regions == FRENCH) >= 3:
        assert(np.sum(s.resolved_regions == FRENCH) == 3) #game should end right when 3 go to France
        return True
    return s.current_struggle == 8 #last struggle was just resolved

def whoIsWinner(s):
    assert(isEndGameState(s))

    if np.sum(s.resolved_regions == FRENCH) == 3:
        # Invasion
        p1_sets = np.min(s.player_followers[PLAYER_1])
        p2_sets = np.min(s.player_followers[PLAYER_2])
        if p1_sets > p2_sets:
            return PLAYER_1
        elif p2_sets > p1_sets:
            return PLAYER_2
        else:
            return s.last_to_play

    else:
        #coronation
        English_control = np.sum(s.resolved_regions == ENGLISH)
        Scottish_control = np.sum(s.resolved_regions == SCOTTISH)
        Welsh_control = np.sum(s.resolved_regions == WELSH)

        resolutions = s.resolved_regions[s.struggles]
        English_last_resolve = -1 if np.sum(resolutions == ENGLISH) == 0 else np.max(np.where(resolutions == ENGLISH)[0])
        Scottish_last_resolve = -1 if np.sum(resolutions == SCOTTISH) == 0 else np.max(np.where(resolutions == SCOTTISH)[0])
        Welsh_last_resolve = -1 if np.sum(resolutions == WELSH) == 0 else np.max(np.where(resolutions == WELSH)[0])

        C = [(ENGLISH, English_control, English_last_resolve), (SCOTTISH, Scottish_control, Scottish_last_resolve), (WELSH, Welsh_control, Welsh_last_resolve)]

        def comp(faction1, faction2):
            if faction1[1] != faction2[1]:
                return faction2[1] - faction1[1]
            return faction2[2] - faction1[2]

        C = sorted(C, key=cmp_to_key(comp))

        faction1, faction2, faction3 = C[0][0], C[1][0], C[2][0]

        if s.player_followers[PLAYER_1,faction1] > s.player_followers[PLAYER_2,faction1]:
            return PLAYER_1
        elif s.player_followers[PLAYER_1,faction1] < s.player_followers[PLAYER_2,faction1]:
            return PLAYER_2
        else:
            if s.player_followers[PLAYER_1,faction2] > s.player_followers[PLAYER_2,faction2]:
                return PLAYER_1
            elif s.player_followers[PLAYER_1,faction2] < s.player_followers[PLAYER_2,faction2]:
                return PLAYER_2
            else:
                return (PLAYER_1 + PLAYER_2) - s.last_to_play


def winStats(s):
    assert(isEndGameState(s))

    winner = None
    win_type = None
    coronation_rankings = None

    if np.sum(s.resolved_regions == FRENCH) == 3:
        # Invasion
        win_type = "Invasion"
        p1_sets = np.min(s.player_followers[PLAYER_1])
        p2_sets = np.min(s.player_followers[PLAYER_2])
        if p1_sets > p2_sets:
            winner = PLAYER_1
        elif p2_sets > p1_sets:
            winner = PLAYER_2
        else:
            winner = s.last_to_play

    else:
        #coronation
        win_type = "Coronation"
        English_control = np.sum(s.resolved_regions == ENGLISH)
        Scottish_control = np.sum(s.resolved_regions == SCOTTISH)
        Welsh_control = np.sum(s.resolved_regions == WELSH)

        resolutions = s.resolved_regions[s.struggles]
        English_last_resolve = -1 if np.sum(resolutions == ENGLISH) == 0 else np.max(np.where(resolutions == ENGLISH)[0])
        Scottish_last_resolve = -1 if np.sum(resolutions == SCOTTISH) == 0 else np.max(np.where(resolutions == SCOTTISH)[0])
        Welsh_last_resolve = -1 if np.sum(resolutions == WELSH) == 0 else np.max(np.where(resolutions == WELSH)[0])

        C = [(ENGLISH, English_control, English_last_resolve), (SCOTTISH, Scottish_control, Scottish_last_resolve), (WELSH, Welsh_control, Welsh_last_resolve)]

        def comp(faction1, faction2):
            if faction1[1] != faction2[1]:
                return faction2[1] - faction1[1]
            return faction2[2] - faction1[2]

        C = sorted(C, key=cmp_to_key(comp))

        faction1, faction2, faction3 = C[0][0], C[1][0], C[2][0]

        coronation_rankings = (FACTION_NAMES[faction1], FACTION_NAMES[faction2], FACTION_NAMES[faction3])

        if s.player_followers[PLAYER_1,faction1] > s.player_followers[PLAYER_2,faction1]:
            winner = PLAYER_1
        elif s.player_followers[PLAYER_1,faction1] < s.player_followers[PLAYER_2,faction1]:
            winner = PLAYER_2
        else:
            if s.player_followers[PLAYER_1,faction2] > s.player_followers[PLAYER_2,faction2]:
                winner = PLAYER_1
            elif s.player_followers[PLAYER_1,faction2] < s.player_followers[PLAYER_2,faction2]:
                winner = PLAYER_2
            else:
                winner =  (PLAYER_1 + PLAYER_2) - s.last_to_play

    return winner, win_type, coronation_rankings
