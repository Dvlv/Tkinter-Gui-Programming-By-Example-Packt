import os
import random
import tkinter as tk

assets_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'assets/'))


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.img = tk.PhotoImage(file=assets_folder + '/' + self.suit + self.value + ".png")

    def __repr__(self):
        return " of ".join((self.value, self.suit))

    def get_file(self):
        return self.img

    @classmethod
    def get_back_file(cls):
        cls.back = tk.PhotoImage(file=assets_folder + "/back.png")

        return cls.back


class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] for v in
                      ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value


class Player:
    def __init__(self):
        self.money = 50
        self.hand = Hand()

    def add_winnings(self, winnings):
        self.money += winnings

    def place_bet(self, amount):
        self.money -= amount

    def can_place_bet(self, amount):
        return self.money >= amount

    def receive_card(self, card):
        self.hand.add_card(card)

    def empty_hand(self):
        self.hand.cards = []

    @property
    def score(self):
        return self.hand.get_value()

    @property
    def is_over(self):
        return self.hand.get_value() > 21

    @property
    def has_blackjack(self):
        return self.hand.get_value() == 21

    @property
    def cards(self):
        return [card for card in self.hand.cards]


class Dealer(Player):
    def __init__(self):
        super().__init__()
