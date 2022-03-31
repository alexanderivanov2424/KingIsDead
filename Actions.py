from Constants import *

class Action:
    def __init__(self):
        self.summon_region = None
        self.summon = None
    def __str__(self):
        return f"Summon {FACTION_NAMES[self.summon]} from {REGION_NAMES[self.summon_region]}\n"

class ActionEnglishSupport(Action):
    def __init__(self, region, amount):
        self.region = region
        self.amount = amount

    def __str__(self):
        return f"English Support {REGION_NAMES[self.summon_region]} with {self.amount}\n" + Action.__str__(self)

class ActionScottishSupport(Action):
    def __init__(self, region, amount):
        self.region = region
        self.amount = amount

    def __str__(self):
        return f"Scottish Support {REGION_NAMES[self.summon_region]} with {self.amount}\n" + Action.__str__(self)

class ActionWelshSupport(Action):
    def __init__(self, region, amount):
        self.region = region
        self.amount = amount

    def __str__(self):
        return f"Welsh Support {REGION_NAMES[self.summon_region]} with {self.amount}\n" + Action.__str__(self)

class ActionAssemble(Action):
    def __init__(self, english_r, scottish_r, welsh_r):
        self.english_r = english_r
        self.scottish_r = scottish_r
        self.welsh_r = welsh_r

    def __str__(self):
        r = "Assemble "
        r += f"{'no ENGLISH ' if self.english_r == NO_REGION else 'ENGLISH in ' + REGION_NAMES[self.english_r]}, "
        r += f"{'no SCOTTISH ' if self.scottish_r == NO_REGION else 'SCOTTISH in ' + REGION_NAMES[self.scottish_r]}, "
        r += f"{'no WELSH ' if self.welsh_r == NO_REGION else 'WELSH in ' + REGION_NAMES[self.welsh_r]},\n"
        return r + Action.__str__(self)


class ActionNegotiate(Action):
    def __init__(self, struggle_1, new_pos_1, struggle_2, new_pos_2):
        self.struggle_1 = struggle_1
        self.new_pos_1 = new_pos_1
        self.struggle_2 = struggle_2
        self.new_pos_2 = new_pos_2

    def __str__(self):
        return f"Negotiate {REGION_NAMES[self.struggle_1]} to struggle {self.new_pos_1 + 1} and {REGION_NAMES[self.struggle_2]} to struggle {self.new_pos_2 + 1}\n" + Action.__str__(self)

class ActionManoeuvre(Action):
    def __init__(self, first_region, first_follower, second_region, second_follower):
        self.first_region = first_region
        self.first_follower = first_follower
        self.second_region = second_region
        self.second_follower = second_follower

    def __str__(self):
        if self.first_region == NO_REGION or self.second_region == NO_REGION:
            return "Manoeuvre nothing\n" + Action.__str__(self)
        r = "Manoeuvre "
        r += f"{FACTION_NAMES[self.first_follower]} from {REGION_NAMES[self.first_region]} to {REGION_NAMES[self.second_region]}\n"
        r += f"{FACTION_NAMES[self.second_follower]} from {REGION_NAMES[self.second_region]} to {REGION_NAMES[self.first_region]}\n"
        return r + Action.__str__(self)

class ActionOutmanoeuvre(Action):
    def __init__(self, first_region, first_follower1, first_follower2, second_region, second_follower):
        self.first_region = first_region
        self.first_follower1 = first_follower1
        self.first_follower2 = first_follower2
        self.second_region = second_region
        self.second_follower = second_follower

    def __str__(self):
        if self.first_region == NO_REGION or self.second_region == NO_REGION:
            return "Outmanoeuvre nothing\n" + Action.__str__(self)
        r = "Manoeuvre "
        r += f"{FACTION_NAMES[self.first_follower1]} from {REGION_NAMES[self.first_region]} to {REGION_NAMES[self.second_region]}\n"
        r += f"{FACTION_NAMES[self.first_follower2]} from {REGION_NAMES[self.first_region]} to {REGION_NAMES[self.second_region]}\n"
        r += f"{FACTION_NAMES[self.second_follower]} from {REGION_NAMES[self.second_region]} to {REGION_NAMES[self.first_region]}\n"
        return r + Action.__str__(self)

class ActionPass(Action):
    def __init__(self):
        pass

    def __str__(self):
        return "Pass\n"
