
import MovementManagement
import os
import datetime
from termcolor import colored
from tabulate import tabulate
import pandas as pd
from PickleManager import save_game_data_to_pickle


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
            
            if choice == 1:
                pause = False

            elif choice == 2:
                extended_options(game)
                show_options()

            elif choice == 3:
                show_controls()
                show_options()

            elif choice == 4:
                undo_turn(game)
                show_options()
            
            elif choice == 5:
                save_game(game)
                show_options()

            elif choice == 6:
                exit_game = True

            else:
                print_onColored("Invalid choice input", "on_red")

        except Exception as e:
            print(e)
            print_onColored("Invalid choice input", "on_red")

    clear_terminal()

    if exit_game:
        if not replay:
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

    if game.player1.score > game.player2.score:    
        print_colored("Winner: " + game.player1.name)

    elif game.player1.score < game.player2.score:
        print_colored("Winner: " + game.player2.name)

    else:
        print_colored("Draw")

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

            if choice == 1:
                show_ranking()
                show_extended_options()

            elif choice == 2:
                modify_friction()
                show_extended_options()

            elif choice == 3:
                modify_game_speed(game)
                show_extended_options()
            
            elif choice == 4:
                back = True

            else:
                print_onColored("Invalid choice input", "on_red")
        
        except:
            print_onColored("Invalaaaaaaaaaid choice input", "on_red")

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
    print_colored("\nCurrent friction: " + str(int(MovementManagement.friction*2000)))
    print("Friction accepts values in range [0,100] where 0 is no friction!")

    while True:
        friction = input("New friction value: ").strip()

        try: 
            friction = int(friction)
            
            if 0 <= friction <= 100:
                MovementManagement.friction = round(friction / 2000 , 2)
                print("Friction correctly updated")
                break

        except:
            print_onColored("Invalid value", "on_red")

    clear_terminal()

    return


def save_game(game, type = 1):

    if game.getTurnStatus() != "initial":
        clear_terminal()
        print_colored("Saving data is only available during turn start\n", "red")
        return

    # Game data to save
    status_data = [game.current_player.name, game.played_time, game.mode,
                    game.game_speed]
    status_columns = ["CurrentPlayer", "PlayedTime", "Mode", "GameSpeed"]

    # Player data to save
    p1 = game.player1
    p1_data = [p1.name, p1.ball.id, p1.score, p1.turn_count, p1.type]
    p1_columns = ["P1Name", "P1BallID", "P1Score", "P1Turn", "P1Type"]
    
    p2 = game.player2
    p2_data = [p2.name, p2.ball.id, p2.score,
                p2.turn_count, p2.type]
    p2_columns = ["P2Name", "P2BallID", "P2Score", "P2Turn", "P2Type"]

    # Sphere position data
    sphere_data = [game.spheres[i].pos for i in range(3)]
    sphere_columns = ["Sphere1Pos", "Sphere2Pos", "Sphere3Pos"]

    game_data = status_data + p1_data + p2_data + sphere_data
    game_columns = status_columns + p1_columns + p2_columns + sphere_columns

    game_df = pd.DataFrame([game_data], columns = game_columns)

    status = save_game_data_to_pickle(game_df,type)

    if status:
        clear_terminal()
        print_colored("Game saved successfully\n")

    else:
        clear_terminal()
        print_colored("Save data file could not be created\n", "red")
    
    return


def undo_turn(game):
    # Undo sphere movement in turn
    
    clear_terminal()

    if game.getTurnStatus() != "played":
        
        print_colored("Undo turn only available when player has made a move",
                         "red")
        return None

    
    for i in range(3):

        # Return sphere to initial position and velocity to zero
        #game.spheres[i].pos = game.spheres_turn_initial_position[i]
        game.spheres[i].velocity *= 0

        # Deletes collision record for this turn
    game.current_player.collision_record.clear()

        # Updates current player status
    game.current_player.played = False
    
    game.undo_turn = True
    print_colored("Undo Turn in process", "green")
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
    print("     4) Undo Turn")
    print("     5) Save Game")
    print("     6) Exit Game")


def show_extended_options():
    # Extended options menu

    print_onColored("#### Pause Menu ####")
    print("\nExtended Options:")
    print("     1) Show Ranking")
    print("     2) Modify Friction")
    print("     3) Modify Game Speed")
    print("     4) Return")