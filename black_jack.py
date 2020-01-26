from random import shuffle

class Card:
    'represents a playing card'
    
    def __init__(self, rank, suit):
        'initialize rank and suit of playing card'
        self.rank = rank
        self.suit = suit

    def getRank(self):
        'return rank of card'
        return self.rank
    
    def getSuit(self):
        'return suit of card'
        return self.suit

    def getRankValue(self):
        'return value of the rank of card'
        if self.rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            self.rank_value = int(self.rank)
            return self.rank_value
        elif self.rank in ['J', 'Q', 'K']:
            self.rank_value = 10
            return self.rank_value
        else: # Else it is 'A' for Ace
            self.rank_value = 11
            return self.rank_value

class Deck:
    'represents a deck of 52 cards'

    # ranks and suits are Deck class variables
    ranks = {'2', '3', '4', '5', '6', '7', '8', '9',
             '10', 'J', 'Q', 'K', 'A'}

    # suits is a set of 4 Unicode symbols representing the 4 suits
    suits = ['\u2660', '\u2661', '\u2662', '\u2663']

    def __init__(self):
        'initiate deck of 52 cards'
        self.deck = [] # deck is initially empty

        for suit in Deck.suits:
            for rank in Deck.ranks:
                self.deck.append(Card(rank, suit))

    def dealCard(self):
        'deal (pop and return) card from the top of the deck'
        return self.deck.pop()
    
    def shuffle(self):
        'shuffle the deck'
        shuffle(self.deck)
                
class Chips:
    'represents the chips or money for the game of blackjack'

    def __init__(self):
        'initiate chips for user, starting with 100'
        self.chips = 100 # user starts with 100 chips

    def betChips(self, chips_to_bet):
        'user selects amount of chips to bet, then subtract from chips'
        if chips_to_bet > self.chips: # if user bets more chips than they have
            self.chips_to_bet = self.chips # only bet all chips that they have
        else:
            self.chips_to_bet = chips_to_bet
        self.chips -= self.chips_to_bet
        print('You just bet {} chips, good luck!'.format(self.chips_to_bet))

    def winChips(self):
        'if user wins, their chips will be updated with their winnings'
        self.chips += (self.chips_to_bet * 2)
        print("You win!")

    def pushChips(self):
        'if user ties, their chips will be returned'
        self.chips += self.chips_to_bet
        print("You pushed!")

def deal(deck):
    p_card_1, p_card_2 = (deck.dealCard(), deck.dealCard()) # user's cards
    d_card_1, d_card_2 = (deck.dealCard(), deck.dealCard()) # dealer's cards
    return [p_card_1, p_card_2, d_card_1, d_card_2]

def hit(deck, cards):
    'takes deck and cards as arg, deals card from deck and appends to cards'
    card = deck.dealCard()
    cards.append(card)
    return cards

def print_cards(who, cards):
    card_string_1 = '{} cards:'.format(who)
    card_string_2 = ' [{} {}]'
    card_tuple = [] # start as list, but change to tuple in a few lines
    for card in cards:
        card_string_1 += card_string_2
    for card in cards:
        card_tuple.append(card.getRank())
        card_tuple.append(card.getSuit())
    card_tuple = tuple(card_tuple)
    print(card_string_1.format(*card_tuple))

def print_cards_dealer_init(cards):
    print("Dealer's cards: [{} {}] [X X]".format(
                cards.getRank(), cards.getSuit()))

def check_21(cards):
    'returns a tuple ex: (under, 16) which includes total value of cards'
    sum_of_cards = sum([card.getRankValue() for card in cards])
    num_of_aces = len([card for card in cards if card.getRank() == 'A'])

    while num_of_aces > 0:
        if sum_of_cards > 21:
            sum_of_cards -= 10
            num_of_aces -= 1
        else:
            break

    if sum_of_cards < 21:
        return ('under', sum_of_cards)
    elif sum_of_cards == 21:
        return ('blackjack', sum_of_cards)
    else:
        return ('bust', sum_of_cards)            

