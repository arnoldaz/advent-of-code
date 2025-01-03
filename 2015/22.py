# pylint: disable-all

from copy import copy
from dataclasses import dataclass
import sys
from typing import Callable, NamedTuple, Optional

from utils.list import remove_list_indexes

sys.setrecursionlimit(2 ** 30)

@dataclass
class Effect:
    id: int
    duration: int
    bonus_armor: int
    damage: int
    regen: int

class Spell(NamedTuple):
    name: str
    cost: int
    damage: int
    heal: int
    is_effect: bool
    get_effect: Callable[[], Effect]

class Player(NamedTuple):
    hp: int
    mana: int
    active_effects: list[Effect]

class Boss(NamedTuple):
    hp: int
    damage: int


def get_all_spells():
    return [
        Spell("Magic Missile",  53, 4, 0, False, lambda: Effect(0, 0, 0, 0,   0)),
        Spell("Drain",          73, 2, 2, False, lambda: Effect(0, 0, 0, 0,   0)),
        Spell("Shield",        113, 0, 0,  True, lambda: Effect(1, 6, 7, 0,   0)),
        Spell("Poison",        173, 0, 0,  True, lambda: Effect(2, 6, 0, 3,   0)),
        Spell("Recharge",      229, 0, 0,  True, lambda: Effect(3, 5, 0, 0, 101)),
    ]

# print = lambda *x: ()

def simulate_turn(spell: Spell, player: Player, boss: Boss) -> tuple[Player, Boss, bool]:
    player_hp = player.hp
    player_mana = player.mana
    player_armor = 0
    boss_hp = boss.hp
    active_effects: list[Effect] = []
    for effect in player.active_effects:
        active_effects.append(copy(effect))

    # uncomment for gold
    # player_hp -= 1

    # Effect procs
    expired_effect_ids: list[int] = []
    for i, effect in enumerate(active_effects):
        if effect.duration > 0:
            # print("effect proc", effect)
            boss_hp -= effect.damage
            player_armor += effect.bonus_armor
            player_mana += effect.regen

        effect.duration -= 1
        if effect.duration <= 0:
            # print("effect over", effect)
            expired_effect_ids.append(i)

    remove_list_indexes(active_effects, expired_effect_ids)


    # if boss_hp <= 0:
    #     return Player(player_hp, player_mana, active_effects), Boss(boss_hp, boss.damage), True

    # Check if current effect is not duplicated
    if spell.is_effect:
        new_effect = spell.get_effect()
        if any(effect.id == new_effect.id for effect in active_effects):
            return Player(player.hp, player.mana, player.active_effects), Boss(boss.hp, boss.damage), False

    if player_mana < spell.cost:
        return Player(player.hp, player.mana, player.active_effects), Boss(boss.hp, boss.damage), False

    # print(f"before player turn {player_hp=}, {player_mana=}, {boss_hp=}")
    # Player turn
    player_mana -= spell.cost
    boss_hp -= spell.damage
    player_hp += spell.heal
    # print(f"after player turn {player_hp=}, {player_mana=}, {boss_hp=}")

    # if boss_hp <= 0:
    #     return Player(player_hp, player_mana, active_effects), Boss(boss_hp, boss.damage), True

    if spell.is_effect:
        new_effect = spell.get_effect()
        if not any(effect.id == new_effect.id for effect in active_effects):
            active_effects.append(new_effect)

    player_armor = 0

    # Effect procs
    expired_effect_ids: list[int] = []
    for i, effect in enumerate(active_effects):
        if effect.duration > 0:
            # print("effect proc", effect)
            boss_hp -= effect.damage
            player_armor += effect.bonus_armor
            player_mana += effect.regen

        effect.duration -= 1
        if effect.duration <= 0:
            # print("effect over", effect)
            expired_effect_ids.append(i)

    remove_list_indexes(active_effects, expired_effect_ids)
    
    # Boss turn
    # print(f"before boss turn {player_hp=}, {player_mana=}, {boss_hp=}")
    player_hp -= max(1, boss.damage - player_armor)
    # print(f"after boss turn {player_hp=}, {player_mana=}, {boss_hp=}")

    return Player(player_hp, player_mana, active_effects), Boss(boss_hp, boss.damage), True

super_min = sys.maxsize

def aaaa(player: Player, boss: Boss, mana_spent: int, depth: int, spell_order: list[str]) -> int:
    # print("    " * depth, "==== START ", player, boss, mana_spent)
    global super_min
    if mana_spent > super_min:
        return sys.maxsize

    if boss.hp <= 0:
        # global super_min
        # if mana_spent < 1500:
        #     print(player, boss, mana_spent, depth, spell_order)
        if mana_spent < super_min:
            super_min = mana_spent
        # print("    " * depth, "victory")
        return mana_spent
    if player.hp <= 0:
        # print("    " * depth, "defeat")
        return sys.maxsize

    min_value = sys.maxsize
    for spell in get_all_spells():
        # print("    " * depth, "considering", spell.name)
        # if mana_spent + spell.cost > super_min:
        #     continue

        updated_player, updated_boss, is_valid_move = simulate_turn(spell, player, boss)
        if not is_valid_move:
            continue

        # print("    " * depth, spell.name, updated_player, updated_boss, mana_spent + spell.cost)

        value = aaaa(updated_player, updated_boss, mana_spent + spell.cost, depth + 1, spell_order + [spell.name])
        min_value = min(min_value, value)

    # print(super_min)
    return min_value

def parse_input(lines: list[str]) -> Boss:
    return Boss(*[int(line.split(": ")[1]) for line in lines])

def silver_solution(lines: list[str]) -> int:
    boss = parse_input(lines)
    player = Player(50, 500, [])

    # print(boss)

    # player = Player(10, 250, [])
    # boss = Boss(14, 8)
    return aaaa(player, boss, 0, 0, [])
    

    # return [
    #     Spell("Magic Missile",  53, 4, 0, False, lambda: Effect(0, 0, 0, 0,   0)),
    #     Spell("Drain",          73, 2, 2, False, lambda: Effect(0, 0, 0, 0,   0)),
    #     Spell("Shield",        113, 0, 0,  True, lambda: Effect(1, 6, 7, 0,   0)),
    #     Spell("Poison",        173, 0, 0,  True, lambda: Effect(2, 6, 0, 3,   0)),
    #     Spell("Recharge",      229, 0, 0,  True, lambda: Effect(3, 5, 0, 0, 101)),
    # ]

    a = get_all_spells()
    spells = [a[3], a[4], a[2], a[3], a[4], a[0], a[3], a[0], a[0]]

    print("    ", player)
    print("    ", boss)
    print()
    b = 0
    for spell in spells:
        print("    ", spell.name)
        player, boss, test = simulate_turn(spell, player, boss)
        b+=spell.cost
        print("    ", player)
        print("    ", boss)
        print("    ", test)
        print()
    print(b)

    return -123

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
