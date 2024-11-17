import random
from utils.dice_graphics import DICE_FACES, DICE_HEIGHT

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
                if self._bet_is_valid(new_bet, kwargs["prev_bet"]):
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


