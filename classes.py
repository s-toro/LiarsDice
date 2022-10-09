import random
from dice_graphics import DICE_FACES, DICE_HEIGHT


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

    def make_decision(self):
        pass #TODO implement func for a human player to choose between betting and calling

    def lose_die(self):
        if len(self.hand) > 0:
            self.hand.pop()
            self.num_of_dice -= 1
            Player.total_die_count -= 1

    def make_bet(previous_bet, player):
        new_bet = [0, 0]
        valid_bet = False
        print("Place your bet")
        # TODO: catch if bet is not digits
        while not valid_bet:
            new_bet[0] = int(input('Enter Number of die: '))
            new_bet[1] = int(input('Enter Value of die:'))
            valid_bet = self.bet_valid_check(new_bet, previous_bet)
        return new_bet

    def bet_valid_check(self, bet, previous_bet):
        if bet[0] <= previous_bet[0] and bet[1] <= previous_bet[1]:
            print('You have to bet a higher number of die, or the same number but with larget die value.')
            return False
        elif bet[0] > Player.total_die_count or bet[1] > 6:
            print(
                f"You can't bet a number of die larger than the current amount of dice on the table {Player.total_die_count}")
            return False
        else:
            return True


class NPCPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.is_human = False

    def calc_odds(self, face_val):
        return round(Player.total_die_count / 6) + self.hand.count(face_val)

    def make_bet(previous_bet, player):
        new_bet = [0, 0]
        valid_bet = False
        die_val = previous_bet[1]
        odds = best_odds
        for face_val in range(1, 7):
            odds = player.calc_odds(face_val)
            if face_val <= previous_bet[1]:
                odds -= 1
            if odds > best_odds:
                die_val = face_val
                best_odds = odds
        if die_val <= previous_bet[1]:
            new_bet[0] = previous_bet[0] + 1
        else:
            new_bet[0] = previous_bet[0]
        new_bet[1] = die_val
        print(f'{player.name} bets that there is {new_bet[0]} die with value of {new_bet[1]} on the table')
        return new_bet

        def make_decision(self):
            pass #TODO reimplement the decision making for the AI player to choose calling or raising based on odds


class Game:
    def __init__(self, bot_names_list):
        self.bet = {"dice_count": 0, "dice_value": 6}
        self.list_of_players = []
        self.starting_player = ""
        self.next_player = ""
        self.add_players(bot_names_list)
        self.set_starting_player()
        self.game_over = False

    def add_players(self, bot_names_list):
        number_of_bots = 0
        self.list_of_players = []
        self.list_of_players.append(Player(input("Enter your name: ")))
        while number_of_bots < 1 or number_of_bots > 5:
            number_of_bots = int(input('Enter a number between 1 and 5 to choose how many AI players to have: '))
        for _ in range(number_of_bots):
            self.list_of_players.append(NPCPlayer(random.choice(bot_names_list)))

    def set_starting_player(self):
        self.next_player = random.choice(self.list_of_players)
        self.next_player.make_bet()

    def get_next_player(self):
        return (self.list_of_players.index(self.next_player) + 1) % len(self.list_of_players)

    def check_winner(self):
        pass #TODO: implement a winnder checker

    def play_round(self):
        for _ in range(len(self.list_of_players)):
            self.get_next_player()
            self.next_player.make_decision(self.bet)
            if self.next_player.call is True:
                self.next_player.call = False
                break
        self.check_winndr



if __name__ == "__main__":
    bot_names = ["player1", "player2", "player3", "player4", "player5"]
    oGame = Game(bot_names)
    for player in oGame.list_of_players:
        player.gen_dice_faces()
        player.lose_die()
    for player in oGame.list_of_players:
        player.gen_dice_faces()
