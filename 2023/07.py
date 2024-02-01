from collections import Counter
from enum import Enum
from typing import NamedTuple

class Hand(NamedTuple):
    cards: str
    bid: int

def parse_input(lines: list[str]) -> list[Hand]:
    return [Hand(hand, int(bid.strip())) for line in lines for hand, bid in [line.split(" ")]]

def get_two_largest_char_amounts(string: str, remove_jokers = False) -> tuple[int, int]:
    string = string if not remove_jokers else string.replace("J", "")
    if len(set(string)) <= 1:
        return len(string), 0

    counter = Counter(string)
    most_common, second_most_common = counter.most_common(2)

    return most_common[1], second_most_common[1]

class HandRank(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

def calculate_hand_rank(cards: str) -> HandRank:
    max_amount, second_amount = get_two_largest_char_amounts(cards)
    match max_amount:
        case 5:
            return HandRank.FIVE_OF_A_KIND
        case 4:
            return HandRank.FOUR_OF_A_KIND
        case 3:
            return HandRank.FULL_HOUSE if second_amount == 2 else HandRank.THREE_OF_A_KIND
        case 2:
            return HandRank.TWO_PAIRS if second_amount == 2 else HandRank.ONE_PAIR
        case _:
            return HandRank.HIGH_CARD

def calculate_joker_hand_rank(cards: str) -> HandRank:
    max_amount, second_amount = get_two_largest_char_amounts(cards, True)
    jokers = cards.count("J")

    match max_amount:
        case 5:
            return HandRank.FIVE_OF_A_KIND
        case 4:
            return HandRank.FIVE_OF_A_KIND if jokers > 0 else HandRank.FOUR_OF_A_KIND
        case 3:
            if jokers == 2:
                return HandRank.FIVE_OF_A_KIND
            if jokers == 1:
                return HandRank.FOUR_OF_A_KIND

            return HandRank.FULL_HOUSE if second_amount == 2 else HandRank.THREE_OF_A_KIND
        case 2:
            if jokers == 3:
                return HandRank.FIVE_OF_A_KIND
            if jokers == 2:
                return HandRank.FOUR_OF_A_KIND

            if second_amount == 2:
                return HandRank.FULL_HOUSE if jokers == 1 else HandRank.TWO_PAIRS

            return HandRank.THREE_OF_A_KIND if jokers == 1 else HandRank.ONE_PAIR
        case 1:
            if jokers == 4:
                return HandRank.FIVE_OF_A_KIND
            if jokers == 3:
                return HandRank.FOUR_OF_A_KIND
            if jokers == 2:
                return HandRank.THREE_OF_A_KIND
            if jokers == 1:
                return HandRank.ONE_PAIR

            return HandRank.HIGH_CARD
        case _:
            return HandRank.FIVE_OF_A_KIND # No non-joker cards

CARD_STRENGTH_ORDER_NORMAL = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
CARD_STRENGTH_ORDER_JOKER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

def rankings_sort_condition(element: tuple[int, Hand], card_strength_order: list[str]):
    hand_rank, hand = element
    return [hand_rank, *[card_strength_order.index(card) for card in hand.cards]]

def silver_solution(lines: list[str]) -> int:
    hands = parse_input(lines)

    rankings = [(calculate_hand_rank(hand.cards).value, hand) for hand in hands]
    rankings.sort(key=lambda x: rankings_sort_condition(x, CARD_STRENGTH_ORDER_NORMAL))

    return sum((i+1) * hand.bid for i, (_, hand) in enumerate(rankings))

def gold_solution(lines: list[str]) -> int:
    hands = parse_input(lines)

    rankings = [(calculate_joker_hand_rank(hand.cards).value, hand) for hand in hands]
    rankings.sort(key=lambda x: rankings_sort_condition(x, CARD_STRENGTH_ORDER_JOKER))

    return sum((i+1) * hand.bid for i, (_, hand) in enumerate(rankings))
