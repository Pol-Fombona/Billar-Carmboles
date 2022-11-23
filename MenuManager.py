
import MovementManagement
import os
import datetime
from termcolor import colored
from tabulate import tabulate
import pandas as pd


def progress_manager(played_time, last_timestamp, actual_timestamp):
    # Manage played time
    
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


def pause_manager(game, replay=False):
    # Manages menu options 

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
                    extended_options(game)
                    show_options()

                case 3:
                    show_controls()
                    show_options()

                case 4:
                    exit_game = True

                case _:
                    print_onColored("Invalid choice input", "on_red")

        except:
            print_onColored("Invalid choice input", "on_red")

    clear_terminal()

    if not replay and exit_game:
        game_ended(game)

    else:
        print_onColored("#### Game Resumed ####")

    return exit_game

def game_ended(game):
    # Prints summary of the game and
    # updates ranking file
    
    clear_terminal()

    print_onColored("#### Game Finished #### ")
    print("Played Time:", format_time(game.played_time))
    print("Score:", game.get_scores())
    print_colored("Winner: " + game.winner)
    print("\n")

    update_ranking(game)


def update_ranking(game):
    # Update ranking file

    ranking_data = pd.read_csv('GameData/Rankings/ranking.csv')

    game_data = [(game.player1.name, game.player1.score, game.player1.turn_count),
                    (game.player2.name, game.player2.score, game.player2.turn_count)]
    
    game_data = pd.DataFrame(game_data, columns=["Player", "Score", "Turns"])

    ranking_data = pd.concat([ranking_data, game_data], ignore_index=True)
    ranking_data = ranking_data.sort_values(by=["Score", "Turns"], ascending=[False, True])
    ranking_data = ranking_data.head(10)

    ranking_data.to_csv('GameData/Rankings/ranking.csv', sep=",", index=False)

    return


def extended_options(game):
    # More options menu manager

    clear_terminal()
    show_extended_options()

    back = False

    while not back:
        choice = input("\nEnter choice: ").strip()

        try:
            choice = int(choice)

            match choice:

                case 1:
                    show_ranking()
                    show_extended_options()

                case 2:
                    modify_friction()
                    show_extended_options()

                case 3:
                    modify_game_speed(game)
                    show_extended_options()

                case 4:
                    back = True

                case _:
                    print_onColored("Invalid choice input", "on_red")
        
        except:
            print_onColored("Invalid choice input", "on_red")

    clear_terminal()
    

def show_controls():
    # Show keybinds

    clear_terminal()
    print_colored("TODO")
    print("Press 1 to return")

    while True:
        
        option = input("\nEnter choice: ").strip()

        try:
            if (int(option)) == 1:
                break

            else:
                print_onColored("Invalid value", "on_red")

        except:
            print_onColored("Invalid value", "on_red")

    clear_terminal()
    return


def show_ranking():
    # Show ranking data in terminal

    ranking_data = pd.read_csv('GameData/Rankings/ranking.csv')

    clear_terminal()

    print(tabulate(ranking_data, headers = 'keys', tablefmt = 'psql'))
    print_colored("\nEnter '1' to return: ")

    while True:
        
        option = input("\nEnter choice: ").strip()

        try:
            if (int(option)) == 1:
                break
        
            else:
                print_onColored("Invalid value", "on_red")
        
        except:
            print_onColored("Invalid value", "on_red")

    clear_terminal()

    return 


def modify_game_speed(game):
    # Modifies game speed (fps)

    clear_terminal()

    accepted_values = [0.5, 1, 2, 4]

    print_onColored("#### Modify Game Speed ####")
    print_colored("\nCurrent speed: " + str(game.game_speed / 60))
    print("Accepted values are (" + str(accepted_values)[1:-1] + ")!")

    while True:
        new_speed = input("New Game Speed value: ").strip()

        try: 
            new_speed = float(new_speed)
            
            if new_speed in accepted_values:
                game.game_speed = int(60 * new_speed)
                break

            else:
                print_onColored("Invalid value", "on_red")

        except:
            print_onColored("Invalid value", "on_red")

    clear_terminal()

    return


def modify_friction():
    # Updates friction value by input
     
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
    # Clears terminal (linux & windows)

    os.system('cls' if os.name=='nt' else 'clear')


def print_onColored(text, color="on_green"):
    # Print text with highlighted colour

    print(colored(text, on_color = color))


def print_colored(text, color="green"):
    # Print text with colored letters

    print(colored(text, color))


def show_options():
    # Prints menu options 

    print_onColored("#### Pause Menu ####")
    print("\nOptions:")
    print("     1) Resume game")
    print("     2) More Options")
    print("     3) Show Controls")
    print("     4) Exit Game")


def show_extended_options():
    # Extended options menu

    print_onColored("#### Pause Menu ####")
    print("\nExtended Options:")
    print("     1) Show Ranking")
    print("     2) Modify Friction")
    print("     3) Modify Game Speed")
    print("     4) Return")