
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


def pause_manager(game):
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
                    modify_friction()
                    show_options()

                case 3:
                    show_ranking()
                    show_options()

                case 4:
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
    # Prints summary of the game and
    # updates ranking file

    print_onColored("#### Game Finished #### ")
    print("Played Time:", format_time(game.played_time))
    print("Score:", game.get_scores())
    print("\n")

    update_ranking(game)


def update_ranking(game):
    # Update ranking file

    ranking_data = pd.read_csv('results/ranking.csv')

    game_data = [(game.player1.name, game.player1.score),
                    (game.player2.name, game.player2.score)]
    
    game_data = pd.DataFrame(game_data, columns=["Player", "Score"])

    ranking_data = pd.concat([ranking_data, game_data], ignore_index=True)
    ranking_data = ranking_data.sort_values(by=["Score"], ascending=False)
    ranking_data = ranking_data.head(10)

    ranking_data.to_csv('results/ranking.csv', sep=",", index=False)

    return


def show_ranking():
    # Show ranking data in terminal

    ranking_data = pd.read_csv('results/ranking.csv')

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
    print("     2) Modify friction")
    print("     3) Show Ranking")
    print("     4) Exit game")