from player import Player
from npc_player import NPCPlayer
from game import Game
#from classes import *

BOT_NAMES = [
    "Maccus",
    "Ratlin",
    "Penrod",
    "Jimmy Legs",
    "Koleniko",
    "Greenbeard",
    "Clanker",
    "Crash",
    "Hadras",
    "Wyvern",
]


if __name__ == "__main__":
    game = Game(BOT_NAMES)
    game.start_game()
