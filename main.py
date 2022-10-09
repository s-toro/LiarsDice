import random

from dice_graphics import DICE_FACES, DICE_HEIGHT


bot_names = ['Maccus', 'Ratlin', 'Penrod', 'Jimmy Legs', 'Koleniko', 'Greenbeard', 'Clanker', 'Crash', 'Hadras',
             'Wyvern']


    
#MAIN
def main():
    oGame = Game()
    while True:
        if oGame.get_next_player().is_human:

    #players = []
    #bet = [0, 6]
    #players.append(Player(input("Enter your name: ")))
    #players += addBots()
       #next_player  = random.choice(players)
    #game_continues = True
    #while game_continues:
        #if next_player.is_human:
            #print('Your hand is')
            #next_player.gen_dice_faces()
            #print(f"'There are {Player.total_die_count - next_player.num_of_dice} other die on the table")
        #print(f'{next_player.name} will start.')
        #bet = make_bet(bet, next_player)
        #break



if __name__ == '__main__':
    main()
    
    



