'''
This bot is based on the alpha beta pruning and scans 5 rounds ahead to find a possible victory/lost using minmax.
The heuristic is equal to 1 if a win is found, -1 if a lost is found and 0 if the search was cut off.
'''


def simulate_p2(state,i):
# scans every possible move that p2 can make and returns -1 if p2 has a winning move, otherwise returns the minimum of the moves values
    moves = ['CA', 'CB', 'DA', 'DB', 'DC', 'CD']
    possible_moves = legal_possible_moves(state, moves) # subset of legal moves
    n = len(possible_moves)
    i += 1
    move_values = {}
    if i < 11:
        for move in possible_moves: # scans every possible move
            tapping_hand = move[0]
            tapped_hand = move[1]
            state_next = state.copy()
            if state[tapped_hand] == 0 and state[tapping_hand] == 4 : # first possible split
                state_next[tapped_hand] = 2
                state_next[tapping_hand] = 2
            elif state[tapped_hand] == 0 and state[tapping_hand] == 5 : # other possible split
                state_next[tapped_hand] = 2
                state_next[tapping_hand] = 3
            else:
                state_next[tapped_hand] += state_next[tapping_hand] # tap move
                if state_next[tapped_hand] > 5:
                    state_next[tapped_hand] = 0
                if lost_game(state_next):
                    # if p2 has a winning move returns -1
                    return -(1)
                
            move_values[move] = simulate_p1(state_next,i)
            # gives a value to every move return p1's move with maximimum value and iteratively calling p2's response move with minimum value
            
            if move_values[move] == -1: # pruning part
                return -1
                
            
            
        return min(move_values.values())
        # returns the minimum of the moves values that it's going to be the value of the previous p1 move

    else:
        return 0 # if i > 10 the search is too deep and returns 0


def simulate_p1(state, i):
# scans every possible move that p1 can make and returns i if p1 has a winning move, otherwise returns the maximum of the moves values
    moves = ['AB', 'AC', 'AD', 'BA', 'BC', 'BD']
    possible_moves = legal_possible_moves(state, moves) # subset of legal moves
    n = len(possible_moves)
    move_values = {}
    i += 1
    if i < 11:
        for move in possible_moves: # scans every possible move
            tapping_hand = move[0]
            tapped_hand = move[1]
            state_next = state.copy()
            if state[tapped_hand] == 0 and state[tapping_hand] == 4 : # first possible split
                state_next[tapped_hand] = 2
                state_next[tapping_hand] = 2
            elif state[tapped_hand] == 0 and state[tapping_hand] == 5 : # other possible split
                state_next[tapped_hand] = 2
                state_next[tapping_hand] = 3
            else:
                state_next[tapped_hand] += state_next[tapping_hand] # tap move
                if state_next[tapped_hand] > 5:
                    state_next[tapped_hand] = 0
                if won_game(state_next):
                    return (1)
                # if p1 has a winning move returns 1
                
            move_values[move] = simulate_p2(state_next,i)
            # gives a value to every move simulating p2's move with minimum value and iteratively calling p1's move with maximimum value
            
            if move_values[move] == 1: # pruning part
                return 1
            
                            
        return max(move_values.values())
        # returns the maximum of the moves' values that it's going to be the value of the previous p2 move
    else:
        return 0 # if i > 10 the search is too deep and returns 0






def is_legal(tapping_hand,tapped_hand,state):
# returns True if the move is legal
    if state[tapping_hand] == 0: return False # tapping hand needs to be unbusted
    if state[tapped_hand] == 0 and state[tapping_hand] < 4 : # split is legal only if x>=4
        return False
    move = tapping_hand + tapped_hand
    if move not in ['AB','BA','CD','DC']:
        if state[tapped_hand] == 0: return False # tapped hand needs to be unbusted if it's not a split situation
    return True

def legal_possible_moves(state, moves):
# returns a subset with only moves that are legal
    subset = []
    for move in moves:
        tapping_hand = move[0]
        tapped_hand = move[1]
        if is_legal(tapping_hand,tapped_hand,state): subset.append(move)
    return subset


def won_game(state):
# true if the move brings to victory
    if state['C'] == 0 and state['D'] == 0: 
        return True
    return False

def lost_game(state):
# true if the move brings to losing
    if state['A'] == 0 and state['B'] == 0: 
        return True
    return False


def generate_move(state_str):
    if state_str == 'A1B1C1D1':
        return 'AB'
    state = {'A': int(state_str[1]), 'B': int(state_str[3]), 'C': int(state_str[5]), 'D': int(state_str[7])}
    possible_moves = ['AB', 'AC', 'AD', 'BA', 'BC', 'BD']
    possible_moves = legal_possible_moves(state, possible_moves)
    
    best_move = ''
    move_values = {}
    for move in possible_moves: # scans every possible move
        i = 0 # iterative variables that will keep track of how many moves in advance the algorithm is looking
        tapping_hand = move[0]
        tapped_hand = move[1]
        state_next = state.copy()
        if state[tapped_hand] == 0 and state[tapping_hand] == 4 : # first possible split
            state_next[tapped_hand] = 2
            state_next[tapping_hand] = 2
        elif state[tapped_hand] == 0 and state[tapping_hand] == 5 : # other possible split
            state_next[tapped_hand] = 2
            state_next[tapping_hand] = 3
        else:
            state_next[tapped_hand] += state_next[tapping_hand] # tap move
            if state_next[tapped_hand] > 5:
                state_next[tapped_hand] = 0
            if won_game(state_next): # check if the move is a winning one, in that case it plays that one
                best_move = move
                break
        move_values[move] = simulate_p2(state_next, i)
        # gives a value to every move simulating p2's move with minimum value and iteratively calling p1's move with minimum value
            
        
    if best_move == '': 
        return max(move_values, key=move_values.get) # if there is no winning move returns the move with max value
    else:
        return best_move
    
