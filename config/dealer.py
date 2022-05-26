cards = []

for i in range(0, 64, 8):
    cards.append(i)
    cards.append(i+1)
    cards.append(i+2)
    cards.append(i+3)

    cards.append(i+4)

    cards.append(i+5)

    cards.append(i+6)

    cards.append(i+7)

for j in range(0, 64):
    if j not in cards:
        print(j)

print('duplicates?:', len(cards) != len(set(cards)))

cards_gold = list(range(64))
for k in range(len(cards_gold)):
    if cards_gold[k] != cards[k]:
        print(f"gold: {cards_gold[k]}, cards: {cards[k]}")
