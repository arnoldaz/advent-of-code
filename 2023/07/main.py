from typing import NamedTuple

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class Hand(NamedTuple):
    cards: str
    bid: int

hands: list[Hand] = []
for line in lines:
    hand, bid = line.split(" ")
    hands.append(Hand(hand, int(bid.strip())))

def two_largest(list):
    largest = -1
    largest_index = -1
    second_largest = -1

    for i, item in enumerate(list):
        if item > largest:
            second_largest = largest
            largest = item
            largest_index = i
        elif largest >= item > second_largest and largest_index != i:
            second_largest = item

    return largest, second_largest

def get_two_largest_char_amounts(string: str) -> tuple[int, int]:
    char_count = {}
    
    for char in string:
        char_count[char] = char_count.get(char, 0) + 1

    values = char_count.values()
    return two_largest(values)

def get_two_largest_char_amounts_exclude_joker(string: str) -> tuple[int, int]:
    char_count = {}
    
    for char in string:
        char_count[char] = char_count.get(char, 0) + 1

    # remove jokers
    char_count["J"] = 0

    values = char_count.values()
    return two_largest(values)

# Hand ranks
# 1. High card
# 2. One pair
# 3. Two pairs
# 4. Three of a kind
# 5. Full house
# 6. Four of a kind
# 7. Five of a kind

def calculate_hand_rank(cards: str) -> int:
    # five of a kind
    if len(set(cards)) == 1:
        return 7

    max_amount, second_amount = get_two_largest_char_amounts(cards)
    match max_amount:
        case 4:
            return 6
        case 3:
            # check for full house also
            return 5 if second_amount == 2 else 4
        case 2:
            # check for 2 pairs also
            return 3 if second_amount == 2 else 2
        case 1:
            return 1

    # impossible
    return 0

def calculate_joker_hand_rank(cards: str) -> int:
    # five of a kind
    if len(set(cards)) == 1:
        return 7

    max_amount, second_amount = get_two_largest_char_amounts_exclude_joker(cards)
    jokers = cards.count("J")

    match max_amount:
        case 4:
            return 7 if jokers > 0 else 6
        case 3:
            if jokers == 1:
                return 6
            elif jokers == 2:
                return 7
            else:
                return 5 if second_amount == 2 else 4
        case 2:
            if jokers == 3:
                return 7
            elif jokers == 2:
                return 6
            else:
                if second_amount == 2:
                    if jokers == 1:
                        return 5
                    else:
                        return 3
                else:
                    if jokers == 1:
                        return 4
                    else:
                        return 2
        case 1:
            if jokers == 4:
                return 7
            elif jokers == 3:
                return 6
            elif jokers == 2:
                return 4
            elif jokers == 1:
                return 2
            else:
                return 1

    # impossible
    return 0

CARD_STRENGTH_ORDER = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARD_STRENGTH_ORDER_JOKER = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

def rankings_sort_condition(element: tuple[int, Hand]):
    hand_rank = element[0]
    cards = element[1].cards

    card_order_length = len(CARD_STRENGTH_ORDER)

    high_card_strength = \
        (card_order_length - CARD_STRENGTH_ORDER.index(cards[0])) * 100000000 + \
        (card_order_length - CARD_STRENGTH_ORDER.index(cards[1])) * 1000000 + \
        (card_order_length - CARD_STRENGTH_ORDER.index(cards[2])) * 10000 + \
        (card_order_length - CARD_STRENGTH_ORDER.index(cards[3])) * 100 + \
        (card_order_length - CARD_STRENGTH_ORDER.index(cards[4]))

    return (hand_rank, high_card_strength)

def rankings_sort_condition_joker(element: tuple[int, Hand]):
    hand_rank = element[0]
    cards = element[1].cards

    card_order_length = len(CARD_STRENGTH_ORDER_JOKER)

    high_card_strength = \
        (card_order_length - CARD_STRENGTH_ORDER_JOKER.index(cards[0])) * 100000000 + \
        (card_order_length - CARD_STRENGTH_ORDER_JOKER.index(cards[1])) * 1000000 + \
        (card_order_length - CARD_STRENGTH_ORDER_JOKER.index(cards[2])) * 10000 + \
        (card_order_length - CARD_STRENGTH_ORDER_JOKER.index(cards[3])) * 100 + \
        (card_order_length - CARD_STRENGTH_ORDER_JOKER.index(cards[4]))

    return (hand_rank, high_card_strength)

def calculate_winnings(hands: list[Hand]) -> int:
    final_winnings = 0

    rankings: list[tuple[int, Hand]] = []

    for hand in hands:
        hand_rank = calculate_hand_rank(hand.cards)
        rankings.append((hand_rank, hand))

    rankings.sort(key=rankings_sort_condition)

    for i, ranking in enumerate(rankings):
        bid = ranking[1].bid
        final_winnings += (i+1) * bid

    return final_winnings

def calculate_joker_winnings(hands: list[Hand]) -> int:
    final_winnings = 0

    rankings: list[tuple[int, Hand]] = []

    for hand in hands:
        hand_rank = calculate_joker_hand_rank(hand.cards)
        rankings.append((hand_rank, hand))

    rankings.sort(key=rankings_sort_condition_joker)

    for i, ranking in enumerate(rankings):
        bid = ranking[1].bid
        final_winnings += (i+1) * bid

    return final_winnings

print(f"{calculate_winnings(hands)=}")
print(f"{calculate_joker_winnings(hands)=}")

