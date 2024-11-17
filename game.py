import random
import time
from player import Player
from npc_player import NPCPlayer
from utils.dice_graphics import START_SCREEN, START_TEXT

class Game:
    """
    A class to represent the game of Liar's dice and coordinate the player classes

    Attributes
    ----------
    bet
        Dict to hold the number of dice (dice_count) and the dice face (dice_value) of the last made bet
    starting_player
        Set to the player starting the round
    current_player
        The player whose turn it currently is
    bot_names_list
        List of names to be used for the NPC players

    Methods
    ---------
    start_game
        Set the initial state of the game - print start screen, add players
    print_start_graphic
        Print the starting screen
    set_wild_mode
        Enable the wild ones mode where 1's count as the face of the current bet
    add_players
        Add the human controlled and a selected number of NPC players
    set_starting_player
        Set the starting player for the game
    get_next_player
        Get the next player who's turn it is
    check_winner
        Check who is the winner of the game an prints his name
    reroll_players_dice
        Reroll the dice in all players' hands
    resolve_round
        After a player calls a bet, check if call is correct or not, and remove dice and players accordingly, set player that wil start next round
    restart_for_new_round
        Resets the settings for the next round - call reroll_players_dice, reset the bet
    get_winner
        Check when only one player remains in the game, declare him the winner
    reveal_hands
        Print the hands of all players in the game
    play_game
        Play a game going through rounds until only one player remains
    """

    def __init__(self, bot_names_list):
        self.bet = {"dice_count": 0, "dice_value": 0}
        self.starting_player = ""
        self.current_player = ""
        self.bot_names_list = bot_names_list

    def start_game(self):
        """Setup the game - print starting graphics, add players, set wild ones mode"""
        self._print_start_graphic()
        self._add_players(self.bot_names_list)
        self._set_wild_mode()
        self._play_game()
        while continue_game != "n" or continue_game != "y":
            continue_game = input("Would you like to player another game (y/n): ")
        if continue_game == "y":
            self.init_game()
        else:
            print("Quitting game.")

    def _print_with_delay(self, text, delay=0.001):
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print("\n\n")

    def _print_start_graphic(self):
        """Print the graphics for the game, defined in dice_graphics.py"""
        for text in [START_TEXT, START_SCREEN]:
            self._print_with_delay(text)

    def _set_wild_mode(self):
        """Activate wild ones mode where 1's count as the face of the current bet"""
        while True:
            is_wild = input(
                "Would you like to enable wild ones mode and count ones as the face of the current bid (y/n): "
            )
            if is_wild == "y" or is_wild == "n":
                break
            else:
                print("Please enter either 'y'(yes) or 'n'(no)!")
        if is_wild == "y":
            self.wild_ones = True
            print("Wild mode activated!\n")
        else:
            print("Wild mode NOT active!\n")
            self.wild_ones = False

    def _add_players(self, bot_names_list):
        """Add the human player, prompt him regarding how many NPC players he wants in the game"""
        self.list_of_players = []
        number_of_bots = 0
        #self.list_of_players.append(Player(input("Enter your name: ")))
        self._add_human_player()
        while True:
            try:
                number_of_bots = int(
                    input(
                        "Please enter a number between 1 and 5 for how many AI players you would like to have: "
                    )
                )
                if 1 <= number_of_bots <= 5:
                    break
                else:
                    print("The number is not between 1 and 5.")
            except ValueError:
                print("The input is not a valid integer.")
        for _ in range(number_of_bots):
            name = random.choice(bot_names_list)
            print(f"{name} joins the game!")
            bot_names_list.remove(name)
            self.list_of_players.append(NPCPlayer(name))
    
    def _add_human_player(self):
        name = ""
        while(name == "" or name in self.bot_names_list):
            name=input("Enter your name: ")
            if not name:
                print("You cannot play with an empty name")
            if name in self.bot_names_list:
                print(f"The name {name} is already a reserved name for a bot player, choose a name that is a non-empty string and not one of the following names {self.bot_names_list}")

        self.list_of_players.append(Player(name))

    def _set_starting_player(self):
        """Set who will be the starting player for the game, if he is not an NPC, show his hand on the screen"""
        if self.current_player == "":
            self.current_player = random.choice(self.list_of_players)
            print("START GAME!!!")
            print(f"{self.current_player.get_name()} starts first!")
            if self.current_player.is_human:
                print("Your hand is:")
                self.current_player.gen_dice_faces()

    def _get_next_player(self):
        """Return the next player object from the ones in the game"""
        self.previous_player = self.current_player
        self.current_player = self.list_of_players[
            (self.list_of_players.index(self.current_player) + 1)
            % len(self.list_of_players)
        ]

    def _check_winner(self):
        """Check who is the winner depending on all dice on the table and last bet made"""
        total_dice_count = 0
        for player in self.list_of_players:
            total_dice_count += player.hand.count(self.bet["dice_value"])
            if self.wild_ones:
                total_dice_count += player.hand.count(1)
        if self.wild_ones:
            print(
                f"There is a total of {total_dice_count} {self.bet['dice_value']}'s when counting ones as well."
            )
        else:
            print(f"There is a total of {total_dice_count} {self.bet['dice_value']}'s.")
        if total_dice_count < self.bet["dice_count"]:
            print(
                f"{self.current_player.get_name()}'s call was correct, "
                f"{self.previous_player.get_name()} loses a die"
            )
            self.previous_player.lose_die()
        else:
            print(
                f"{self.current_player.get_name()}'s call was wrong, {self.current_player.get_name()} loses a die"
            )
            self.current_player.lose_die()

    def _reroll_player_dice(self):
        """Re-roll the dice for each player in the game"""
        for player in self.list_of_players:
            player.dice_roll()

    def _resolve_round(self):
        """Remove all players which have no dice left, if the player who should be next in turn has 0 dice, set the next player"""
        while len(self.current_player.hand) == 0:
            self._get_next_player()
        for player in self.list_of_players:
            if len(player.hand) == 0:
                print(f"{player.get_name()} is out of the game")
        self.list_of_players = [
            player for player in self.list_of_players if not len(player.hand) == 0
        ]
        if len(self.list_of_players) == 1:
            self._get_winner()

    def _restart_for_new_round(self):
        """Resets the table for a new round - the dice in each players hands will be re-rolled, bet value will be reset"""
        input("\n[Press enter to continue to next round]")
        print("\n\nStarting new round!")
        print(f"{self.current_player.get_name()} starts the round!")
        time.sleep(1)
        self._reroll_player_dice()
        self.bet = {"dice_count": 0, "dice_value": 0}
        if self.current_player.is_human:
            print("Your hand is: ")
            self.current_player.gen_dice_faces()

    def _get_winner(self):
        """Print the name of the winner, who will be the only remaining player in the game"""
        print(f"{self.list_of_players[0].get_name()} is the winner!")
        exit()

    def _reveal_hands(self):
        """Display the hands of all participating players in the game"""
        for player in self.list_of_players:
            print(f"{player.get_name()}'s hand is:")
            player.gen_dice_faces()
            time.sleep(1)

    def _play_game(self):
        """Play rounds looping through each player until only one remains"""
        self._set_starting_player()
        self.bet.update(
            self.current_player.make_bet(prev_bet=self.bet, is_wild=self.wild_ones)
        )
        self._get_next_player()
        while True:
            player_decision = self.current_player.make_decision(
                game_prev_bet=self.bet, is_wild=self.wild_ones
            )
            if player_decision == "call":
                print(f"{self.current_player.get_name()} calls that last bet was BS!")
                print("Revealing all players hands!!!")
                self._reveal_hands()
                self._check_winner()
                self._resolve_round()
                self._restart_for_new_round()
                player_decision = "bet"
            if player_decision == "bet":
                self.bet.update(
                    self.current_player.make_bet(
                        prev_bet=self.bet, is_wild=self.wild_ones
                    )
                )
                self._get_next_player()