###############################################################################
game_on = False
play = input("Do you want to play BlackJack? ")
if play in ['Yes', 'Y', 'y', 'yes', 'ye', 'yes!', 'Yes!', 'Yest', 'yest']:
    print("Game on!\n--------------------------------------------------")
    game_on = True
else:
    print("OK. See you later!\n")
    
while game_on:
    chips = Chips() # User starts with 100 chips
    while chips.chips > 0:
        deck = Deck() # initialize the deck
        deck.shuffle() # shuffle the deck
        while len(deck.deck) > 10: # shuffle the deck if it gets too low
            print("Cards left in deck: {}".format(len(deck.deck)))
            print("You have {} chips".format(chips.chips))
            chips_bet = int(input(
'''How many chips do you want to bet? (Enter 0 to QUIT)
Chips to bet: '''))
            if chips_bet == 0: # if user bets 0 chips, game over and quit
                chips.chips = 0
                game_on = False
                break
            chips.betChips(chips_bet) # update chip holdings and track bet
            # Game starts here
            four_cards = deal(deck) # Deal first 4 cards (2 user, 2 dealer)
            player_cards = [four_cards[0], four_cards[1]]
            dealer_cards = [four_cards[2], four_cards[3]]
            # Print out players cards and dealers cards (only 1 visible)
            print_cards('Your', player_cards)
            print_cards_dealer_init(dealer_cards[0])
            # Check if user or dealer (or both) have 21
            player_value = check_21(player_cards)
            dealer_value = check_21(dealer_cards)
            if player_value[0] == 'blackjack':
                if dealer_value[0] == 'blackjack':
                    # Push, user gets chips back
                    chips.pushChips()
                else:
                    # You win, you have blackjack and dealer doesn't
                    chips.winChips()
            elif dealer_value[0] == 'blackjack':
                if player_value[0] == 'blackjack':
                    # Push, user gets chips back
                    chips.pushChips()
                else:
                    # You lose, dealer has blackjack and you don't
                    print("You lose!")
            ###################################################################
            else:
                # No one has blackjack, offer user to 'hit'
                while True:
                    player_hit = input(
                        "Press 1 for hit (any other key for stay): ")
                    if player_hit == '1':
                        player_cards = hit(deck, player_cards)
                        print_cards('Your', player_cards)
                        player_value = check_21(player_cards)
                        if player_value[0] == 'blackjack':
                            # You got blackjack, you win!
                            chips.winChips()
                            break
                        elif player_value[0] == 'bust':
                            # You busted, game over!
                            print("You lose!")
                            break
                    ###########################################################
                    else:
                        # You 'stayed' instead of 'hitting'
                        # If user doesn't win or bust,
                        # now dealer's turn to 'hit'
                        while True:
                            print_cards('Dealer', dealer_cards)
                            dealer_value = check_21(dealer_cards)
                            if dealer_value[1] >= 16:
                                break
                            else:
                                dealer_cards = hit(deck, dealer_cards)
                        # Check if dealer got 21 or bust
                        if dealer_value[0] == 'blackjack':
                            # You lose, dealer has blackjack and you don't
                            print("You lose!")
                            break
                        elif dealer_value[0] == 'bust':
                            # You win, dealer busted and you didn't
                            chips.winChips()
                            break
                        #######################################################
                        else:
                            # Heads up, who has the higher value
                            # (dealer or user)
                            if dealer_value[1] > player_value[1]:
                                # You lose, dealer is closer to 21
                                print("You lose!")
                                break
                            elif dealer_value[1] < player_value[1]:
                                # You win, you are closer to 21
                                chips.winChips()
                                break
                            else:
                                # Push, you tied the dealer
                                chips.pushChips()
                                break
            print_cards('Your', player_cards)
            print_cards('Dealer', dealer_cards)
            print("--------------------------------------------------")
            if chips.chips == 0:
                print("You have nothing left to bet! GAME OVER")
                game_on = False
                break
                
                    
            
