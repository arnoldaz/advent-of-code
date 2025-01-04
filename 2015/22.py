import sys
from dataclasses import dataclass
from typing import Callable, NamedTuple

@dataclass
class Effect:
    id: int
    duration: int
    bonus_armor: int
    damage: int
    regen: int

    def copy(self) -> "Effect":
        return Effect(self.id, self.duration, self.bonus_armor, self.damage, self.regen)

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

def parse_input(lines: list[str]) -> Boss:
    return Boss(*[int(line.split(": ")[1]) for line in lines])

def get_all_spells():
    return [
        Spell("Magic Missile",  53, 4, 0, False, lambda: Effect(0, 0, 0, 0,   0)),
        Spell("Drain",          73, 2, 2, False, lambda: Effect(0, 0, 0, 0,   0)),
        Spell("Shield",        113, 0, 0,  True, lambda: Effect(1, 6, 7, 0,   0)),
        Spell("Poison",        173, 0, 0,  True, lambda: Effect(2, 6, 0, 3,   0)),
        Spell("Recharge",      229, 0, 0,  True, lambda: Effect(3, 5, 0, 0, 101)),
    ]

def simulate_turn(spell: Spell, player: Player, boss: Boss, is_hard_mode: bool) -> tuple[Player, Boss, bool]:
    player_hp = player.hp
    player_mana = player.mana
    boss_hp = boss.hp
    active_effects = [effect.copy() for effect in player.active_effects]

    # Hard mode health drain
    if is_hard_mode:
        player_hp -= 1

    # Effect procs
    player_armor = 0
    for effect in active_effects:
        if effect.duration > 0:
            boss_hp -= effect.damage
            player_armor += effect.bonus_armor
            player_mana += effect.regen

        effect.duration -= 1

    # Check if current effect is not duplicated
    if spell.is_effect:
        new_effect = spell.get_effect()
        if any(effect.id == new_effect.id for effect in active_effects if effect.duration > 0):
            return player, boss, False

    # Check if player can cast the spell
    if player_mana < spell.cost:
        return player, boss, False

    # Player turn
    player_mana -= spell.cost
    boss_hp -= spell.damage
    player_hp += spell.heal

    if spell.is_effect:
        new_effect = spell.get_effect()
        active_effects.append(new_effect)

    # Effect procs
    player_armor = 0
    for effect in active_effects:
        if effect.duration > 0:
            boss_hp -= effect.damage
            player_armor += effect.bonus_armor
            player_mana += effect.regen

        effect.duration -= 1

    # Boss turn
    player_hp -= max(1, boss.damage - player_armor)

    return (
        Player(player_hp, player_mana, [effect for effect in active_effects if effect.duration > 0]),
        Boss(boss_hp, boss.damage),
        True
    )

def get_min_mana_spent_win(player: Player, boss: Boss, is_hard_mode: bool) -> int:
    all_spells = get_all_spells()
    global_spent_minimum = sys.maxsize
    def find_spell_order_recursive(player: Player, boss: Boss, mana_spent: int):
        nonlocal global_spent_minimum, all_spells
        if mana_spent > global_spent_minimum:
            return sys.maxsize

        if boss.hp <= 0:
            global_spent_minimum = min(global_spent_minimum, mana_spent)
            return mana_spent

        if player.hp <= 0:
            return sys.maxsize

        min_value = sys.maxsize
        for spell in all_spells:
            updated_player, updated_boss, is_valid_move = simulate_turn(spell, player, boss, is_hard_mode)
            if not is_valid_move:
                continue

            value = find_spell_order_recursive(updated_player, updated_boss, mana_spent + spell.cost)
            min_value = min(min_value, value)

        return min_value

    return find_spell_order_recursive(player, boss, 0)

def silver_solution(lines: list[str]) -> int:
    boss = parse_input(lines)
    player = Player(50, 500, [])
    return get_min_mana_spent_win(player, boss, False)

def gold_solution(lines: list[str]) -> int:
    boss = parse_input(lines)
    player = Player(50, 500, [])
    return get_min_mana_spent_win(player, boss, True)
