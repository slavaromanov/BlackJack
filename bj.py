from os import system
from sys import platform

class Player:
    def __init__(self, name):
        self.name = name
        self.scores = 0
        self.cards = dict()
        self.status = str()

    def change_status(self):
        if self.scores > 21:
            self.status = 'L'
        elif self.scores == 21:
            self.status = 'W'
        else:
            self.status = 'N'
        return self.status

    def get_scores(self):
        scores = sum(map(int, self.cards.values()))
        if scores <= 10 and self.has_ace():
            scores += 10
        self.scores = scores
        return self.scores

    def has_ace(self):
        for card in self.cards.keys():
            if card[0] == 'A':
                return 1
        return 0

    def add_card(self, card):
        self.cards.update(card)

    def get_name(self):
        return self.name

    def get_cards(self):
        out = str()
        for key in self.cards.keys():
            out += key[0:-1] + ' of {}'.format(self.suit_name(key[-1]))+'\t'
        return out

    def suit_name(self, suit):
        if suit == 'd': return 'diamonds'
        elif suit == 'c': return 'clubs'
        elif suit == 's': return 'spades'
        elif suit == 'h': return 'hearts'

class AIPlayer(Player):
    pass

class BlackJack:
    def __init__(self, *names):
        self.deck = self.init_deck()
        self.players = list(map(lambda p: self.get_card(p, i=2), [Player(i) for i in names]))
        self.winner = None
        self.turned = self.players[0]
        self.turn()

    def clear(self):
        if platform == 'win32':
            system('cls')
        else:
            system('clear')

    def init_deck(self):
        grades = (['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K'])
        out = dict()
        for bob in list(map(self.add_suits, grades)):
            for card in bob:
                out.update({card: self.get_cost(card)})
        return out

    def add_suits(self, card):
        suits = ['h', 'd', 'c', 's']
        return list(map(lambda suit: card+suit, suits))

    def get_cost(self, card):
        if card[0].isdigit(): return int(card[0])
        elif card[0] == 'A': return 1
        else: return 10

    def get_card(self, player, i=1):
        for n in range(i):
            card = self.deck.popitem()
            player.add_card({card[0]: card[1]})
        return player

    def turn(self, msg=''):
        while True:
            if self.turned.get_scores() >= 21:
                if self.players.index(self.turned) == len(self.players)-1:
                        self.game_end()
                        break
                else:
                        self.turned = self.players[self.players.index(self.turned)+1]
                        self.turn()
                        break
            self.print_table(msg+'{} is turning now!'.format(self.turned.get_name()))
            choice = input('Print Y for get new card or N for stop this\n').lower()
            if choice == 'y':
                self.get_card(self.turned)
            elif choice == 'n':
                if self.players.index(self.turned) == len(self.players)-1:
                    self.game_end()
                else:
                    self.turned = self.players[self.players.index(self.turned)+1]
                    self.turn()
                break
            else:
                self.turn('Input error\n')
                break

    def game_end(self):
        self.print_table()
        winners = list()
        notwinners = list()
        maximum = 0
        for player in self.players:
            status = player.change_status()
            if status == 'W':
                winners.append(player)
            elif status == 'N':
                if player.get_scores() > maximum:
                    notwinners = [player]
                elif player.get_scores() == maximum:
                    notwinners.append(player)
        if winners:
            print('Winners is:')
            for w in winners:
                print(w.get_name()+'!')
        elif notwinners:
            print('Winners is:')
            for w in notwinners:
                print(w.get_name()+'!')
        else:
            print('Casino win!')

    def print_table(self, msg=''):
        self.clear()
        print(msg)
        for player in self.players:
            print(player.get_name(), player.get_scores(), player.get_cards(), sep='\t')

BlackJack('Petya', 'Vasya', 'Elena', 'George', 'Lisa')
