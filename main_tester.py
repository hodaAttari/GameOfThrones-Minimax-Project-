import argparse
import importlib
import concurrent.futures
import random
from os import name as os_name
from os import system as os_system
from os.path import abspath, join, dirname
import sys
import json
import copy
import pygraphics
from utils.classes import Card, Player

# Add the utils folder to the path
sys.path.append(join(dirname(abspath(__file__))))

# Import the utils


# Set the path of the file
path = dirname(abspath(__file__))

TIMEOUT = 10  # Time limit for the AI agent

parser = argparse.ArgumentParser(description="A Game of Thrones: Hand of the King")
parser.add_argument('--player1', metavar='p1', type=str, help="either human or an AI file", default='human')
parser.add_argument('--player2', metavar='p2', type=str, help="either human or an AI file", default='human')
parser.add_argument('-l', '--load', type=str, help="file containing starting board setup (for repeatability)", default=None)
parser.add_argument('-s', '--save', type=str, help="file to save board setup to", default=None)

def make_board():
    '''
    This function creates a random board for the game.

    Returns:
        cards (list): list of Card objects
    '''

    # Load the characters
    with open(join(path, "assets", "characters.json"), 'r') as file:
        characters = json.load(file)

    cards = [] # List to hold the cards

    for i in range(36):
        # Get a random character
        house = random.choice(list(characters.keys()))
        name = random.choice(characters[house])

        # Remove the character from the dictionary
        characters[house].remove(name)
        if len(characters[house]) == 0:
            del characters[house]
        
        card = Card(house, name, i)

        cards.append(card)

    return cards

def save_board(cards, filename='board'):
    '''
    This function saves the board to a file.

    Parameters:
        cards (list): list of Card objects
        filename (str): name of the file to save the board to
    '''

    cards_json = []

    for card in cards:
        card_json = {'house': card.get_house(), 'name': card.get_name(), 'location': card.get_location()}
        cards_json.append(card_json)

    with open(join(path, "boards", filename + ".json"), 'w') as file:
        json.dump(cards_json, file, indent=4)

def load_board(filename='board'):
    '''
    This function loads the board from a file.

    Parameters:
        filename (str): name of the file to load the board from

    Returns:
        cards (list): list of Card objects
    '''

    with open(join(path, "boards", filename + ".json"), 'r') as file:
        cards = json.load(file)
    
    cards = [Card(card['house'], card['name'], card['location']) for card in cards]

    return cards

def find_varys(cards):
    '''
    This function finds the location of Varys on the board.

    Parameters:
        cards (list): list of Card objects

    Returns:
        varys_location (int): location of Varys
    '''

    varys = [card for card in cards if card.get_name() == 'Varys']

    varys_location = varys[0].get_location()

    return varys_location

def get_possible_moves(cards):
    '''
    This function gets the possible moves for the player.

    Parameters:
        cards (list): list of Card objects

    Returns:
        moves (list): list of possible moves
    '''

    # Get the location of Varys
    varys_location = find_varys(cards)

    # Get the row and column of Varys
    varys_row, varys_col = varys_location // 6, varys_location % 6

    moves = []

    # Get the cards in the same row or column as Varys
    for card in cards:
        if card.get_name() == 'Varys':
            continue

        row, col = card.get_location() // 6, card.get_location() % 6

        if row == varys_row or col == varys_col:
            moves.append(card.get_location())

    return moves

def calculate_winner(player1, player2):
    '''
    This function determines the winner of the game.

    Parameters:
        player1 (Player): player 1
        player2 (Player): player 2

    Returns:
        winner (int): 1 if player 1 wins, 2 if player 2 wins
    '''

    player1_banners = player1.get_banners()
    player2_banners = player2.get_banners()

    # Calculate the scores of the players
    player1_score = sum(player1_banners.values())
    player2_score = sum(player2_banners.values())

    if player1_score > player2_score:
        return 1
    
    elif player2_score > player1_score:
        return 2
    
    # If the scores are the same, whoever has the banner of the house with the most cards wins
    else:
        if player1_banners['Stark'] > player2_banners['Stark']:
            return 1
        
        elif player2_banners['Stark'] > player1_banners['Stark']:
            return 2
        
        elif player1_banners['Greyjoy'] > player2_banners['Greyjoy']:
            return 1
        
        elif player2_banners['Greyjoy'] > player1_banners['Greyjoy']:
            return 2
        
        elif player1_banners['Lannister'] > player2_banners['Lannister']:
            return 1
        
        elif player2_banners['Lannister'] > player1_banners['Lannister']:
            return 2
        
        elif player1_banners['Targaryen'] > player2_banners['Targaryen']:
            return 1
        
        elif player2_banners['Targaryen'] > player1_banners['Targaryen']:
            return 2
        
        elif player1_banners['Baratheon'] > player2_banners['Baratheon']:
            return 1
        
        elif player2_banners['Baratheon'] > player1_banners['Baratheon']:
            return 2
        
        elif player1_banners['Tyrell'] > player2_banners['Tyrell']:
            return 1
        
        elif player2_banners['Tyrell'] > player1_banners['Tyrell']:
            return 2
        
        elif player1_banners['Tully'] > player2_banners['Tully']:
            return 1
        
        elif player2_banners['Tully'] > player1_banners['Tully']:
            return 2

