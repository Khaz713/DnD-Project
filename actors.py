import random
import math

DAMAGE_TYPES = ['Acid', 'Bludgeoning', 'Bludgeoning from non magical attacks', 'Cold', 'Damage dealt by traps',
                'Damage from spells', 'Fire', 'Force', 'Lightning', 'Necrotic', 'Piercing', 'Poison', 'Psychic',
                'Radiant', 'Ranged Attacks', 'Slashing', 'Thunder']


class Character:
    def __init__(self, name):
        self.name = name

    max_hp = 0
    hp = 0
    temp_hp = 0
    inspiration = False
    ac = 0
    initiative = 0
    size = None
    classes = []
    hit_die = {'1d6': [0, 0], '1d8': [0, 0], '1d10': [0, 0], '1d12': [0, 0]}  # [0] = current, [1] = max
    race = None
    stats = {'str': [0, 0, 0, 0, 0], 'dex': [0, 0, 0, 0, 0], 'con': [0, 0, 0, 0, 0], 'wis': [0, 0, 0, 0, 0],
             'int': [0, 0, 0, 0, 0], 'cha': [0, 0, 0, 0, 0]}
    # [0] == rolled_score, [1] == bonus_score, [2] == total score, [3] == mod, [4] == race
    saving_throw = {'str': [False, 0], 'dex': [False, 0], 'con': [False, 0], 'wis': [False, 0], 'int': [False, 0],
                    'cha': [False, 0]}  # [0] == prof, [1] == mod
    level = 1
    exp = 0
    level_up_table = {1: 300, 2: 900, 3: 2700, 4: 6500, 5: 14000, 6: 23000, 7: 34000, 8: 48000, 9: 64000, 10: 85000,
                      11: 100000, 12: 120000, 13: 140000, 14: 165000, 15: 195000, 16: 225000, 17: 265000, 18: 305000,
                      19: 355000, 20: 'MAX'}
    proficiency_bonus_table = {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5,
                               15: 5, 16: 5, 17: 6, 18: 6, 19: 6, 20: 6}
    skills_table = {'Acrobatics': [False, 0, 'dex', False], 'Animal Handling': [False, 0, 'wis', False],
                    'Arcana': [False, 0, 'int', False], 'Athletics': [False, 0, 'str', False],
                    'Deception': [False, 0, 'cha', False], 'History': [False, 0, 'int', False],
                    'Insight': [False, 0, 'wis', False], 'Intimidation': [False, 0, 'cha', False],
                    'Investigation': [False, 0, 'int', False], 'Medicine': [False, 0, 'wis', False],
                    'Nature': [False, 0, 'int', False], 'Perception': [False, 0, 'wis', False],
                    'Performance': [False, 0, 'cha', False], 'Persuasion': [False, 0, 'cha', False],
                    'Religion': [False, 0, 'int', False], 'Sleight of Hand': [False, 0, 'dex', False],
                    'Stealth': [False, 0, 'dex', False],
                    'Survival': [False, 0, 'wis', False]}  # [0] == prof, [1] == bonus, [2] == mod, [3] == expertise
    senses = {'Blindsight': [False, 0], 'Darkvision': [False, 0], 'Tremorsense': [False, 0], 'Truesight': [False, 0]}
    passive_stats = {'Perception': [False, 0, 'wis'], 'Investigation': [False, 0, 'int'],
                     'Insight': [False, 0, 'wis']}
    movement = {'Burrowing': [False, 0], 'Climbing': [False, 0], 'Flying': [False, 0], 'Swimming': [False, 0],
                'Walking': [False, 0]}
    defenses = {}
    conditions = {}
    advantages = {}
    saving_throw_advantages = []
    proficiencies = {'Armor': [], 'Weapons': [], 'Tools': [], 'Languages': []}
    spell_list = []  # TODO: create spell class and import list from csv
    spell_slots = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0], 5: [0, 0], 6: [0, 0], 7: [0, 0], 8: [0, 0], 9: [0, 0]}
    equipment = []  # TODO: create equipment class and import list from csv
    money = {'Platinum': 0, 'Gold': 0, 'Electrum': 0, 'Silver': 0, 'Copper': 0}

    def roll_skill(self, skill):
        return [random.randint(1, 20), self.skills_table[skill][1]]

    def roll_saving_throw(self, save, damage):
        if damage in self.saving_throw_advantages:
            return [[random.randint(1, 20), self.saving_throw[save][1]],
                    [random.randint(1, 20), self.saving_throw[save][1]]]
        else:
            return [random.randint(1, 20), self.saving_throw[save][1]]

    def update_skills_value(self):
        for skill_name in self.skills_table.keys():
            if self.skills_table[skill_name][3]:
                self.skills_table[skill_name][1] = self.stats[self.skills_table[skill_name][2]][2] + (
                        self.proficiency_bonus_table[self.level] * 2)
            elif self.skills_table[skill_name][0]:
                self.skills_table[skill_name][1] = self.stats[self.skills_table[skill_name][2]][2] + (
                    self.proficiency_bonus_table[self.level])

            else:
                self.skills_table[skill_name][1] = self.stats[self.skills_table[skill_name][2]][2]
            if skill_name in self.passive_stats:
                self.passive_stats[skill_name][1] = 10 + self.skills_table[skill_name][1]

    def update_stats_value(self):
        for stat_name in self.stats.keys():
            self.stats.get(stat_name)[2] = self.stats[stat_name][0] + self.stats[stat_name][1]
            self.stats[stat_name][3] = math.floor((self.stats[stat_name][2] - 10) / 2)
            if self.saving_throw[stat_name][0]:
                self.saving_throw[stat_name][1] = self.stats[stat_name][3] + self.proficiency_bonus_table[self.level]
            else:
                self.saving_throw[stat_name][1] = self.stats[stat_name][3]
        self.initiative = self.stats['dex'][3]

    def update_proficiencies(self):
        _class: Classes
        for _class in self.classes:
            _dict = _class.get_proficiencies()
            for key in _dict:
                self.proficiencies[key] = list(dict.fromkeys(self.proficiencies[key] + _dict[key]))

    def set_senses(self, sense, distance):
        if distance > 0:
            self.senses[sense] = [True, distance]
        else:
            self.senses[sense] = [False, 0]

    def add_exp(self, points):
        self.exp += points
        if self.exp >= self.level_up_table[self.level]:
            self.level += 1
            # TODO: level up sequence

    def add_defence(self, defence: str, multiplayer: float, def_type: str):
        self.defenses[defence] = [multiplayer, def_type]
        # defence = type of damage/condition, multiplayer = 0, 0.5, 2, def_type ='immunity','resistance','vulnerability'

    def remove_defence(self, name):
        self.defenses.pop(name)

    def add_condition(self, name):
        self.conditions[name] = True

    def remove_condition(self, name):
        self.conditions.pop(name)

    def add_money(self, name, value):
        self.money[name] = self.money[name] + value

    def roll_hit_die(self, die):
        self.hit_die['1d' + str(die)][0] -= 1
        return [random.randint(1, die), self.stats['con'][3]]

    def add_hp(self, points):
        self.hp += points
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def add_temp_hp(self, points):
        self.temp_hp = points

    def update_ac(self):
        self.ac = 10 + self.stats['dex'][3]  # TODO: include skills and armor

    def set_saving_throws(self):
        _class: Classes
        _class = self.classes[0]
        for key in _class.get_saving_throws():
            self.saving_throw[key] = [True, self.saving_throw[key][1]]


