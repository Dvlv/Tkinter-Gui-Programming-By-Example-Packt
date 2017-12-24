import tkinter as tk
import os
import random

assets_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets/'))


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
    def __init__(self, name):
        self.name = name
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
        super().__init__("Dealer")


class GameScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry("800x640")
        self.resizable(False, False)

        self.CARD_ORIGINAL_POSITION = 100
        self.CARD_WIDTH_OFFSET = 100

        self.PLAYER_CARD_HEIGHT = 300
        self.DEALER_CARD_HEIGHT = 100

        self.PLAYER_SCORE_TEXT_COORDS = (340, 450)
        self.PLAYER_MONEY_COORDS = (490, 450)
        self.POT_MONEY_COORDS = (500, 100)
        self.WINNER_TEXT_COORDS = (400, 250)

        self.game_state = GameState("Player")

        self.game_screen = tk.Canvas(self, bg="white", width=800, height=500)

        self.bottom_frame = tk.Frame(self, width=800, height=140, bg="red")
        self.bottom_frame.pack_propagate(0)

        self.hit_button = tk.Button(self.bottom_frame, text="Hit", width=25, command=self.hit)
        self.stick_button = tk.Button(self.bottom_frame, text="Stick", width=25, command=self.stick)

        self.next_round_button = tk.Button(self.bottom_frame, text="Next Round", width=25, command=self.next_round)
        self.quit_button = tk.Button(self.bottom_frame, text="Quit", width=25, command=self.destroy)

        self.hit_button.pack(side=tk.LEFT, padx=(100, 200))
        self.stick_button.pack(side=tk.LEFT)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)

        self.display_table()

    def display_table(self, hide_dealer=True, table_state=None):
        if not table_state:
            table_state = self.game_state.get_table_state()

        player_card_images = [card.get_file() for card in table_state['player_cards']]
        dealer_card_images = [card.get_file() for card in table_state['dealer_cards']]
        if hide_dealer and not table_state['blackjack']:
            dealer_card_images[0] = Card.get_back_file()

        self.game_screen.delete("all")
        self.tabletop_image = tk.PhotoImage(file=assets_folder + "/tabletop.png")

        self.game_screen.create_image((400, 250), image=self.tabletop_image)

        for card_number, card_image in enumerate(player_card_images):
            self.game_screen.create_image(
                (self.CARD_ORIGINAL_POSITION + self.CARD_WIDTH_OFFSET * card_number, self.PLAYER_CARD_HEIGHT),
                image=card_image
            )

        for card_number, card_image in enumerate(dealer_card_images):
            self.game_screen.create_image(
                (self.CARD_ORIGINAL_POSITION + self.CARD_WIDTH_OFFSET * card_number, self.DEALER_CARD_HEIGHT),
                image=card_image
            )

        self.game_screen.create_text(self.PLAYER_SCORE_TEXT_COORDS, text=self.game_state.player_score_as_text(),
                                     font=(None, 20))
        self.game_screen.create_text(self.PLAYER_MONEY_COORDS, text=self.game_state.player_money_as_text(),
                                     font=(None, 20))
        self.game_screen.create_text(self.POT_MONEY_COORDS, text=self.game_state.pot_money_as_text(),
                                     font=(None, 20))

        if table_state['has_winner']:
            if table_state['has_winner'] == 'p':
                self.game_screen.create_text(self.WINNER_TEXT_COORDS, text="YOU WIN!", font=(None, 50))
            elif table_state['has_winner'] == 'dp':
                self.game_screen.create_text(self.WINNER_TEXT_COORDS, text="TIE!", font=(None, 50))
            else:
                self.game_screen.create_text(self.WINNER_TEXT_COORDS, text="DEALER WINS!", font=(None, 50))

            self.show_next_round_options()

    def show_next_round_options(self):
        self.hit_button.pack_forget()
        self.stick_button.pack_forget()

        self.next_round_button.pack(side=tk.LEFT, padx=(100, 200))
        self.quit_button.pack(side=tk.LEFT)

    def show_gameplay_buttons(self):
        self.next_round_button.pack_forget()
        self.quit_button.pack_forget()

        self.hit_button.pack(side=tk.LEFT, padx=(100, 200))
        self.stick_button.pack(side=tk.LEFT)

    def next_round(self):
        self.show_gameplay_buttons()
        self.game_state.next_round()
        self.display_table()

    def hit(self):
        self.game_state.hit()
        self.display_table()

    def stick(self):
        table_state = self.game_state.calculate_final_state()
        self.display_table(False, table_state)


class GameState:
    def __init__(self, player_name):
        self.BASE_BET = 5
        self.minimum_bet = self.BASE_BET
        self.current_round = 1
        self.pot = 0

        self.deck = Deck()
        self.deck.shuffle()

        self.player = Player(player_name)
        self.dealer = Dealer()

        self.begin_round()

    def begin_round(self):
        self.has_winner = ''

        for i in range(2):
            self.player.receive_card(self.deck.deal())
            self.dealer.receive_card(self.deck.deal())

        if self.player.can_place_bet(self.minimum_bet):
            self.player.place_bet(self.minimum_bet)
            self.dealer.place_bet(self.minimum_bet)
            self.add_bet(self.minimum_bet * 2)
        else:
            # player is out - game over
            pass

    def next_round(self):
        self.assign_winnings(self.has_winner)

        self.current_round += 1
        self.minimum_bet = self.BASE_BET * self.current_round
        print('mb', self.minimum_bet)

        self.player.empty_hand()
        self.dealer.empty_hand()

        self.begin_round()

    def add_bet(self, amount):
        print('adding', amount, 'to pot of', self.pot)
        self.pot += amount

    def assign_winnings(self, winner):
        if winner == 'p':
            self.player.add_winnings(self.pot)
            print('player wins, reset pot')
            self.pot = 0
        elif winner == 'd':
            self.dealer.add_winnings(self.pot)
            print('dealer wins, empty pot')
            self.pot = 0

    def hit(self):
        self.player.receive_card(self.deck.deal())
        if self.player.has_blackjack:
            self.has_winner = 'p'
        elif self.player.is_over:
            self.has_winner = 'd'

        return self.has_winner

    def get_table_state(self):
        blackjack = False
        winner = self.has_winner
        if not winner:
            winner = self.someone_has_blackjack()
            if winner:
                blackjack = True
        table_state = {
            'player_cards': self.player.cards,
            'dealer_cards': self.dealer.cards,
            'has_winner': winner,
            'blackjack': blackjack,
            'player_money': self.player.money
        }

        return table_state

    def calculate_final_state(self):
        player_hand_value = self.player.score
        dealer_hand_value = self.dealer.score

        if player_hand_value == dealer_hand_value:
            winner = 'dp'
        elif player_hand_value > dealer_hand_value:
            winner = 'p'
        else:
            winner = 'd'

        self.has_winner = winner

        table_state = {
            'player_cards': self.player.cards,
            'dealer_cards': self.dealer.cards,
            'has_winner': winner,
            'player_money': self.player.money
        }

        return table_state

    def player_score_as_text(self):
        return "Score: " + str(self.player.score)

    def player_money_as_text(self):
        return "Money: £" + str(self.player.money)

    def pot_money_as_text(self):
        return "Pot: £" + str(self.pot)

    def someone_has_blackjack(self):
        player = False
        dealer = False
        if self.player.has_blackjack:
            player = True
        if self.dealer.has_blackjack:
            dealer = True

        if player and dealer:
            return 'dp'
        elif player:
            return 'p'
        elif dealer:
            return 'd'

        return False


if __name__ == "__main__":
    gs = GameScreen()
    gs.mainloop()