def find_card(cards, location):
    '''
    This function finds the card at the location.

    Parameters:
        cards (list): list of Card objects
        location (int): location of the card

    Returns:
        card (Card): card at the location
    '''

    for card in cards:
        if card.get_location() == location:
            return card

def make_move(cards, move, player):
    '''
    This function makes a move for the player.

    Parameters:
        cards (list): list of Card objects
        move (int): location of the card
        player (Player): player making the move
    '''

    # Get the location of Varys
    varys_location = find_varys(cards)

    # Find the row and column of Varys
    varys_row, varys_col = varys_location // 6, varys_location % 6

    # Get the row and column of the move
    move_row, move_col = move // 6, move % 6

    # Find the selected card
    selected_card = find_card(cards, move)
    
    removing_cards = []

    # Find the cards that should be removed
    for i in range(len(cards)):
        if cards[i].get_name() == 'Varys':
            varys_index = i
            continue
        
        # If the card is between Varys and the selected card and has the same house as the selected card
        if varys_row == move_row and varys_col < move_col:
            if cards[i].get_location() // 6 == varys_row and varys_col < cards[i].get_location() % 6 < move_col and cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                # Add the card to the player's cards
                player.add_card(cards[i])
        
        elif varys_row == move_row and varys_col > move_col:
            if cards[i].get_location() // 6 == varys_row and move_col < cards[i].get_location() % 6 < varys_col and cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                # Add the card to the player's cards
                player.add_card(cards[i])
        
        elif varys_col == move_col and varys_row < move_row:
            if cards[i].get_location() % 6 == varys_col and varys_row < cards[i].get_location() // 6 < move_row and cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                # Add the card to the player's cards
                player.add_card(cards[i])
        
        elif varys_col == move_col and varys_row > move_row:
            if cards[i].get_location() % 6 == varys_col and move_row < cards[i].get_location() // 6 < varys_row and cards[i].get_house() == selected_card.get_house():
                removing_cards.append(cards[i])

                # Add the card to the player's cards
                player.add_card(cards[i])
    
    # Add the selected card to the player's cards
    player.add_card(selected_card)

    # Set the location of Varys
    cards[varys_index].set_location(move)
        
    # Remove the cards
    for card in removing_cards:
        cards.remove(card)
    
    # Remove the selected card
    cards.remove(selected_card)

    # Return the selected card's house
    return selected_card.get_house()

def set_banners(player1, player2, last_house, last_turn):
    '''
    This function sets the banners for the players.

    Parameters:
        player1 (Player): player 1
        player2 (Player): player 2
        last_house (str): house of the last chosen card
        last_turn (int): last turn of the player
    
    Returns:
        player1_status (dict): status of the cards for player 1
        player2_status (dict): status of the cards for player 2
    '''

    # Get the cards of the players
    player1_cards = player1.get_cards()
    player2_cards = player2.get_cards()

    # Get the banners of the players
    player1_banners = player1.get_banners()
    player2_banners = player2.get_banners()

    # Initialize the status of the cards
    player1_status = {}
    player2_status = {}

    for house in player1_cards.keys():
        # Flag to keep track of the selected player
        selected_player = None

        # The player with the more cards of a house gets the banner
        if len(player1_cards[house]) > len(player2_cards[house]):
            # Give the banner to player 1
            selected_player = 1
        
        elif len(player2_cards[house]) > len(player1_cards[house]):
            # Give the banner to player 2
            selected_player = 2
        
        # If the number of cards is the same, the player who chose the last card of that house gets the banner
        else:
            if last_house == house:
                if last_turn == 1:
                    # Give the banner to player 1
                    selected_player = 1

                else:
                    # Give the banner to player 2
                    selected_player = 2

            else:
                if player1_banners[house] > player2_banners[house]:
                    selected_player = 1
                elif player2_banners[house] > player1_banners[house]:
                    selected_player = 2
        
        # If player 1 should get the banner
        if selected_player == 1:
            # Give the banner to player 1
            player1.get_house_banner(house)
            player2.remove_house_banner(house)

            # Set the status of the cards
            if len(player1_cards[house]) != 0:
                player1_status[house] = len(player1_cards[house]), 'Green'
            
            else:
                player1_status[house] = len(player1_cards[house]), 'White'
            
            player2_status[house] = len(player2_cards[house]), 'White'
        
        elif selected_player == 2:
            # Give the banner to player 2
            player1.remove_house_banner(house)
            player2.get_house_banner(house)

            # Set the status of the cards
            if len(player2_cards[house]) != 0:
                player2_status[house] = len(player2_cards[house]), 'Green'
            
            else:
                player2_status[house] = len(player2_cards[house]), 'White'
            
            player1_status[house] = len(player1_cards[house]), 'White'

        else:
            player2_status[house] = len(player2_cards[house]), 'White'
            player1_status[house] = len(player1_cards[house]), 'White'

    return player1_status, player2_status

