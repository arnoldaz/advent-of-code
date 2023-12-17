from typing import NamedTuple

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class Card(NamedTuple):
    id: int
    winning_numbers: list[int]
    card_numbers: list[int]

cards: list[Card] = []
for line in lines:
    id_string, numbers = line.split(":")
    id = int(id_string.removeprefix("Card "))
    winning_number_string, card_number_string = numbers.split("|")
    winning_numbers = [int(x) for x in winning_number_string.split(" ") if x.strip() != ""]
    card_numbers = [int(x) for x in card_number_string.split(" ") if x.strip() != ""]
    cards.append(Card(id, winning_numbers, card_numbers))

def calculate_payout(cards: list[Card]) -> int:
    final_sum = 0

    for card in cards:
        matching_numbers = 0
        for card_number in card.card_numbers:
            if card_number in card.winning_numbers:
                matching_numbers += 1

        if matching_numbers > 0:
            final_sum += pow(2, matching_numbers - 1)

    return int(final_sum)

def calculate_cards(cards: list[Card]) -> int:
    card_amounts = [1 for _ in range(0, len(cards))]

    for i, card in enumerate(cards):
        matching_numbers = 0
        for card_number in card.card_numbers:
            if card_number in card.winning_numbers:
                matching_numbers += 1
        
        if matching_numbers > 0:
            for number in range(0, matching_numbers):
                if i + number + 1 <= len(card_amounts) - 1:
                    card_amounts[i + number + 1] += card_amounts[i]

    final_sum = 0
    for amount in card_amounts:
        final_sum += amount

    return final_sum

print(f"{calculate_payout(cards)=}")
print(f"{calculate_cards(cards)=}")



