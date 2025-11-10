import random

CONST_Deck = [11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2]
Cards = [11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2]
Hand = []
Dealer = []

Chips = 500
Bet = 50
Resetting = False

def reset():
    global Cards, Dealer, Hand
    Hand.clear()
    Dealer.clear()
    Cards = CONST_Deck.copy()
    Resetting = False

def deal():
    global Cards, Dealer, Hand, Resetting, Bet
    if len(Cards) <= 10:
        Cards = CONST_Deck.copy()
    Deal = []
    Hand.clear()
    Dealer.clear()
    for i in range(4):
        index = random.randrange(len(Cards))
        Deal.append(Cards.pop(index))
    Hand.append(Deal[0])
    Hand.append(Deal[1])
    Dealer.append(Deal[2])
    Dealer.append(Deal[3])
    Resetting = False
    print("Chips =", Chips)
    Bet = bet()

def bust(int):
    global Chips, Resetting
    if int == 0:
        Chips -= Bet
    elif int == 1:
        Chips += Bet
    deal()

def hit(list):
    global Hand
    index = random.randrange(len(Cards))
    list.append(Cards.pop(index))
    while sum(list) > 21 and 11 in list:
        list[list.index(11)] = 1
    if sum(Hand) > 21:
        print(Hand)
        bust(0)

def stand():
    global Resetting, Dealer, Hand
    if not Resetting:
        while sum(Dealer) < 17:
            if len(Dealer) <= 1:
                return
            if Dealer[0] == 11 and sum(Dealer) > 21:
                Dealer[0] = 1
            Dealer = sorted(Dealer, reverse=True)
            print(Hand, Dealer, sum(Hand), sum(Dealer))
            hit(Dealer)
        print(Hand, Dealer, sum(Hand), sum(Dealer))
        if sum(Hand) > sum(Dealer) or sum(Dealer) > 21:
            bust(1)
        elif sum(Hand) < sum(Dealer):
            bust(0)
        else:
            bust(2)
        Resetting = True

def bet():
    try:
        Bet_Input = input("Bet: ")
    except ValueError:
        Bet_Input = input("Bet: ")
    Bet = max(10, round(int(Bet_Input) / 5) * 5)
    print("Bet =", Bet)
    return Bet


while True:
    action = " "
    deal()
    print("\n", Hand, Dealer[1])

    Resetting = False
    while not Resetting:
        action = input()
        if action == "h":
            hit(Hand)
            if len(Dealer) <= 1:
                break
            Hand = sorted(Hand, reverse=True)
            print(Hand, Dealer[1])
        elif action == "r":
            reset()
            action = " "
            break
        elif action == "s":
            stand()
            action = " "
            Resetting = True
            break
        action = " "
