from random import randint
print('Welcome to guess the number made by Joseph')
print('='* 50)
player_name1 = input('Player 1 what is your name?')
print('=' * 50)
player_name2 = input('Player 2 what is your name?')

class Player:
    def __init__(self, name):
        self.name = name 
    
    def get_choice(self):
        return  int(input('Please input a number, {}.'.format(self.name)))


player1 = Player(player_name1)
player2 = Player(player_name2)

correct_answer = randint(0, 9)
player1_answer = player1.get_choice() 
player2_answer = player2.get_choice()

def play_game():
  if player2_answer == correct_answer and  player1_answer == correct_answer:
     print(f'Both {player1} and {player2} guessed correctly.')

  elif player1_answer != correct_answer and player1_answer == correct_answer:
     print(f'{player2}, guessed correctly.')

  elif player1_answer == correct_answer and player2_answer != correct_answer:
     print(f'{player1}, guessed correctly.')
    
  else:
     print('Both players guessed incorrectly.')
  pass 
 



rounds_played = 0


# Ask player
num_rounds = int(input("How many rounds do you want to play? "))

for i in range(num_rounds):
    print(f"\n--- Round {i + 1} ---")
    play_game()








    