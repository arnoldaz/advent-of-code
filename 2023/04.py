from typing import NamedTuple

class Card(NamedTuple):
    id: int
    winning_numbers: list[int]
    card_numbers: list[int]

def parse_input(lines: list[str]) -> list[Card]:
    cards: list[Card] = []
    for line in lines:
        card_id_string, numbers = line.split(":")
        card_id = int(card_id_string.removeprefix("Card "))
        winning_numbers, card_numbers = [[int(x) for x in number.split(" ") if x.strip() != ""] for number in numbers.split("|")]
        cards.append(Card(card_id, winning_numbers, card_numbers))

    return cards

def silver_solution(lines: list[str]) -> int:
    cards = parse_input(lines)

    final_sum: float = 0
    for card in cards:
        matching_numbers = sum(1 for card_number in card.card_numbers if card_number in card.winning_numbers)
        if matching_numbers > 0:
            final_sum += pow(2, matching_numbers - 1)

    return int(final_sum)

def gold_solution(lines: list[str]) -> int:
    cards = parse_input(lines)
    card_amounts = [1 for _ in range(0, len(cards))]

    for i, card in enumerate(cards):
        matching_numbers = sum(1 for card_number in card.card_numbers if card_number in card.winning_numbers)
        if matching_numbers == 0:
            continue

        for number in range(min(matching_numbers, len(card_amounts) - i - 1)):
            card_amounts[i + number + 1] += card_amounts[i]

    return sum(card_amounts)
