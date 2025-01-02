import sys
from typing import NamedTuple
from itertools import combinations

class Entity(NamedTuple):
    hp: int
    damage: int
    armor: int

class Item(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int

def parse_input(lines: list[str]) -> Entity:
    return Entity(*[int(line.split(": ")[1]) for line in lines])

def get_all_items() -> tuple[list[Item], list[Item], list[Item]]:
    return [
        Item("Dagger",       8, 4, 0),
        Item("Shortsword",  10, 5, 0),
        Item("Warhammer",   25, 6, 0),
        Item("Longsword",   40, 7, 0),
        Item("Greataxe",    74, 8, 0),
    ], [
        Item("Leather",     13, 0, 1),
        Item("Chainmail",   31, 0, 2),
        Item("Splintmail",  53, 0, 3),
        Item("Bandedmail",  75, 0, 4),
        Item("Platemail",  102, 0, 5),
    ], [
        Item("Damage +1",   25, 1, 0),
        Item("Damage +2",   50, 2, 0),
        Item("Damage +3",  100, 3, 0),
        Item("Defense +1",  20, 0, 1),
        Item("Defense +2",  40, 0, 2),
        Item("Defense +3",  80, 0, 3),
    ]

def simulate_fight(player: Entity, boss: Entity) -> bool:
    player_hp, boss_hp = player.hp, boss.hp
    while True:
        boss_hp -= max(1, player.damage - boss.armor)
        if boss_hp <= 0:
            return True

        player_hp -= max(1, boss.damage - player.armor)
        if player_hp <= 0:
            return False

def silver_solution(lines: list[str]) -> int:
    boss = parse_input(lines)
    weapons, armors, rings = get_all_items()
    empty_item = Item("Empty", 0, 0, 0)
    player_hp = 100

    min_gold_spent = sys.maxsize
    for weapon in weapons:
        for armor in [empty_item] + armors:
            for ring in [(empty_item,)] + [(r,) for r in rings] + list(combinations(rings, 2)):
                total_damage = weapon.damage + armor.damage + sum(r.damage for r in ring)
                total_armor = weapon.armor + armor.armor + sum(r.armor for r in ring)
                player = Entity(player_hp, total_damage, total_armor)
                if simulate_fight(player, boss):
                    total_cost = weapon.cost + armor.cost + sum(r.cost for r in ring)
                    min_gold_spent = min(min_gold_spent, total_cost)

    return min_gold_spent

def gold_solution(lines: list[str]) -> int:
    boss = parse_input(lines)
    weapons, armors, rings = get_all_items()
    empty_item = Item("Empty", 0, 0, 0)
    player_hp = 100

    max_gold_spent = 0
    for weapon in weapons:
        for armor in [empty_item] + armors:
            for ring in [(empty_item,)] + [(r,) for r in rings] + list(combinations(rings, 2)):
                total_damage = weapon.damage + armor.damage + sum(r.damage for r in ring)
                total_armor = weapon.armor + armor.armor + sum(r.armor for r in ring)
                player = Entity(player_hp, total_damage, total_armor)
                if not simulate_fight(player, boss):
                    total_cost = weapon.cost + armor.cost + sum(r.cost for r in ring)
                    max_gold_spent = max(max_gold_spent, total_cost)

    return max_gold_spent
