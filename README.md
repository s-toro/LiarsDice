# Liar's Dice python game

Simulation of a Liar's dice game in Python.

## Rules of the Game:
The game is played by two or more player.
Each player starts with 5 dice in their hand.
Each player rolls their dice at the start of the round without showing them to their oponents.
The starting player makes the initial bid, the bid consists of a dice value and number of dice.
The bid represents the number of total dice with the particular value on the whole table.
Turns rotate among the other players.
Players must either raise the bet or call the previous bet.
- When raising the bet a player must bet either a higher quantaty of the same face as previous bet or it can be any quantaty of a higher face.
- When a players 'calls' the previous bet, all dice on the table are reviewed, if there are at least as many dice of the face value that was bid,
then the player who made that bid wins, otherwise the person that called the bet wins.
The losing player loses one die.
The game goes on until only one player has remaining dice in his hand, that player is declared the winner.

