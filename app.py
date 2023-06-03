import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        value = self.value
        if value == 11:
            value = "J"
        elif value == 12:
            value = "Q"
        elif value == 13:
            value = "K"
        elif value == 14:
            value = "A"
        return f"{value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] for v in range(2, 15)]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.table_cards = []
        self.secret_cards = []

    def initial_draw(self, deck):
        for i in range(6):
            self.hand.append(deck.draw())

    def draw(self, deck):
        while len(self.hand) < 3 and deck.cards:
            self.hand.append(deck.draw())

    def choose_table_cards(self):
        print(f"{self.name}, your cards: {self.hand}")
        for i in range(3):
            while True:
                try:
                    card_value = input("Which card do you want to put on the table? (Enter value) ")
                    if card_value.isdigit():
                        card_value = int(card_value)
                    else:
                        card_value = card_value.upper()

                    if card_value == 'J':
                        card_value = 11
                    elif card_value == 'Q':
                        card_value = 12
                    elif card_value == 'K':
                        card_value = 13
                    elif card_value == 'A':
                        card_value = 14

                    card = next((card for card in self.hand if card.value == card_value), None)
                    if card is None:
                        print("You don't have this card! Try again.")
                        continue

                    self.hand.remove(card)
                    self.table_cards.append(card)
                    print(f"{self.name}, your cards: {self.hand}")
                    print(f"{self.name}, your table cards: {self.table_cards}")
                    break
                except ValueError:
                    print("Invalid input, try again.")
        print(f"{self.name}, your table cards: {self.table_cards}")

    def play_card(self, pile, deck):
        while True:
            print(f"{self.name}, your hand: {self.hand}")
            valid_cards = [card for card in self.hand
                           if not pile or card.value >= pile[-1].value or card.value == 2 or card.value == 3]

            if not valid_cards:  # Player cannot play any card
                print(f"{self.name} cannot play any card and collects the pile.")
                self.hand += pile
                pile.clear()
                return None  # Return None to indicate that the player could not play

            try:
                card_value = input("Which card do you want to play? (Enter value) ")
                if card_value.isdigit():
                    card_value = int(card_value)
                else:
                    card_value = card_value.upper()

                if card_value == 'J':
                    card_value = 11
                elif card_value == 'Q':
                    card_value = 12
                elif card_value == 'K':
                    card_value = 13
                elif card_value == 'A':
                    card_value = 14

                card = next((card for card in self.hand if card.value == card_value), None)
                if card is None or card not in valid_cards:
                    print("You can't play this card! Try again.")
                    continue

                self.hand.remove(card)
                if deck.cards:
                    self.hand.append(deck.draw())
                return card
            except ValueError:
                print("Invalid input, try again.")


class Game:
    def __init__(self, players):
        self.players = [Player(name) for name in players]
        self.deck = Deck()
        self.pile = []
        self.upper_limit = None  # Add this line

    def start(self):
        for player in self.players:
            player.initial_draw(self.deck)
            player.choose_table_cards()

        skip_next = False
        keep_turn = False
        while self.players:
            for player in self.players:
                if skip_next:
                    skip_next = False
                    continue
                while True:
                    if not player.hand and not player.table_cards and player.secret_cards:
                        player.hand.append(player.secret_cards.pop())
                    card = player.play_card(self.pile, self.deck)

                    if card is None:
                        print(f"{player.name} cannot play a card and picks up the pile.")
                        player.hand += self.pile
                        self.pile = []
                        continue

                    # Add this check
                    if self.upper_limit is not None and (card.value > self.upper_limit and (card.value != 3)):
                        print(f"You can't play this card! It is above the current limit of {self.upper_limit}.")
                        continue

                    self.pile.append(card)
                    print(f"{player.name} played {card}")

                    # Implement special rules
                    if card.value == 10:
                        self.pile = []
                        print("10 was played. The pile is cleared!")
                        keep_turn = True
                    elif card.value == 8:
                        skip_next = True
                        print("8 was played. Next player is skipped!")
                        self.upper_limit = None  # Reset the upper limit
                        break  # end the turn
                    elif card.value == 7:
                        print("7 was played. Next player must play a card of equal or lower rank!")
                        self.upper_limit = 7  # Set the upper limit to 7
                        break  # end the turn
                    elif card.value == 2:
                        self.pile = [card]
                        print("2 was played. Next player can play any card!")
                        self.upper_limit = None  # Reset the upper limit
                        break  # end the turn
                    elif card.value == 3:
                        if len(self.pile) >= 2:
                            self.pile[-1] = self.pile[-2]
                            print("3 was played. It copies the value of the previous card!")
                        else:
                            print("3 was played as the first card, so it keeps its own value!")
                        self.upper_limit = None  # Reset the upper limit
                        break  # end the turn
                    else:
                        self.upper_limit = None  # Reset the upper limit
                        break  # end the turn

                    if not player.hand and not player.table_cards and player.secret_cards:
                        player.hand.append(player.secret_cards.pop())

                    if not player.hand and not player.table_cards and not player.secret_cards:
                        print(f"{player.name} has no more cards! They are out of the game.")
                        self.players.remove(player)

                    if keep_turn:
                        keep_turn = False
                    else:
                        break

        print("The game is over!")



if __name__ == "__main__":
    game = Game(["dor", "oz"])
    game.start()