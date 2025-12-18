from enum import Enum


class Suit(Enum):

    HEARTS = "\u2665"
    DIAMONDS = "\u2666"
    CLUBS = "\u2663"
    SPADES = "\u2660"
    WILD = "W"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"{self.value}"


class Card():
    def __init__(self,rank = 0,suit = 0):
        self._rank = rank
        self._suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    @property
    def rank(self):
        return self._rank
    
    @property
    def suit(self):
        return self._suit
    
    @property
    def chips(self):

        chip_value = 0
         
        num_set = {"1","2","3","4","5","6","7","8","9","10"}

        if self.rank in num_set:
            chip_value = int(self.rank)
        
        elif self.rank == "A":
            chip_value = 11
        
        else:
            chip_value = 10
        
        return chip_value


class SilverCard(Card):

    def __init__(self,rank,suit):
        super().__init__(rank,suit)

    def __repr__(self):
        return f"Silver {self.rank}{self.suit}"

    def __str__(self):
        return f"Silver {self.rank}{self.suit}"

    @property
    def chips(self):
        card_chips = super().chips
        return card_chips * 2


class GoldCard(Card):

    def __init__(self,rank,suit):
        super().__init__(rank,suit)

    def __repr__(self):
        return f"Gold {self.rank}{self.suit}"

    def __str__(self):
        return f"Gold {self.rank}{self.suit}"
    
    @property
    def chips(self):
        card_chips = super().chips
        return card_chips * 4


class WildCard(Card):

    def __init__(self,rank):
        suit = Suit.WILD
        super().__init__(rank,suit)

    def __repr__(self):
        return f"Wild {self.rank}{self.suit}"
    
    def __str__(self):
        return f"Wild {self.rank}{self.suit}"
    
    @property
    def chips(self): 
        return super().chips


class Joker():

    def __init__(self, chips, mult, action = lambda chips, mult: (chips, mult)):
        self._chips = chips
        self._mult = mult
        self._action = action

    def __repr__(self):
        return f"Joker({self._chips}{self._mult}{self._action})"

    def __str__(self):
        return f"({self._chips}{self._mult}{self._action})"
    
    @property
    def chips(self):
        return self._chips
    
    @property
    def mult(self):
        return self._mult
    
    @property
    def action(self):
        return self._action
    

def score(cards,jokers):

    if len(cards) != 5:
        return 0
    
    value = 0
    mult = 1
    same_cards = [0,0,0,0,0,0,0,0]

    #add card value & count repeating
    for card in cards:
        value += card.chips

        if card.rank == "A":
            same_cards[0] += 1
        if card.rank == "K":
            same_cards[1] += 1
        if card.rank == "Q":
            same_cards[2] += 1
        if card.rank == "J":
            same_cards[3] += 1
        
        if  card.suit == Suit.HEARTS:
            same_cards[4] += 1
        if card.suit == Suit.DIAMONDS:
            same_cards[5] += 1
        if card.suit == Suit.CLUBS:
            same_cards[6] += 1
        if card.suit == Suit.SPADES:
            same_cards[7] += 1
        
        if isinstance(card,WildCard) == True:
            for i in same_cards:
                same_cards[i] += 1
    print(f"{same_cards = }")

    for i in same_cards:
        if i > 1:
            mult += i
    
    if  len(jokers) != 0:
        for joker in jokers:
            value += joker.chips
            mult += joker.mult

        #needed to add everything first per instructions

        for joker in jokers:
            do_stuff = joker.action
            value, mult = do_stuff(value,mult)

    print(f"{value = },{mult = }")
    return value * mult

#test1
#c1 = Card("A", Suit.CLUBS)
#c2 = Card("K", Suit.HEARTS)
#c3 = Card("K", Suit.SPADES)
#c4 = Card("7", Suit.DIAMONDS)
#c5 = Card("2", Suit.DIAMONDS)

#print(score([c1, c2, c3, c4, c5], []))
#passed

#test2
#c1 = Card("A", Suit.CLUBS)
#c2 = SilverCard("K", Suit.DIAMONDS)
#c3 = GoldCard("K", Suit.HEARTS)
#c4 = WildCard("A")
#c5 = Card("A", Suit.SPADES)

#j1 = Joker(5, 2)
#j2 = Joker(10, 3, action=lambda chips, mult: (chips + 10, mult * 2))

#print(score([c1, c2, c3, c4, c5], [j1, j2]))
#passed

#test3
#c1 = Card("A", Suit.HEARTS)
#c2 = Card("K", Suit.HEARTS)
#c3 = Card("Q", Suit.HEARTS)
#c4 = Card("J", Suit.HEARTS)
#c5 = Card("10", Suit.HEARTS)

#j1 = Joker(1, 1, action=lambda chips, mult: (chips + 10, mult * 2))
#j2 = Joker(1, 1, action=lambda chips, mult: (chips + 10, mult + 3))

#print(score([c1, c2, c3, c4, c5], [j1, j2]))
#passed

#test4
#c1 = Card("A", Suit.HEARTS)
#c2 = Card("K", Suit.HEARTS)
#c3 = Card("Q", Suit.HEARTS)
#c4 = Card("J", Suit.HEARTS)
#c5 = Card("10", Suit.HEARTS)

#j1 = Joker(1, 1, action=lambda chips, mult: (chips + 10, mult * 2))
#j2 = Joker(1, 1, action=lambda chips, mult: (chips + 10, mult + 3))

#print(score([c1, c2, c3, c4, c5], [j2, j1]))
#passed
