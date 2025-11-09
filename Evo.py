import random
import numpy as np
import pickle
import os
from collections import defaultdict

CONST_Deck = [11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2]
Cards = [11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2]
Hand = []
Dealer = []

Chips = 500
Bet = 10
Resetting = False

#Evo Var
def start():
    return [0.0, 0.0]

Q = defaultdict(start)
Learn = 0.1
Future = 0.7
Epsilon = 0.1
Action = 0
Reward = 0
State = ()
Next = ()

Trials = 1000000000
Save_Interval = 500000
#Load / Save Q

if os.path.exists("q_table.pkl"):
    with open("q_table.pkl", "rb") as f:
        Q = defaultdict(start, pickle.load(f))
else:
    Q = defaultdict(start)
print(Q)

#Evo Funcs
def get_state():
    global Hand, Dealer
    ace = 0
    while 11 in Hand:
        if hand_value(Hand) <= 21:
            ace = 1
            break
    return (hand_value(Hand), Dealer[1], ace)

def get_action(state):
    global Epsilon, Q
    if np.random.rand() < Epsilon:
        return np.random.choice([0, 1])
    return np.argmax(Q[state])

def update(state, q, next, action, learn, future, reward):
    if next[0] > 21:
        best = 0.01
    else:
        best = max(q[next])
    target_value = reward + future * best
    target_error = target_value - q[state][action]
    q[state][action] += learn * target_error

#Blackjack Funcs
def reset():
    global Cards, Dealer, Hand
    Hand.clear()
    Dealer.clear()
    Cards = CONST_Deck.copy()
    Resetting = False

def hand_value(hand):
    value = sum(hand)
    aces = hand.count(11)
    while value > 21 and aces:
        hand[hand.index(11)] = 1
        value -= 10
        aces -= 1
    return value

def deal():
    global Cards, Dealer, Hand, Resetting, Bet
    if len(Cards) <= 15:
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

def bust(int):
    global Chips, Resetting, State, Q, Action, Learn, Future, Next, Reward
    Reward = 0
    if int == 0:
        Chips -= Bet
        Reward = -abs((hand_value(Hand) - hand_value(Dealer)) / 21)
    elif int == 1:
        Chips += Bet
        Reward = abs((hand_value(Hand) - hand_value(Dealer)) / 21)
    Next = get_state()
    update(State, Q, Next, Action, Learn, Future, Reward)
    Resetting = True

def hit(list):
    index = random.randrange(len(Cards))
    list.append(Cards.pop(index))
    while sum(list) > 21 and 11 in list:
        list[list.index(11)] = 1
    if list == Hand and hand_value(Hand) <= 21:
        Reward = 0.5
        Next = get_state()
        update(State, Q, Next, Action, Learn, Future, Reward)
    if hand_value(list) > 21:
        Resetting = True

        if list == Hand:
            bust(0)
        else:
            bust(1)

def stand():
    global Resetting, Dealer, Hand, State, Q, Action, Learn, Future, Next, Reward
    if not Resetting:
        while hand_value(Dealer) < 17:
            if len(Dealer) <= 1:
                return
            if Dealer[0] == 11 and sum(Dealer) > 21:
                Dealer[0] = 1
            Dealer = sorted(Dealer, reverse=True)
            hit(Dealer)
        if hand_value(Hand) > hand_value(Dealer):
            bust(1)
        elif hand_value(Hand) < hand_value(Dealer):
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


test = False
summary = 100000

for i in range(Trials):
    if i == Save_Interval and i > 0:
        with open("q_table.pkl", "wb") as f:
            pickle.dump(Q, f)
        print(f"Q-table auto-saved at episode {i}")
        Save_Interval += 500000
    if i == summary:
        print(Q)
        summary += 100000
    deal()
    Resetting = False
    while not Resetting:
        if hand_value(Hand) <= 21 and hand_value(Dealer) <= 21:
            State = get_state()
        Action = get_action(State)
        if Action == 0:
            hit(Hand)
        elif Action == 1:
            stand()

print("Saving Q-table...")
with open("q_table.pkl", "wb") as f:
    pickle.dump(Q, f)
    print("Q-table saved!")