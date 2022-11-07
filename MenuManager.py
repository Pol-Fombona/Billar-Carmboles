
import MovementManagement
import os
import datetime
from termcolor import colored
import time


def progress_manager(played_time, last_timestamp, actual_timestamp):
    
    elapsed_time = actual_timestamp - last_timestamp

    if elapsed_time >= 1: # Més d'un segons

        played_time += int(elapsed_time)
        '''
        clear_terminal()
        print_onColored("#### Game in Progress ####")
        formatted_time = format_time(played_time)
        print("Playing time:", formatted_time)
        '''

        return played_time, actual_timestamp

    else:
        return played_time, last_timestamp


def format_time(time):
    # Returns total time played in format ("hh:mm:ss")

    return datetime.timedelta(seconds=time)


def pause_manager(game):

    pause = True
    exit_game = False

    clear_terminal()
    show_options()

    while pause and not exit_game:
        
        choice = input("\nEnter choice: ").strip()

        try:
            choice = int(choice)
            
            match choice:
                case 1:
                    pause = False

                case 2:
                    modify_friction()
                    show_options()

                case 3:
                    exit_game = True

                case _:
                    print_onColored("Invalid choice input", "on_red")

        except:
            print_onColored("Invalid choice input", "on_red")

    clear_terminal()

    if exit_game:
        game_ended(game)

    return exit_game

def game_ended(game):
    print_onColored("#### Game Finalished #### ")
    print("Played Time:", format_time(game.played_time))
    print("Score:", game.get_scores())
    print("\n")

def modify_friction():

    clear_terminal()
    
    print_onColored("#### Modify Friction ####")
    print_colored("\nCurrent friction: " + str(int(MovementManagement.friction*100)))
    print("Friction accepts values in range [0,100] where 0 is no friction!")

    while True:
        friction = input("New friction value: ").strip()

        try: 
            friction = int(friction)
            
            if 0 <= friction <= 100:
                MovementManagement.friction = round(friction / 100 , 2)
                print("Friction correctly updated")
                break

        except:
            print_onColored("Invalid value", "on_red")

    clear_terminal()
    return


def clear_terminal():
    os.system('cls' if os.name=='nt' else 'clear')


def print_onColored(text, color="on_green"):
    print(colored(text, on_color = color))

def print_colored(text, color="green"):
    print(colored(text, color))

def show_options():
    print_onColored("#### Pause Menu ####")
    print("\nOptions:")
    print("     1) Resume game")
    print("     2) Modify friction")
    print("     3) Exit game")