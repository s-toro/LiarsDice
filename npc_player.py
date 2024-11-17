import random
import time
from scipy.stats import binom
from player import Player

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
        odds = self.calc_odds(kwargs["game_prev_bet"], kwargs["is_wild"])
        # TODO fix magic number 0.3
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
            if kwargs["is_wild"] and i != 1:
                freq += self.hand.count(1)
            if freq > new_bet["dice_count"]:
                new_bet["dice_count"] = freq
                new_bet["dice_value"] = i
        if kwargs["is_wild"] and new_bet["dice_value"] == 1:
            new_bet["dice_value"] = random.randint(2, 6)
        while not self._bet_is_valid(new_bet, kwargs["prev_bet"]):
            # bluff on random
            if random.random() < 0.3:
                new_bet["dice_value"], new_bet["dice_count"] = random.randint(
                    kwargs["prev_bet"].get("dice_value"), 6
                ), kwargs["prev_bet"].get("dice_count") + random.randint(-1, 1)
            else:
                new_bet["dice_value"], new_bet["dice_count"] = kwargs["prev_bet"].get(
                    "dice_value"
                ), kwargs["prev_bet"].get("dice_count") + random.randint(1, 2)
        print(
            f'{self.name} bets that there is {new_bet["dice_count"]} die with value of'
            f' {new_bet["dice_value"]} on the table'
        )
        time.sleep(1)
        return new_bet
