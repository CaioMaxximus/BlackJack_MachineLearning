def choose_move():
    
def in_game():
    
    player = True
    
    deck =  np.array(cards * 4)
    random.shuffle(deck)
    pl_points = 0
    dealer_points = 0
    number_moves = 0
    index = 0
    
    pl_game = []
    dealer_hand = []
    
    hand = Hand(deck[-2:], 100)
    
    pl_game , dealer_hand , deck = [hand], [deck[-3]] , deck[:-3]
    
    # game_status_vector
    
    
    local_data = pd.DataFrame()
    local_data['card1'], local_data['card2'] = [pl_game[0].cards[0]], [pl_game[0].cards[1]]
    local_data['two_hands'] = ['False']
    move_count = 1

    
    while (dealer_points < 21):
        
        if(player):
            
            move = choose_move_random(pl_game)
            
            print(move)
            if(move == 'P'):
                local_data['two_hands'] = ['True']
                pl_game = split(pl_game,deck)
                local_data['move_' + str(move_count)].append(move)
                

            else:
                #Execute moves 
                for i , hand in enumerate(pl_game):
                    
                    try:
                        local_data['move_' + str(move_count)].append(move[i])
                    except:
                        local_data['move_' + str(move_count)] = [move[i]]
                    move_count += 1
                        
                    player = True

                    if(move[i] == 'S'):
                        hand.playing = False 
                        player = False
                        
                    elif(move == 'H'):
                        
                        deck = hint(hand, deck)
                        # pos = len(hand.cards)
                        
                        # local_data['card' + str(pos)] = hand.cards[pos -1]
                        
                    elif(move == 'DD'):
                        
                        deck = double(hand, deck)
                print(hand.cards)
        else:
            
            print('dealer Time')
            break 
                                
    print(local_data)