def clear_screen():
    '''
    This function clears the screen.
    '''

    if os_name == 'nt': # Windows
        os_system('cls')
    
    else: # Mac and Linux
        os_system('clear')

def print_cards_status(player1_status, player2_status):
    '''
    This function prints the status of cards of the players.

    Parameters:
        player1_status (dict): status of the cards for player 1
        player2_status (dict): status of the cards for player 2
    '''

    # Clear the screen
    # clear_screen()

    # Print the status of the cards
    print("Player 1 cards status:", end=' ')
    for house, status in player1_status.items():
        try:
            # If player 1 has the banner of the house
            if status[1] == 'Green':
                # Print the house in color green
                print(f"\033[92m{house}: {status[0]}\033[0m", end=' ')
            
            else:
                # Print the house in color white
                print(f"\033[97m{house}: {status[0]}\033[0m", end=' ')
        
        except:
            print(f"{house}: {status[0]}", end=' ')
    
    # Print a new line
    print()

    print("Player 2 cards status:", end=' ')
    for house, status in player2_status.items():
        try:
            # If player 2 has the banner of the house
            if status[1] == 'Green':
                # Print the house in color green
                print(f"\033[92m{house}: {status[0]}\033[0m", end=' ')
            
            else:
                # Print the house in color white
                print(f"\033[97m{house}: {status[0]}\033[0m", end=' ')
        
        except:
            print(f"{house}: {status[0]}", end=' ')
    
    # Print a new line
    print()

def try_get_move(agent, cards, player1, player2):
    '''
    This function tries to get the move from the AI agent.

    Parameters:
        agent (module): AI agent
        cards (list): list of Card objects
        player1 (Player): player 1
        player2 (Player): player 2

    Returns:
        move (int): location of the card
    '''
    
    # Try to get the move from the AI agent in TIMEOUT seconds
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(agent.get_move, copy.deepcopy(cards), copy.deepcopy(player1), copy.deepcopy(player2))

        try:
            move = future.result(timeout=TIMEOUT)
        
        except concurrent.futures.TimeoutError:
            move = None
    
    return move
            
def main(args):
    '''
    This function runs the game.

    Parameters:
        args (Namespace): command line arguments
    '''

    p1win = 0
    p2win = 0

    for i in range(50):

        if args.load:
            try:
                cards = load_board(args.load)
            
            except FileNotFoundError:
                print("File not found. Creating a new board.")
                cards = make_board()
        
        else:
            cards = make_board()
        
        if args.save:
            try:
                save_board(cards, args.save)
            
            except:
                print("Error saving board.")
        
        if args.player1 == 'human':
            player1_agent = None
        
        else:
            try:
                player1_agent = importlib.import_module(args.player1)
            
            except ImportError:
                print("AI file not found.")
                return
            
            if not hasattr(player1_agent, 'get_move'):
                print("AI file does not have the get_move function.")
                return
        
        if args.player2 == 'human':
            player2_agent = None
        
        else:
            try:
                player2_agent = importlib.import_module(args.player2)
            
            except ImportError:
                print("AI file not found.")
                return
            
            if not hasattr(player2_agent, 'get_move'):
                print("AI file does not have the get_move function.")
                return
        
        player1 = Player(args.player1)
        player2 = Player(args.player2)

        turn = 1 # 1: player 1's turn, 2: player 2's turn

        while True:
            moves = get_possible_moves(cards)

            if len(moves) == 0:
                
                winner = calculate_winner(player1, player2)

                p1 = sum(player1.get_banners().values())
                p2 = sum(player2.get_banners().values())
                print(i,")", end=' ')
                if winner == 1:
                    print(f"\033[92m{p1}", end=' ')
                    print(":", end=' ')
                    print(f"\033[97m{p2}", end=' ')
                    p1win += 1
                else:
                    print(f"\033[97m{p1}", end=' ')
                    print(":", end=' ')
                    print(f"\033[92m{p2}", end=' ')
                    print("-", end=' ')
                    p2win += 1

                break

            if turn == 1:
                move = try_get_move(player1_agent, cards, player1, player2)

                if move is None:
                    turn = 2
            
            else:
                move = try_get_move(player2_agent, cards, player1, player2)

                if move is None:
                    turn = 1
            
            if move in moves:
                selected_house = make_move(cards, move, player1 if turn == 1 else player2)
                player1_status, player2_status = set_banners(player1, player2, selected_house, turn)
                turn = 2 if turn == 1 else 1
            
        print()

    print(p1win, p2win)

if __name__ == "__main__":
    main(parser.parse_args())