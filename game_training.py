import random
import numpy as np
import pandas as pd
from tqdm import tqdm

games = pd.DataFrame(columns = [ 'cards_initial', 'moves_initial','hand1_cards','hand2_cards','moves_1' , 'moves_2','dealer_hand','money'] )


class Hand:
        
    def __init__(self , cards, money):
        self.cards = cards
        self.playing = True
        self.money = money
        self.moves = []

    def hint_card(self ,card):
        self.cards.append(card)
        
    def add_move(self , move):
        self.moves.append(move) 

                  
def game(hand, dealer_hand, game_id):
    
    global deck
    player = True
    
    dealer_points = 0
    pl_points = 0
    splited = False
    hands = [hand]
    size = len(hands)
    series_vect = []
    series_vect.append(hand.cards)
    i = 0
    while i < size:
        hand = hands[i]
        while (hand.playing):
            
            move = choose_move_random(hand)
            
            #print(f'hand{i}', hand.moves)
            
            if(move == 'P' and not(splited)):

                new_hands = split(hand)
                hands = np.append(hands, new_hands)
                
                hand.add_move(move)
                hand.playing = False
                splited = True
                i+= 1
                size  = len(hands)
                
                
            else:
                #Execute moves

                player = True

                if(move == 'S'):
                   
                    hand.playing = False 
                    hand.add_move(move)
                    i+= 1
                elif(move == 'H'):
                   
                    hand.add_move(move)
                    deck = hint(hand, deck)
                    
                    
                elif(move == 'DD'):  
                    
                    hand.add_move(move)
                    deck = double(hand, deck)
                    hand.playing = False
                    i+= 1
            

                    
    while (dealer_points < 17):
        
        dealer_hand.append(deck[-1])
        deck = deck[:-1]
        dealer_points = sum_points(dealer_hand)
        
    final_money = 0        
    
    series_vect.append(hands[0].moves)
       
     
    if len(hands) == 1:
        final_money = cal_bet(hands[0], dealer_hand, dealer_points)
        series_vect.append([])
        series_vect.append([])
        series_vect.append([])
        series_vect.append([])

    else:
        
        final_money += cal_bet(hands[1], dealer_hand, dealer_points)
        final_money += cal_bet(hands[2], dealer_hand, dealer_points)
        series_vect.append(hands[1].cards)
        series_vect.append(hands[2].cards)
        series_vect.append(hands[1].moves)
        series_vect.append(hands[2].moves)

    series_vect.append(dealer_hand)
    series_vect.append(final_money)

    games.loc[game_id] = series_vect

 
def cal_bet(hand , dealer_hand, dealer_points):
    
    pl_points = sum_points(hand.cards)
    if(pl_points > 21):
        return - (hand.money)
    elif(pl_points == dealer_points):
        if((is_blackjack(hand.cards) and is_blackjack(dealer_hand))):
            return 0
        elif(is_blackjack(hand.cards)):
            return (hand.money * 3)/2
        elif(is_blackjack(dealer_hand)):
            return -(hand.money)
        else:
            return 0
    elif(pl_points < dealer_points and dealer_points < 22):
        return -(hand.money)
        
    else:
        return hand.money

    
def is_blackjack(cards):
    
    if ((len(cards) == 2) and ('A' in cards) and (convert_card(cards[0]) == 10 or convert_card(cards[1]) == 10)):
        return True
    
    return False 
                  
                  
def convert_card(card):

    if(type(card) is str and card != 'A'):
        return 10
    
    return card

def sum_points(cards):
    
    as_count = 0
    points = 0
    a_counts = 0
    for card in cards:
        value = convert_card(card)
        if (value == 'A'):
            a_counts += 1
        else:
            points += value
    for a in range(as_count):
        if(points + 11 < 21):
            points += 11
        else:
            points += 1
    return points
        
              
                  
def hint(hand , deck):
    hand.hint_card((deck[-1]))
    
    deck = deck[:-1]
    return deck

def double(hand, deck):
    
    hand.hint_card(deck[-1])
    deck = deck[:-1]
    hand.money =  hand.money * 2
    return deck

def split(hand):
    
    
    card1 = [hand.cards[0]]
    card2 = [hand.cards[1]]
    
    
    return [Hand(card1,hand.money),Hand(card2,hand.money)]
    
    

def choose_move_random(hand):
    
    cards = hand.cards
    options = []
    move  = ''
    if(len(cards) == 2 and convert_card(cards[0]) == convert_card(cards[1])):
        options = ['H', 'S', 'DD', 'P']
        random.shuffle(options)
        move = options[0]
    
        
    else:
        options = ['H', 'S', 'DD']
        random.shuffle(options)
        move = options[0]     
        
    return move       
    
    
cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'K','Q']

deck = []
def play_N_games(n):
    global deck
    for num in tqdm(range(n)):
        deck = (cards * 4)
        random.shuffle(deck)
        hand , dealer_hand , deck = Hand(deck[-2:], 100), [deck[-3]] , deck[:-3]
        game(hand , dealer_hand, num)

play_N_games(30000)

print(games.head())
games.to_csv (r'.\games.csv', index = False, header=True)
