import random
import time
from dice_graphics import DICE_FACES, DICE_HEIGHT, START_SCREEN, START_TEXT

from scipy.stats import binom


class Player:
    """
    A class used to represent a player in 'liars' dice' game

    Attributes
    ----------
    name
        The name of the player
    num_of_dice
        The number of dice in a players hand
    is_human
        Marks if it is a human controlled player or an NPC

    Methods
    ---------
    get_name
        Return the name of the player
    dice_roll
        Rolls the dice in a players hand to generate a random hand
    gen_dice_face
        Print the faces of the dice in a players hand
    make_decision
        Prompts the player to make a decision to bet or call
    make_bet
        Prompts the player for a dice count and face to make a bet, if bet is valid it is returned
    lose_die
        Remove one die from a players hand
    bet_is_valid
        Check if a bet is valid according to the previous bet in the game
    """

    total_die_count = 0

    def __init__(self, name):
        self.name = name
        self.num_of_dice = 5
        self.hand = []
        self.dice_roll()
        self.is_human = True
        Player.total_die_count += self.num_of_dice

    def get_name(self):
        """Return a players name"""
        return self.name

    def dice_roll(self):
        """Roll the dice in a players hand"""
        roll_results = []
        for _ in range(self.num_of_dice):
            roll = random.randint(1, 6)
            roll_results.append(roll)
        self.hand = roll_results

    def gen_dice_faces(self):
        """Generate graphics for the dice in a players hand"""
        dice_faces = []
        if len(self.hand) < 1:
            print(f"Player {self.name} has no die left")
        else:
            for val in self.hand:
                dice_faces.append(DICE_FACES[val])
            dice_faces_rows = []
            for row_idx in range(DICE_HEIGHT):
                row_string = ""
                for die in dice_faces:
                    row_string = row_string + " " + die[row_idx]
                dice_faces_rows.append(row_string)

            for row in dice_faces_rows:
                print(f"{row}")

    def make_decision(self, **kwargs):
        """Prompt the player to make a decision whether to bet or call"""
        print(
            f'Last bet was {kwargs["game_prev_bet"].get("dice_count")} dice of the value'
            f' {kwargs["game_prev_bet"].get("dice_value")}'
        )
        print("Your hand is:")
        self.gen_dice_faces()
        action = input("Enter [b] to bet, or [c] to call: ")
        if action == "b":
            return "bet"
        if action == "c":
            return "call"

    def lose_die(self):
        """Remove one die from a players hand, to be used when he make a wrong call or his bluff is called"""
        if len(self.hand) > 0:
            self.hand.pop()
            self.num_of_dice -= 1
            Player.total_die_count -= 1

    def make_bet(self, **kwargs):
        """Prompt player to make a bet, and return it once a valid one is made"""
        new_bet = {"dice_count": 0, "dice_value": 0}
        print("Place your bet.")
        while True:
            try:
                new_bet["dice_value"] = int(input("Enter Value of die: "))
                new_bet["dice_count"] = int(input("Enter Number of die: "))
            except ValueError:
                print("The entered value is a not an integer. Try again")
                continue
            else:
                if self._bet_is_valid(new_bet, kwargs['prev_bet']):
                    return new_bet

    def _bet_is_valid(self, new_bet, prev_bet):
        """Check if a bet is valid based on the state of the game"""
        new = "\n"
        if (
            not 1 <= new_bet["dice_value"] <= 6
            or not 1 <= new_bet["dice_count"] <= Player.total_die_count
        ):
            if self.__class__.__name__ == "Player":
                print(
                    f"You can't bet using a die value higher than 6 {new}"
                    f"or a die count larger than the number of die on the table {Player.total_die_count} {new}"
                    f'Your bet was: {new_bet["dice_count"]} die with the value of {new_bet["dice_value"]} {new}'
                )
            return False
        if (
            new_bet["dice_count"] <= prev_bet["dice_count"]
            and not new_bet["dice_value"] > prev_bet["dice_value"]
        ) or (new_bet["dice_value"] < prev_bet["dice_value"]):
            if self.__class__.__name__ == "Player":
                print(
                    f"You must place a bet with either a higher count of the current face or any count of a higher face {new}"
                    f'Your current bet was {new_bet["dice_count"]} die with the value of {new_bet["dice_value"]} {new}'
                    f'while the previous bet is {prev_bet["dice_count"]} of die with value of {prev_bet["dice_value"]} {new}'
                )
            return False
        return True


