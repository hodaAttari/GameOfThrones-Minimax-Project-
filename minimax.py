import random
import time
import copy

# Minimax parameters
DEPTH = 4  # Depth of lookahead
TIMEOUT = 10  # Matches main.py

# Helper weights for evaluation
BANNER_WEIGHT = 10
CARD_WEIGHT = 1
PROXIMITY_WEIGHT = 0.5


def get_move(cards, player1, player2):
    start_time = time.time()
    valid_moves = get_possible_moves(cards)

    if not valid_moves:
        return None

    best_move = None
    best_score = -float('inf')

    for move in valid_moves:
        if time.time() - start_time > TIMEOUT:
            break

        new_cards, new_player1, new_player2 = simulate_move(cards, player1, player2, move, True)
        score = minimax(new_cards, new_player1, new_player2, DEPTH - 1, False, -float('inf'), float('inf'))

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def minimax(cards, player1, player2, depth, maximizing_player, alpha, beta):
    if depth == 0 or is_game_over(cards):
        return evaluate_state(cards, player1, player2)

    valid_moves = get_possible_moves(cards)
    if not valid_moves:
        return evaluate_state(cards, player1, player2)

    if maximizing_player:
        max_eval = -float('inf')
        for move in valid_moves:
            new_cards, new_player1, new_player2 = simulate_move(cards, player1, player2, move, True)
            eval_score = minimax(new_cards, new_player1, new_player2, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_cards, new_player1, new_player2 = simulate_move(cards, player1, player2, move, False)
            eval_score = minimax(new_cards, new_player1, new_player2, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

def get_possible_moves(cards):
    varys_location = find_varys(cards)
    if varys_location is None:
        return []

    varys_row, varys_col = varys_location // 6, varys_location % 6
    moves = []

    for card in cards:
        if card.get_name() == 'Varys':
            continue

        row, col = card.get_location() // 6, card.get_location() % 6
        if row == varys_row or col == varys_col:
            moves.append(card.get_location())

    return moves

def evaluate_state(cards, player1, player2):
    player1_banners = sum(player1.get_banners().values()) * BANNER_WEIGHT
    player2_banners = sum(player2.get_banners().values()) * BANNER_WEIGHT

    player1_control = evaluate_player_control(player1, cards)
    player2_control = evaluate_player_control(player2, cards)

    return (player1_banners + player1_control) - (player2_banners + player2_control)

def evaluate_player_control(player, cards):
    return get_cards_in_hand(player) * CARD_WEIGHT

def simulate_move(cards, player1, player2, move, maximizing_player):
    new_cards = copy.deepcopy(cards)
    new_player1 = copy.deepcopy(player1)
    new_player2 = copy.deepcopy(player2)

    if maximizing_player:
        make_move(new_cards, move, new_player1)
    else:
        make_move(new_cards, move, new_player2)

    return new_cards, new_player1, new_player2

def make_move(cards, move, player):
    varys_location = find_varys(cards)
    if varys_location is None:
        return None

    varys_row, varys_col = varys_location // 6, varys_location % 6
    move_row, move_col = move // 6, move % 6

    selected_card = find_card(cards, move)
    removing_cards = []

    for i, card in enumerate(cards):
        if card.get_name() == 'Varys':
            varys_index = i
            continue

        if card.get_location() == move:
            continue

        row, col = card.get_location() // 6, card.get_location() % 6

        if (row == varys_row and varys_col < col < move_col) or \
            (row == varys_row and move_col < col < varys_col) or \
            (col == varys_col and varys_row < row < move_row) or \
            (col == varys_col and move_row < row < varys_row):

            if card.get_house() == selected_card.get_house():
                removing_cards.append(card)
                player.add_card(card)

    player.add_card(selected_card)
    cards[varys_index].set_location(move)

    for card in removing_cards:
        cards.remove(card)

    cards.remove(selected_card)
    return selected_card.get_house()

def find_varys(cards):
    for card in cards:
        if card.get_name() == 'Varys':
            return card.get_location()
    return None

def find_card(cards, location):
    for card in cards:
        if card.get_location() == location:
            return card
    return None

def get_cards_in_hand(player):
    return sum(len(cards) for cards in player.get_cards().values())

def is_game_over(cards):
    return len(get_possible_moves(cards)) == 0