class Race:
    name = None
    subrace = None
    size = None
    stats = {'str': 0, 'dex': 0, 'con': 0, 'wis': 0, 'int': 0, 'cha': 0, }
    movement = {'Burrowing': [False, 0], 'Climbing': [False, 0], 'Flying': [False, 0], 'Swimming': [False, 0],
                'Walking': [False, 0]}
    senses = {'Blindsight': [False, 0], 'Darkvision': [False, 0], 'Tremorsense': [False, 0], 'Truesight': [False, 0]}
    proficiencies = {'Armor': [], 'Weapons': [], 'Tools': [], 'Languages': []}
    defenses = {}
    advantages = {}
    saving_throw_advantages = []
    special_action = []  # TODO: probably as a spell
    choice = {}  # stats: {'str': False, 'dex': False}..., skill: [['Acrobatics', False],...],
    # proficiencies: {'Armor': [['Light Armor', False],...],...},

    def stats_choice(self, stat):
        self.choice['stats'][stat] = True
        for key, value in self.choice['stats'].items():
            if value:
                self.stats[key] = 1
            else:
                self.stats[key] = 0


class Classes:
    level = 1
    hit_die = None
    skills_number = 0
    skill_proficiencies = {}
    proficiencies = {}
    saving_throws = []
    feature_attack = []
    feature_action = []
    feature_bonus = []
    feature_reaction = []
    feature_no_action = []
    attacks_number = 1
    special_ac = False
    sub_class = None

    def set_skill_proficiencies(self, skill):
        self.skill_proficiencies[skill] = True

    def get_skill_proficiencies(self):
        return self.skill_proficiencies

    def get_saving_throws(self):
        return self.saving_throws

    def get_proficiencies(self):
        return self.proficiencies


class Barbarian(Classes):
    def __init__(self, character_level):
        self.hit_die = '1d12'
        if character_level == 1:
            self.skills_number = 2
            self.skill_proficiencies = {'Animal Handling': False, 'Athletics': False, 'Intimidation': False,
                                        'Nature': False, 'Perception': False, 'Survival': False}
            self.saving_throws = ['str', 'con']
            self.proficiencies = {'Armor': ['light armor', 'medium armor', 'shields'],
                                  'Weapons': ['simple weapons', 'martial weapons'], 'Tools': [], 'Languages': []}

        else:
            self.proficiencies = {'Armor': ['shields'],
                                  'Weapons': ['simple weapons', 'martial weapons'], 'Tools': [], 'Languages': []}


class Spell:
    def __init__(self, name, level, damage):
        self.damage = damage
        self.level = level
        self.name = name