class NPCPlayer(Player):
    """
    A class used to represent an NPC player in Liar's Dice game
    The class inherits some of the behavior from the Player class

    Attributes
    ----------
    The attributes for the class is inherited from the Player class

    Methods
    ---------
    calc_odds
        Calculates the probability for for a bet to be correct
        based on a NPCs own hand and the number of other dice on the table
    override make_decision
        The NPC player makes a decision based on odds of the previous bet in the game
    override make_bet
        The NPC makes a bet according to the most common dice in his hand
        If it is not a valid bet, it will be increased or randomized until it is valid
    """

    def __init__(self, name):
        super().__init__(name)
        self.is_human = False

    def make_decision(self, **kwargs):
        """NPC player chooses when to bet or call based on odds"""
        odds = self.calc_odds(kwargs['game_prev_bet'], kwargs['is_wild'])
        #TODO fix magic number 0.3
        if odds < 0.3:
            return "call"
        return "bet"

    def calc_odds(self, bet, is_wild):
        """Calculate the odds based on the previous bet made"""
        total_hidden_dice = Player.total_die_count - len(self.hand)
        dice_val_count = bet["dice_count"] - self.hand.count(bet["dice_value"])
        if is_wild:
            dice_val_count += self.hand.count(1)
            face_possibility = 2 / 6
        else:
            face_possibility = 1 / 6
        if dice_val_count > total_hidden_dice:
            return 0
        return round(
            1 - binom.cdf(dice_val_count - 1, total_hidden_dice, face_possibility), 2
        )

    def make_bet(self, **kwargs):
        """NPC player to make a bet based on dice in his hand, if best bet not a valid bet randomize to a valid one"""
        new_bet = {"dice_count": 0, "dice_value": 0}
        freq = 0
        for i in self.hand:
            freq = self.hand.count(i)
            if kwargs['is_wild'] and i != 1:
                freq += self.hand.count(1)
            if freq > new_bet['dice_count']:
                new_bet['dice_count'] = freq
                new_bet['dice_value'] = i
        if kwargs['is_wild'] and new_bet["dice_value"] == 1:
            new_bet['dice_value'] = random.randint(2, 6)
        while not self._bet_is_valid(new_bet, kwargs['prev_bet']):
            # bluff on random
            if random.random() < 0.3:
                new_bet['dice_value'], new_bet['dice_count'] = random.randint(
                    kwargs['prev_bet'].get('dice_value'), 6
                ), kwargs['prev_bet'].get('dice_count') + random.randint(-1, 1)
            else:
                new_bet['dice_value'], new_bet['dice_count'] = kwargs['prev_bet'].get(
                    'dice_value'
                ), kwargs['prev_bet'].get('dice_count') + random.randint(1, 2)
        print(
            f'{self.name} bets that there is {new_bet["dice_count"]} die with value of'
            f' {new_bet["dice_value"]} on the table'
        )
        time.sleep(1)
        return new_bet


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
        else:
            self.wild_ones = False

    def _add_players(self, bot_names_list):
        """Add the human player, prompt him regarding how many NPC players he wants in the game"""
        self.list_of_players = []
        number_of_bots = 0
        self.list_of_players.append(Player(input("Enter your name: ")))
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
            bot_names_list.remove(name)
            self.list_of_players.append(NPCPlayer(name))

    def _set_starting_player(self):
        """Set who will be the starting player for the game, if he is not an NPC, show his hand on the screen"""
        if self.current_player == "":
            self.current_player = random.choice(self.list_of_players)
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
                f"{self.current_player.get_name()}'s call was correct, {self.previous_player.get_name()}"
                " loses a die"
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
        print("\n\nStarting new round:")
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
        self.bet.update(self.current_player.make_bet(prev_bet=self.bet, is_wild=self.wild_ones))
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
                self.bet.update(self.current_player.make_bet(prev_bet=self.bet, is_wild=self.wild_ones))
                self._get_next_player()
