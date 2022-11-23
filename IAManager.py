# In charge of AI Player
import numpy as np
from random import choice, randrange
from MovementManagement import checkCollisions
import time

def make_turn(n_turns_simulated, ball_objects, game):
    # Loop to simulate n turns
    # If one turn gets a perfect score, return the velocity data of that simulation
    # Else it will return the one with max score that is not perfect score

    #print("\nIA start")

    # Velocity range [+-0.1, +-2]
    possible_values = [i for i in range(1, 21)]

    # Intervals de probabilitat [1-5] = 0.4, [6-10] = 0.3, [11-15] = 0.2, [16-20] = 0.1
    probabilities = [0.08, 0.08, 0.08, 0.08, 0.08, 
                    0.06, 0.06, 0.06, 0.06, 0.06,
                    0.04, 0.04, 0.04, 0.04, 0.04,
                    0.02, 0.02, 0.02, 0.02, 0.02]

    start = time.time()

    # Turn data: array de shape (n_turns, 3) that contains for each turn a random 3-component array velocity 
    #turn_data = np.array([[randrange(1,20)/10*choice([1,-1]), 0, randrange(5,20)/10*choice([-1,1])] 
    #                        for i in range(n_turns_simulated)])
    turn_data = np.array([[np.random.choice(possible_values, p=probabilities) / 10 * choice([1, -1]), 
                            0,
                            np.random.choice(possible_values, p=probabilities) / 10 * choice([1, -1])]
                            for i in range(n_turns_simulated)])

    # Order turn data in ascending mode
    turn_data = turn_data[np.argsort(abs(turn_data).sum(axis=1))]

    scores = []

    original_data = [(np.copy(sphere.m_model), sphere.pos) for sphere in ball_objects]

    for data in turn_data:
        score = simulate_turn(data, game)

        # Restore orignal data to sphere
        for i in range(len(ball_objects)):
            #ball_objects[i].m_model = original_data[i][0]
            ball_objects[i].pos = original_data[i][1]
        
        scores.append(score)

        # Deshabilitat
        # Aqui si un torn simulat retorna puntuació
        # Parem les simulacions i retorna la jugada bona
        # Amb probabilitat "x"
        '''
        if score == 1:
            # Probability to choose correct movement:
            p = np.random.choice([1,0], p=[0.9,0.1])
            if p == 1:
                print("Score fet")
                print("Time:", str(round(time.time()-start,3)))
                return data
    
        else:
            scores.append(score)
        '''

    #print("Simulation time:", str(round(time.time()-start,3)))

    if 1 in scores:
        return turn_data[scores.index(1)]

    elif 0.5 in scores:
        return turn_data[scores.index(0.5)]

    else:
        return turn_data[randrange(0,len(scores))]


def simulate_turn(data, game):
    # Simulate turns and returns the score

    game.current_player.ball.velocity = data.copy()

    # Loop until all sphere are still
    while True:

        for sphere in game.spheres:
            sphere.IA_update()
        
        checkCollisions(game.spheres, None, game.current_player, IA_mode=True)

        if not get_current_movement_data(game.spheres):
            break

    scored = game.mode.update_score_IA_simulation(game.current_player)

    return scored


def get_current_movement_data(ball_objects):
    # Returns True if there is a sphere in movement

    movement = sum([sum(abs(sphere.velocity)) for sphere in ball_objects])

    if movement == 0:
        return False

    else:
        return True


