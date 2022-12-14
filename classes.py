import random
import typing
from dice_graphics import DICE_FACES, DICE_HEIGHT
from math import factorial


class Player:
    total_die_count = 0

    def __init__(self, name):
        self.name = name
        self.num_of_dice = 5
        self.hand = []
        self.dice_roll()
        self.call = False
        self.is_human = True
        Player.total_die_count += self.num_of_dice

    def get_name(self):
        return self.name

    def dice_roll(self):
        roll_results = []
        for _ in range(self.num_of_dice):
            roll = random.randint(1, 6)
            roll_results.append(roll)
        self.hand = roll_results

    def gen_dice_faces(self):
        dice_faces = []
        if len(self.hand) < 1:
            print(f'Player {self.name} has no die left')
        else:
            for val in self.hand:
                dice_faces.append(DICE_FACES[val])

            dice_faces_rows = []
            for row_idx in range(DICE_HEIGHT):
                row_string = ""
                for die in dice_faces:
                    row_string = row_string + ' ' + die[row_idx]
                dice_faces_rows.append(row_string)

            for row in dice_faces_rows:
                print(f"{row}")

    def make_decision(self, prev_bet):
        print(f'Last bet was {prev_bet["dice_count"]} dice of the value {prev_bet["dice_value"]}')
        print("Your hand is:")
        self.gen_dice_faces()
        action = input("Enter [b] to bet, or [c] to call: ")
        if action == "b":
            return "bet"
        if action == "c":
            return "call"

    def lose_die(self):
        if len(self.hand) > 0:
            self.hand.pop()
            self.num_of_dice -= 1
            Player.total_die_count -= 1

    def make_bet(self, bet):
        new_bet = {"dice_count" : 0 , "dice_value" : 0}
        print("Place your bet.")
        while True:
            try:
                new_bet["dice_value"] = int(input('Enter Value of die: '))
                new_bet["dice_count"] = int(input('Enter Number of die: '))
            except ValueError:
                print("The entered value is a not an integer. Try again")
                continue
            else:
                if self.bet_valid_check(new_bet["dice_count"], new_bet["dice_value"], bet):
                    return new_bet

    def bet_valid_check(self, new_bet_dice_count, new_bet_dice_val, bet):
        if not 1 <= new_bet_dice_val <= 6 or not 1 <= new_bet_dice_count <= Player.total_die_count:
            print(f"""You can't bet using a die value higher than 6
                     or a die count larger than the number of die on the table {Player.total_die_count}
                     Your bet was: {new_bet_dice_count} die with the value of {new_bet_dice_val}""")
            return False
        if not ((new_bet_dice_val > bet["dice_value"]) | (new_bet_dice_count > bet["dice_count"])):
            print(f"""You must place a bet with at least either a larger number or value of die
                      You current bet was {new_bet_dice_count} die with the value of {new_bet_dice_val}
                      while the previous bet is {bet["dice_count"]} of die with value of {bet["dice_value"]}""")
            return False
        return True


class NPCPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.is_human = False

    def make_decision(self, game_prev_bet):
        odds = self.calc_odds(game_prev_bet)
        if odds < 0.2:
            self.call = True
            return "call"
        return "bet" 

    def calc_odds(self, game_prev_bet):
        total_hidden_dice = Player.total_die_count - len(self.hand)
        dice_val_count = game_prev_bet["dice_count"] - self.hand.count(game_prev_bet["dice_value"])
        return round(factorial(total_hidden_dice)/factorial(total_hidden_dice - dice_val_count)
                     * pow(1/6, dice_val_count) * pow(5/6, total_hidden_dice - total_hidden_dice), 2)

    def make_bet(self, prev_bet):
        new_bet = {"dice_count" : 0 , "dice_value" : 0}
        curr_freq = 0
        max_freq = 0
        for i in self.hand:
            curr_freq = self.hand.count(i)
            if curr_freq > max_freq:
                max_freq = curr_freq
                dice_val_to_bet = i
        new_bet["dice_count"] = prev_bet["dice_count"] + 1
        new_bet["dice_value"] = dice_val_to_bet
        print(f'{self.name} bets that there is {new_bet["dice_count"]} die with value of'
              f' {new_bet["dice_value"]} on the table')
        return new_bet




class Game:
    def __init__(self, bot_names_list):
        self.bet = {"dice_count": 0, "dice_value": 6}
        self.list_of_players = []
        self.starting_player = ""
        self.current_player = ""
        self.add_players(bot_names_list)
        #self.set_starting_player()
        self.game_over = False

    def add_players(self, bot_names_list):
        number_of_bots = 0
        self.list_of_players.append(Player(input("Enter your name: ")))
        while number_of_bots < 1 or number_of_bots > 5:
            number_of_bots = int(input('Enter a number between 1 and 5 to choose how many AI players to have: '))
        for _ in range(number_of_bots):
            self.list_of_players.append(NPCPlayer(random.choice(bot_names_list)))

    #def set_starting_player(self):
    #    self.current_player = random.choice(self.list_of_players)
    #    print(f"{self.current_player.get_name()} starts the game\n")
    #    self.bet.update(self.current_player.make_bet(self.bet))
    def set_starting_player(self):
        if self.current_player == "":
            self.current_player = random.choice(self.list_of_players)
            if self.current_player.is_human:
                print("Your hand is:")
                self.current_player.gen_dice_faces()


    def get_next_player(self):
        self.current_player = self.list_of_players[(self.list_of_players.index(self.current_player) + 1) % len(self.list_of_players)]

    def check_winner(self):
        for player in self.list_of_players:
            total_dice_count = player.hand.count(self.bet["dice_value"])
        if total_dice_count < self.bet["dice_count"]:
            print(f"{self.current_player.get_name()}'s call was correct, everyone else loses a die")
            for player in self.list_of_players:
                if player.name != self.current_player.name:
                    player.lose_die()
        else:
            print(f"{self.current_player.get_name}'s call was wrong, he loses a die")
            self.current_player.lose_die()

    def resolve_round(self):
        while len(self.current_player.hand) == 0:
            self.get_next_player
        self.list_of_players = [player for player in self.list_of_players if not len(player.hand) == 0]

    def get_winner(self):
        if len(self.list_of_players) == 1:
            print(f"{self.list_of_players[0].get_name} is the winner!")


    def play_round(self):
        #while True:
        self.set_starting_player()
        self.bet.update(self.current_player.make_bet(self.bet))
        self.get_next_player()
        while len(self.list_of_players) > 1:
            player_decision = self.current_player.make_decision(self.bet)
            if player_decision == "call":
                print(f"Player {self.current_player.get_name()} calls that last bet was BS!")
                self.check_winner()
                self.resolve_round()
            if player_decision == "bet":
                self.bet.update(self.current_player.make_bet(self.bet))
            self.get_next_player()
        self.get_winner
        


if __name__ == "__main__":
    bot_names = ["player1", "player2", "player3", "player4", "player5"]
    oGame = Game(bot_names)
    #while len(oGame.list_of_players) > 1:
    #    oGame.play_round()
    #print(f"The winner of the game is {oGame.get_winner}")
    oGame.play_round()
    
