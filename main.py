import random

from dice_graphics import DICE_FACES, DICE_HEIGHT


bot_names = ['Maccus', 'Ratlin', 'Penrod', 'Jimmy Legs', 'Koleniko', 'Greenbeard', 'Clanker', 'Crash', 'Hadras', 'Wyvern'] 

class Player():
    def __init__(self, name):
        self.name = name
        self.num_of_dice = 6
        self.hand = []
        self.dice_roll()


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
                    row_string = row_string + " " + die[row_idx]
                dice_faces_rows.append(row_string)
            
            for row in dice_faces_rows:
                print(f"{row}")


    def lose_die(self):
        if len(self.hand) > 0:
             self.hand.pop()
             self.num_of_dice -= 1


def addBots():
    number_of_bots = 0
    list_of_bots = []
    while number_of_bots < 1 or number_of_bots > 5:
        number_of_bots = int(input("Enter a number between 1 and 5 to choose how many AI players to have: "))
    for i in range(number_of_bots):
        list_of_bots.append(Player(random.choice(bot_names)))
    return list_of_bots
    

#MAIN
if __name__ == '__main__':
    players = []
    players.append(Player(input("Enter your name: ")))
    players += addBots()
    for player in players:
        print(f"{player.name}'s hand is:")
        player.gen_dice_faces()
    
    



