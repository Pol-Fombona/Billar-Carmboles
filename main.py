import pygame as pg
import pygame_menu as pg_menu
import moderngl as mgl
import time
import sys
import pandas as pd

from model import *
from FreeCamera import *
from mesh import Mesh
from positions import *
from scene import Scene
from MenuManager import pause_manager, progress_manager, format_time, game_ended, save_game, undo_turn

from Light import Light
from MovementManagement import checkCollisions
import MoveCue
import MoveLine
from GameManager import *
from SoundManager3D import *
from ScoreManager import *
from PickleManager import (save_game_record_to_pickle, clean_replay_data_file, 
                        load_replay_data)
from IAManager import make_turn
from Metrics import create_graphs
import MovementManagement
import pandas as pd
import json



# Table measures
TABLE_WIDTH = 41.64
TABLE_LENGTH = 83.28
TABLE_HEIGHT = 0.5
MARGIN_WIDTH = 1
LEGS_HEIGHT = 500
TABLE_PROF = (
    TABLE_HEIGHT / 2
)  # Aixo es la profunditat de la moqueta a l'interor de la taula
# Per a tenir la moqueta de la taula a 0,0,0 aquestes son les coordenades de la taula => (-MARGIN_WIDTH, -TABLE_PROF, -MARGIN_WIDTH)
TABLE_POSITION = (-MARGIN_WIDTH, -TABLE_PROF, -MARGIN_WIDTH)
W_SIZE = (1280,720)

class Engine():
    # Base game engine

    def __init__(self, win_size=(1280, 720)) -> None:

        # Init pygame module
        #pg.init()

        self.WIN_SIZE = win_size
        
        # Set PyGame attributes
        self.set_pg_attributes()

        # Detect and use exixting opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST)

        self.clock = pg.time.Clock()

        self.camera = Camera(self)
        self.light = Light(position=LIGHT1_POSITION, Ia = 0.2, Id = 0, Is = 0)
        self.light2 = Light(position=LIGHT2_POSITION, Ia = 0)
        self.light3 = Light(position=LIGHT3_POSITION, Ia = 0)
        self.mesh = Mesh(self)
        self.scene = Scene(self)

        self.delta_time = 0
        self.pause = False
        self.quit = False

        # Bird està repetida dues vegades correctament
        self.camera_modes = ["Bird", "Free", "Bird", "Sphere"]
        self.camera_mode_index = 0

        self.game_data = [0]
        self.save_data = False

        

    def set_pg_attributes(self):

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute( pg.GL_CONTEXT_PROFILE_MASK, 
                                        pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)


    def get_info(self):
        # Returns info text (scores, time...) to show on top of window

        time_info = "Playing time: " + str(format_time(self.game.played_time))
        p1_score_info = "Scores: [" + self.game.player1.name + " - " + str(self.game.player1.score) + "; "
        p2_score_info = self.game.player2.name + " - " + str(self.game.player2.score) + "]"
        curent_player_info = "Current player: " + self.game.current_player.name
        camera_info = "Camera mode: " + self.camera_modes[self.camera_mode_index]
        
        info = (time_info + " | " + curent_player_info + " | " + p1_score_info + p2_score_info + " | " +
                camera_info + " | " )

        return info


    def render(self):
        # Default render

        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.render()
        pg.display.set_caption(self.get_info())
        pg.display.flip()


    def render_with_cue(self):
        # render with cue

        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.render_with_cue()
        pg.display.set_caption(self.get_info())
        pg.display.flip()

    
    def renderIA(self):
        pg.display.set_caption(self.get_info())
        #pg.display.flip()


    def unpause(self):
        # Returns current time to not include
        # paused time into the total playtime

        self.pause = False
        pg.event.clear()

        return time.time()


class GraphicsEngine(Engine):
    #def __init__(self, win_size=(1600, 900)):
    def __init__(self, win_size=(1280, 720),game_engine = None):

        self.game_started = False

        super().__init__(win_size)
        self.game_engine = game_engine
        self.game = None
        self.save_game = False
        self.shots_taken = 0

    def reload_params(self):
        # Set PyGame attributes
        self.set_pg_attributes()

        # Detect and use exixting opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST)

        self.camera = Camera(self)
        self.light = Light(position=LIGHT1_POSITION, Ia = 0.2, Id = 0, Is = 0)
        self.light2 = Light(position=LIGHT2_POSITION, Ia = 0)
        self.light3 = Light(position=LIGHT3_POSITION, Ia = 0)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.init_game_params(names = [self.game_engine.menu.name,self.game_engine.menu.name2],mode = self.game_engine.menu.mode,type=2,
        difficulty=self.game_engine.menu.difficulty)
        self.game.game_speed *= self.game_engine.menu.game_speed
        self.init_saved_game_params(type=2)
        #MoveCue.change_objective(self.scene.cue,self.game.current_player.ball)
        #MoveLine.change_objective(self.scene.line,self.game.current_player.ball)
        self.scene.cue.moving = True

    def game_save_frames_data_to_json(self):
        # Save frame data to json for metrics
        columns = ["PlayerName", "TurnStatus", "TurnCount", "Pos1", "Pos2", "Pos3"]
        self.game_data = self.game_data[1:]
        df = pd.DataFrame(self.game_data, columns=columns)
        create_graphs(df) # Create  metrics graphs


    def check_events(self):
        if self.quit:    
            
            self.mesh.destroy()
            self.sound.destroy()
            pg.quit()

            if self.save_game == True:
                self.save_game_record()
            sys.exit()

        for event in pg.event.get():

            if not self.pause:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.pause = True
        
                elif event.type == pg.KEYDOWN and event.key == pg.K_b:
                    self.camera_mode_index = (self.camera_mode_index + 1 ) % 4
                    self.camera.mode = self.camera_modes[self.camera_mode_index]
                    #self.camera.bird_camera = not self.camera.bird_camera

                elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    self.scene.ball_objects[0].velocity[0] += -0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    self.scene.ball_objects[0].velocity[0] += 0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                    self.scene.ball_objects[0].velocity[2] += -0.5
                elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                    self.scene.ball_objects[0].velocity[2] += 0.5

                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    ## Reset positions

                    for object in self.scene.ball_objects:
                        object.velocity *= 0
                        object.pos = object.initial_position

                elif (
                    event.type == pg.KEYDOWN
                    and event.key == pg.K_k
                    and self.scene.cue.state == "stop"
                ):
                    self.scene.cue.rotate_flag = True
                    self.scene.cue.rotate_direction = 1
                elif (
                    event.type == pg.KEYDOWN
                    and event.key == pg.K_j
                    and self.scene.cue.state == "stop"
                ):
                    self.scene.cue.rotate_flag = True
                    self.scene.cue.rotate_direction = -1
                elif event.type == pg.KEYUP and event.key == pg.K_k:
                    self.scene.cue.rotate_flag = False
                    self.scene.cue.rotate_direction = 0
                elif event.type == pg.KEYUP and event.key == pg.K_j:
                    self.scene.cue.rotate_flag = False
                    self.scene.cue.rotate_direction = 0
                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not self.scene.cue.rotate_flag:
                    self.scene.cue.state = "backward"
                elif event.type == pg.KEYUP and event.key == pg.K_SPACE and not self.scene.cue.rotate_flag:
                    self.scene.cue.state = "reset"

                if event.type == pg.KEYDOWN and event.key == pg.K_m:
                    if self.sound.song_playing:
                        self.sound.song_playing = False
                        self.sound.stopSong(0)
                    else:
                        self.sound.song_playing = True
                        self.sound.playSong()       


    def render_status_played(self):
        # Add collision checker to the render,
        # only when turn status is "played" because 
        # the spheres are moving

        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.render()
        checkCollisions(self.scene.ball_objects, self.sound, self.game.current_player)
        pg.display.set_caption(self.get_info())
        pg.display.flip()

    def render_status_played_game_starting(self):
        # Add collision checker to the render,
        # only when turn status is "played" because 
        # the spheres are moving

        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.render()
        valid = checkCollisions(self.scene.ball_objects, self.sound, self.game.current_player, self.game_started)
        pg.display.set_caption(self.get_info())
        pg.display.flip()

        return valid


    def init_game_params(self,names = [], mode = None, type = 1, difficulty = "Normal"):
        # Aqui és on preguntarem nom dels jugador i mode que volen jugar
        
        player1 = Player(name = names[0], ball = self.scene.ball_objects[0])
        player2 = Player(name = names[1], ball = self.scene.ball_objects[1], type = mode)

        self.game = Game(player1, player2, self.scene.ball_objects, difficulty=difficulty)
        if self.game_engine.menu.typeGame == "FreeCarambole":
            self.game.mode = FreeCarambole(max_score=self.game_engine.menu.max_score,
                                            max_turn=self.game_engine.menu.max_turn)
        elif self.game_engine.menu.typeGame == "ThreeWayCarambole":
            self.game.mode = ThreeWayCarambole(max_score=self.game_engine.menu.max_score,
                                                max_turn=self.game_engine.menu.max_turn)
       

        self.sound = SoundManager(self)
        self.sound.playSong(rolloff=1)

        # Game history 
        # (contains: sphere1.pos, sphere2.pos, sphere3.pos, 
        #   p1.score, p2.score)
        if type != 2:
            self.game_record = []

    def init_saved_game_params(self, save_data_path=None, type=1):
        # Load parameters and status from save data file

        #save_data_path = "GameData/SavedGames/2022-12-01_12-09-18.pkl"
        if type == 2:
            save_data_df = self.game_engine.menu.game_df
        else:
            save_data_df = pd.read_pickle(save_data_path) 
        
        # Game data
        self.game.played_time = int(save_data_df.iloc[0]["PlayedTime"])
        self.game.mode = save_data_df.iloc[0]["Mode"]
        if type != 2:
            self.game.game_speed = save_data_df.iloc[0]["GameSpeed"]

        # P1 Data
        self.game.player1.name = save_data_df.iloc[0]["P1Name"]
        self.game.player1.ball_id = save_data_df.iloc[0]["P1BallID"]
        self.game.player1.score = save_data_df.iloc[0]["P1Score"]
        self.game.player1.turn_count = save_data_df.iloc[0]["P1Turn"]
        self.game.player1.type = save_data_df.iloc[0]["P1Type"]

        # P2 Data
        self.game.player2.name = save_data_df.iloc[0]["P2Name"]
        self.game.player2.ball_id = save_data_df.iloc[0]["P2BallID"]
        self.game.player2.score = save_data_df.iloc[0]["P2Score"]
        self.game.player2.turn_count = save_data_df.iloc[0]["P2Turn"]
        self.game.player2.type = save_data_df.iloc[0]["P2Type"]

        if self.game.player1.name == save_data_df.iloc[0]["CurrentPlayer"]:
            self.game.current_player = self.game.player1
        else:
            self.game.current_player = self.game.player2

        # Sphere Data
        self.game.spheres[0].pos = save_data_df.iloc[0]["Sphere1Pos"]
        self.game.spheres[1].pos = save_data_df.iloc[0]["Sphere2Pos"]
        self.game.spheres[2].pos = save_data_df.iloc[0]["Sphere3Pos"]

        if type == 2:
            # Sphere Velocity
            self.game.current_player.played = save_data_df.iloc[0]["Played"]
            self.game.undo_turn = save_data_df.iloc[0]["Undo"]
            self.game.current_player.collision_record = save_data_df.iloc[0]["ColRec"]
            self.game.spheres_turn_initial_position[0] = save_data_df.iloc[0]["Sphere1PosInit"]
            self.game.spheres_turn_initial_position[1] = save_data_df.iloc[0]["Sphere2PosInit"]
            self.game.spheres_turn_initial_position[2] = save_data_df.iloc[0]["Sphere3PosInit"]
            self.game.spheres[0].velocity = save_data_df.iloc[0]["Sphere1Vel"]
            self.game.spheres[1].velocity = save_data_df.iloc[0]["Sphere2Vel"]
            self.game.spheres[2].velocity = save_data_df.iloc[0]["Sphere3Vel"]

        MoveCue.change_objective(self.scene.cue,self.game.current_player.ball)
        MoveLine.change_objective(self.scene.line,self.game.current_player.ball)

        return
    
    def record_frame_data(self):
        # Save current frame data

        frame_data = [self.scene.ball_objects[0].m_model, self.scene.ball_objects[1].m_model, self.scene.ball_objects[2].m_model,
                        self.game.player1.score, self.game.player2.score] # Faltaria afegir les dades del pal

        self.game_record.append(frame_data)

        return

    
    def save_game_record(self):
        # Saves game record as csv file

        columns=["Ball1Model", "Ball2Model", "Ball3Model", "P1Score", "P2Score"]
        game_data = pd.DataFrame(self.game_record, columns=columns)

        save_game_record_to_pickle(game_data)
        
        return

    def start_game(self, names = [], mode = None, difficulty = "Normal"):
        if self.game.player1.type != 'IA' and self.game.player2.type != 'IA':
            if not self.game_started:
                last_timestamp = time.time()
                self.shots_taken = 0
                shots = {'p1':True, 'p2': True}

                while True and self.shots_taken < 2:

                    self.check_events()

                    #if self.pause and self.game.getTurnStatus()=="initial":
                    if self.pause and self.game.current_player.type != "IA":
                        #self.quit = pause_manager(self.game)
                        self.game_engine.menu.display_menu_pause(start=True)
                        last_timestamp = self.unpause()

                    else:

                        self.camera.update(self.game.spheres)
                        self.sound.update()

                        match self.game.getTurnStatus() :

                            case "initial":
                                # Aqui és quan s'ha de mostrar el pal perquè el jugador encara no ha tirat
                                self.render_with_cue()

                                # Temporal per fer proves, per mirar si ha jugat comprovo si la velocitat
                                # de la seva bola no és zero. Aixo s'haura de canviar per a 
                                # modificar l'status de played quan s'allibera el pal, 
                                # es a dir quan s'ha fet el tir
                                if sum(abs(self.game.current_player.ball.velocity)) != 0:
                                    self.game.spheres_turn_initial_position = [self.game.spheres[i].pos for i in range(3)]
                                    self.game.current_player.played = True

                            case "played":
                                # Shot made but spheres are in movement
                                # TODO: Aqui no detecta correctament la variable game_started, no entenc del tot perque
                                valid = self.render_status_played_game_starting()
                            
                            case "ended":
                                # Shot made and all spheres have stopped
                                self.render()
                                scored = self.game.mode.update_score(self.game.current_player)
                                self.game.changeCurrentPlayer(scored)
                                self.shots_taken += 1



                        self.delta_time = self.clock.tick(self.game.game_speed)
                        self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())
                self.sound.stopSong(0)
                z_pos = self.game.get_sphere_position_z()
                min_z = 100
                player1 = None
                for index, z in enumerate(z_pos):
                    if z < min_z:
                        min_z = z
                        player1 = index

                # Aqui tenim el player 1 sera el que mes a prop tingui la pilota del 0 en el eix z, falta com decidir posarlo com a P1

                print(f'El jugador {names[index]} serà el jugador 1.')
        self.sound.stopSong(0)
        self.game_started = True
        # self.mesh.vao.destroy()
        self.scene = Scene(self)
        self.init_game_params(names, mode, difficulty)
        self.run()

    
    def simulate_IA_turn(self):
        # Simulates turn made by IA

        pg.display.set_caption("Processing IA turn...")
        turn_data = make_turn(self.scene.ball_objects, self.game)
        self.game.current_player.ball.update_velocity_values(turn_data)
        self.game.current_player.played = True
        pg.event.clear()

        return

    def procces_undo_turn(self):
        # Updates swiftly the position of the spheres
        # to the original turn position

        undo_completed = True

        for i in range(3):

            actual_pos = self.game.spheres[i].pos
            original_pos = self.game.spheres_turn_initial_position[i]

            # If actual pos is not the original
            if actual_pos != original_pos: 

                difference = (np.array(original_pos) - np.array(actual_pos))
                difference = np.around(difference / 20, 3)
        
                # If the difference between actual and pos is too small
                # Skip and say it is equal
                if sum(difference) == 0:
                    continue

                # Update sphere pos
                self.game.spheres[i].pos = tuple(np.array(actual_pos) + difference)
                undo_completed = False

        if undo_completed:
            self.game.undo_turn = False
            MoveCue.change_objective(self.scene.cue,self.game.current_player.ball)
            MoveLine.change_objective(self.scene.line,self.game.current_player.ball)

        return 

    def run(self):
        # Render the scene with all the spheres again

        last_timestamp = time.time()

        while True:

            self.check_events()

            if self.pause and self.game.current_player.type != "IA":
                #self.quit = pause_manager(self.game)
                self.game_engine.menu.display_menu_pause()
                last_timestamp = self.unpause()

            else:

                self.camera.update(self.game.spheres)
                self.sound.update()

                turn_status = self.game.getTurnStatus()

                if turn_status == "IA":
                    self.simulate_IA_turn()
                    self.save_game_data(turn_status)

                else:
                    if turn_status == "played":
                        # Shot made but spheres are in movement
                        self.render_status_played()
                        self.save_game_data(turn_status)

                    elif turn_status == "initial":
                        # Aqui és quan s'ha de mostrar el pal perquè el jugador encara no ha tirat
                        self.render_with_cue()
                        self.save_game_data(turn_status)
                        self.frame_count = 0

                        # If there is movement, player has made a shot
                        if sum(abs(self.game.current_player.ball.velocity)) != 0:
                            self.game.spheres_turn_initial_position = [self.game.spheres[i].pos for i in range(3)]
                            self.game.current_player.played = True
                     
                    elif turn_status == "ended":
                        # Shot made and all spheres have stopped
                        self.render()
                        scored = self.game.mode.update_score(self.game.current_player)
                        self.save_game_data(turn_status, scored)
                        self.game.changeCurrentPlayer(scored)

                        if self.game.get_match_status():
                            # Mostrar guanyador
                            game_ended(self.game)
                            self.quit = True

                    elif turn_status == "undo":
                        # Process undo of a turn
                        self.render()
                        self.procces_undo_turn()

                self.delta_time = self.clock.tick(self.game.game_speed)
                self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())

            self.record_frame_data()

    def save_game_data2(self, turn_status, scored=False):
        current_player = self.game.current_player
        if turn_status == 'IA':
            if current_player.name not in self.game_data.keys():
                self.game_data[current_player.name] = {}
            if current_player.turn_count not in self.game_data[current_player.name].keys():
                self.game_data[current_player.name][current_player.turn_count] = {}
        else:
            if turn_status == 'initial':
                if current_player.name not in self.game_data.keys():
                    self.game_data[current_player.name] = {}
                if current_player.turn_count not in self.game_data[current_player.name].keys():
                    self.game_data[current_player.name][current_player.turn_count] = {}
                potencia =  self.scene.cue.axis - self.scene.cue.pos
                self.game_data[current_player.name][current_player.turn_count]['initial'] = {
                    'sphere_position': [self.game.spheres[i].pos for i in range(3)],
                    'tir': {
                        'angle': self.scene.cue.angle,
                        'potencia': [potencia[0], potencia[1], potencia[2]],
                        'sphere': self.game.current_player.ball.pos
                    }
                }
            elif turn_status == 'played':
                if 'played' not in self.game_data[current_player.name][current_player.turn_count].keys():
                    self.game_data[current_player.name][current_player.turn_count]['played'] = {}
                self.game_data[current_player.name][current_player.turn_count]['played']['frame_'+str(self.frame_count)] = {
                    'sphere_position': [self.game.spheres[i].pos for i in range(3)]
                }

                self.frame_count += 1
            elif turn_status == 'ended':
                self.game_data[current_player.name][current_player.turn_count]['ended'] = {
                    'sphere_position': [self.game.spheres[i].pos for i in range(3)],
                    'scored': scored
                }


    def save_game_data(self, turn_status, score = None):

        data = [self.game.current_player.name, turn_status, self.game.current_player.turn_count,
                self.game.spheres[0].pos, self.game.spheres[1].pos, self.game.spheres[2].pos]

        if data != self.game_data[-1]:
            self.game_data.append(data)
            
        return


class ReplayEngine(Engine):
    # Engine used when replaying a game

    def __init__(self, win_size=(1280, 720),replay_name="", game_engine = None):

        self.game_started = True
        
        super().__init__(win_size)
        self.game_engine = game_engine

        # ReplayData
        self.replay_file = "GameData\\Replays\\" + replay_name
        self.replay_data = load_replay_data(self.replay_file)
        self.replay_data_iterator = self.replay_data.iterrows()


    def render(self):
        # Default render

        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.replay_render()
        pg.display.set_caption(self.get_info())
        pg.display.flip()

    def check_events(self):
        # Key events

        if self.quit:
            self.mesh.destroy()
            pg.quit()
            sys.exit()

        else:
            for event in pg.event.get():

                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    # Enter pause status
                    self.pause = True

                elif event.type == pg.KEYDOWN and event.key == pg.K_b:
                    self.camera_mode_index = (self.camera_mode_index + 1 ) % 2
                    self.camera.mode = self.camera_modes[self.camera_mode_index]

    def init_game_params(self, names = [], mode = None):
        # Aqui és on preguntarem nom dels jugador i mode que volen jugar
        
        player1 = Player(name = names[0], ball = self.scene.ball_objects[0])
        player2 = Player(name = names[1], ball = self.scene.ball_objects[1], type = mode)

        self.game = Game(player1, player2, self.scene.ball_objects)
        self.game.mode = FreeCarambole()

    
    def set_frame_data(self):
        # Use frame data to update object position and scores

        try:
            _, data = next(self.replay_data_iterator)

            self.scene.ball_objects[0].m_model = data["Ball1Model"]
            self.scene.ball_objects[1].m_model = data["Ball2Model"]
            self.scene.ball_objects[2].m_model = data["Ball3Model"]

            self.game.player1.score = data["P1Score"]
            self.game.player2.score = data["P2Score"]

        except:
            self.end_replay()

        return

    def end_replay(self):
        clean_replay_data_file(self.replay_file)
        print("\nReplay Ended")
        self.mesh.destroy()
        pg.quit()
        sys.exit()
        
    def run(self):
        
        last_timestamp = time.time()

        while True:

            self.set_frame_data()

            self.check_events()

            if self.pause and self.game.current_player.type != "IA":
                    #self.quit = pause_manager(self.game)
                    self.game_engine.menu.display_menu_pause()
                    last_timestamp = self.unpause()

            else:

                self.camera.update(self.game.spheres)
                self.render()
            
                self.delta_time = self.clock.tick(self.game.game_speed)
                self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())
                
class Menu:
    def __init__(self, Game):
        pg.init()
        self.myimage = pg_menu.baseimage.BaseImage(
        image_path="MenuResources/Images/background.jpg",
        drawing_mode=pg_menu.baseimage.IMAGE_MODE_REPEAT_XY,
        )

        self.my_theme = pg_menu.Theme(
            title_bar_style = pg_menu.widgets.MENUBAR_STYLE_NONE,
            title_font_size=60,
            title_offset=(30,100),
            title_font = pg_menu.font.FONT_8BIT,
            background_color=self.myimage,
            title_background_color=(4, 47, 126),
            widget_font=pg_menu.font.FONT_8BIT,
            widget_font_color = (139,0,0),
            widget_font_size = 50
        )
        self.mode = None
        self.name = 'John Doe'
        self.name2 = 'Jane Fey'
        self.replays = [x for x in os.listdir("GameData/Replays")]
        self.game_speed = 1
        self.game_engine = Game
        self.start=False
        self.difficulty = "Normal"
        self.game_df = None
        self.typeGame = "FreeCarambole"
        self.max_score = 10
        self.max_turn = 25

    def display_menu(self):
        self.surface = pg.display.set_mode(W_SIZE)
        self.menu = pg_menu.Menu('Three cushion billiards', W_SIZE[0], W_SIZE[1],
                       theme=self.my_theme)
        self.on_init()               

         
    def on_init(self):
        self.menu.clear()
        self.menu.add.button('Play', self.play)
        self.menu.add.button('Load Game', self.load_game)
        self.menu.add.button('View Replay', self.view_replay)
        self.menu.add.button('Show Ranking', self.show_ranking)
        self.menu.add.button('Options', self.select_options)
        self.menu.add.button('Quit', pg_menu.events.EXIT)
        self.menu.mainloop(self.surface)
       

    def set_name(self,name):
        self.name = name.upper()
    def set_name2(self,name):
        self.name2 = name.upper()
    def select_mode(self,value,mode):
        self.mode = mode   
    def select_typeGame(self,value,typeGame):
        self.typeGame = typeGame      
    def play(self):
        self.mode = None
        self.menu.clear() 
        self.menu.add.selector('Game Type ', [('Free', 'FreeCarambole'), ('ThreeWay', 'ThreeWayCarambole')], onchange=self.select_typeGame)
        self.menu.add.selector('Mode ', [('PvP', None), ('vs IA', "IA")], onchange=self.select_mode)
        self.menu.add.button('Next', self.set_params_game)
        self.menu.add.button('Back', self.on_init)
    def set_params_game(self):
        self.menu.clear() 
        if self.mode == None:
            self.menu.add.text_input('Name Player1:', default='John Doe',onchange=self.set_name)
            self.menu.add.text_input('Name Player2:', default='Jane Fey',onchange=self.set_name2)
        else:
            self.menu.add.text_input('Name Player1:', default='John Doe',onchange=self.set_name)
            self.name2 = "IA"
            self.menu.add.selector('Difficulty ', [('Normal', "Normal"),
            ("Hard", "Hard"),('Easy', "Easy")], onchange=self.select_difficulty)
        self.menu.add.button('Additional Options', self.set_add_options)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Back', self.play)

    def set_add_options(self):
        self.menu.clear() 
        self.menu.add.range_slider('Max turns', 25, (0, 100), 1,
                      rangeslider_id='range_slider1',
                      value_format=lambda x: str(int(x)), onchange=(self.apply_turns))
        self.menu.add.range_slider('Max score', 10, (0, 50), 1,
                      rangeslider_id='range_slider2',
                      value_format=lambda x: str(int(x)), onchange=(self.apply_score))
        self.menu.add.button('Back', self.set_params_game)  

    def apply_turns(self,turn):
        self.max_turn = turn
    def apply_score(self,score):
        self.max_score = score
    
    def select_difficulty(self,value,difficulty):
        self.difficulty = difficulty

    def load_game(self):
        self.menu.clear() 
        savedatas = [x for x in os.listdir("GameData/Savedatas")]
        if len(savedatas)>0:
            for x in savedatas:
                if x[-4:]==".pkl":
                    self.menu.add.button(x[:5], self.load_save,x)    
        self.menu.add.button('Back', self.on_init)

    def load_save(self,path):
        self.game_engine.app = GraphicsEngine(win_size=W_SIZE, game_engine = self.game_engine)
        self.game_engine.app.init_game_params(names = [self.name,self.name2],mode = self.mode)
        self.game_engine.app.init_saved_game_params(save_data_path="GameData/Savedatas/"+path)
        self.game_engine.app.run()   

    def view_replay(self):
        self.menu.clear()
        for x in self.replays:
            if x[-4:]==".zip":
                self.menu.add.button(x[:-4], self.start_replay,x)    
        self.menu.add.button('Back', self.on_init)
        
    def start_replay(self,file=""):
        app = ReplayEngine(win_size=W_SIZE,replay_name = file, game_engine = self.game_engine)
        app.init_game_params(names = [self.name,self.name2],mode = self.mode)
        app.run()

    def select_options(self):
        self.menu.clear()
        self.menu.add.button('Friction', self.change_friction)
        self.menu.add.button('Game Speed', self.change_speed)
        self.menu.add.button('Show Controls', self.show_controls)
        self.menu.add.button('Back', self.on_init)
    def change_friction(self):
        self.menu.clear()
        self.menu.add.range_slider('Choose a value', 1, (0, 100), 1,
                      rangeslider_id='range_slider',
                      value_format=lambda x: str(int(x)), onchange=(self.apply_friction))
        self.menu.add.button('Back', self.select_options)
    
    def apply_friction(self,friction = 1):
        MovementManagement.friction = round(friction / 100 , 2)

    def change_speed(self):
        self.menu.clear()
        self.menu.add.dropselect(
            title='Select Game Speed',
            items=[('x0,5', 0.5),
            ('x1', 1),
            ('x2',2),
            ('x4',4)],
            font_size=30,
            selection_option_font_size=34,
            onchange=(self.apply_speed)
        )
        self.menu.add.button('Back', self.select_options)  

    def apply_speed(self,value,speed=1): 
        self.game_speed = speed

    def show_ranking(self):
        self.menu.clear()
        rankings = pd.read_csv("GameData/Rankings/ranking.csv")
        table = self.menu.add.table(table_id='my_table', font_size=20)
        table.default_cell_padding = 5
        table.default_row_background_color = 'white'
        table.add_row(["Player","Score","Turns"],
            cell_font=pg_menu.font.FONT_OPEN_SANS_BOLD,cell_align=pg_menu.locals.ALIGN_CENTER)
        for index, row in rankings.iterrows():
            table.add_row([row["Player"], row["Score"], row["Turns"]],
                cell_font=pg_menu.font.FONT_OPEN_SANS_BOLD,cell_align=pg_menu.locals.ALIGN_CENTER)
        self.menu.add.button('Back', self.on_init,font_size=30) 

    def show_controls(self):
        self.menu.clear()
        self.menu.add.button('Back', self.select_options) 

    def start_the_game(self):
        self.game_engine.app = GraphicsEngine(win_size=W_SIZE, game_engine = self.game_engine)
        self.game_engine.app.init_game_params(names = [self.name,self.name2],mode = self.mode,difficulty = self.difficulty)
        #app.game_started = True
        self.game_engine.app.start_game(names = [self.name,self.name2], mode = self.mode)
        self.game_engine.app.game.game_speed *= self.game_speed
        #app.init_saved_game_params()
        self.game_engine.app.run()

    def display_menu_pause(self,start=False):
        self.start = start
        #save_game(self.game_engine.app.game,2)
        self.save_temporal_data()
        self.game_engine.app.sound.stopSong()
        self.my_theme = pg_menu.Theme(
            title_bar_style = pg_menu.widgets.MENUBAR_STYLE_NONE,
            title_font_size=60,
            title_offset=(350,100),
            title_font = pg_menu.font.FONT_8BIT,
            background_color=self.myimage,
            title_background_color=(4, 47, 126),
            widget_font=pg_menu.font.FONT_8BIT,
            widget_font_color = (139,0,0),
            widget_font_size = 60
        )
        self.surface = pg.display.set_mode(W_SIZE)
        self.menu = pg_menu.Menu('Pause Menu', W_SIZE[0], W_SIZE[1],
                       theme=self.my_theme)
        self.pause_menu() 

    def pause_menu(self):
        self.menu.clear()
        self.menu.add.button('Resume', self.resume_the_game)
        self.menu.add.button('Options', self.select_options_pause)
        self.menu.add.button('Save Game', self.saveGame)
        self.menu.add.button('Quit', self.quit_pause)
        self.menu.mainloop(self.surface)

    def resume_the_game(self):
        #self.start = False
        self.game_engine.app.pause = False
        self.game_engine.app.reload_params()
        if self.start:
            self.game_engine.app.start_game(names = [self.name,self.name2],mode = self.mode,difficulty = self.difficulty) 
        else:   
            self.game_engine.app.run()

    def quit_pause(self):
        if self.start:
            if self.game_engine.app != None:
                self.game_engine.app.mesh.destroy()
            pg_menu.events.EXIT
            sys.exit()    

        #self.game_engine.app.game_save_frames_data_to_json()
        self.menu.clear()
        self.menu.add.selector(title="Save Replay",
                               items=[("Yes",True),
                               ("No",False)],
                                font_size=50,
                                selection_color = (139,0,0),
                                onreturn=self.save_rep)
        

    def saveGame(self):
        self.menu.clear()
        self.menu.add.button('save1', self.select_save_space,1)
        self.menu.add.button('save2', self.select_save_space,2)
        self.menu.add.button('save3', self.select_save_space,3)
        self.menu.add.button('Back', self.pause_menu)
   
    def select_save_space(self,pos):
        self.menu.clear()
        save_game(game=self.game_engine.app.game,type=3,name_f="save"+str(pos))
        self.menu.add.label("Saved")
        self.menu.add.button('Back', self.saveGame)
  
    def save_rep(self,value,save_bool):
        if save_bool:
            self.game_engine.app.save_game_record()  
        self.menu.clear()
        self.menu.add.selector(title="Save Graphics",
                               items=[("Yes",True),
                               ("No",False)],
                                font_size=50,
                                selection_color = (139,0,0),
                                onreturn=self.save_graphics)
    
    def save_graphics(self,value,save_bool):
        if save_bool:
            self.game_engine.app.game_save_frames_data_to_json()   
        if self.game_engine.app != None:
            self.game_engine.app.mesh.destroy()
        pg_menu.events.EXIT
        sys.exit()

    def select_options_pause(self):
        self.menu.clear()
        self.menu.add.button('Friction', self.change_friction_pause)
        self.menu.add.button('Game Speed', self.change_speed_pause)
        self.menu.add.button('Undo Turn', self.undo_move)
        self.menu.add.button('Show Controls', self.show_controls_pause)
        self.menu.add.button('Back', self.pause_menu)
    
    def change_friction_pause(self):
        self.menu.clear()
        self.menu.add.range_slider('Choose a value', 1, (0, 100), 1,
                      rangeslider_id='range_slider',
                      value_format=lambda x: str(int(x)), onchange=(self.apply_friction))
        self.menu.add.button('Back', self.select_options_pause)
    
    def change_speed_pause(self):
        self.menu.clear()
        self.menu.add.dropselect(
            title='Select Game Speed',
            items=[('x0,5', 0.5),
            ('x1', 1),
            ('x2',2),
            ('x4',4)],
            font_size=30,
            selection_option_font_size=34,
            onchange=(self.apply_speed)
        )
        self.menu.add.button('Back', self.select_options_pause) 

    def undo_move(self):
        undo_turn(self.game_engine.app.game)
        self.save_temporal_data()

    def show_controls_pause(self):
        self.menu.clear()
        self.menu.add.button('Back', self.select_options_pause) 

    def save_temporal_data(self):
        game = self.game_engine.app.game
        # Game data to save
        status_data = [game.current_player.name, game.played_time, game.mode,
                        game.game_speed, game.current_player.played, game.undo_turn, 
                        game.current_player.collision_record]
        status_columns = ["CurrentPlayer", "PlayedTime", "Mode", "GameSpeed", 
                          "Played", "Undo", "ColRec"]

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

        sphere_initial_data = [game.spheres_turn_initial_position[i] for i in range(3)]
        sphere_initial_columns = ["Sphere1PosInit", "Sphere2PosInit", "Sphere3PosInit"]

        # Sphere velocity data
        sphere_data_vel = [game.spheres[i].velocity for i in range(3)]
        sphere_columns_vel = ["Sphere1Vel", "Sphere2Vel", "Sphere3Vel"]

        game_data = status_data + p1_data + p2_data + sphere_data + sphere_data_vel + sphere_initial_data
        game_columns = status_columns + p1_columns + p2_columns + sphere_columns + sphere_columns_vel + sphere_initial_columns

        self.game_df = pd.DataFrame([game_data], columns = game_columns)

class Game_Engine:
    def __init__(self):
        self.menu = Menu(self)
        self.app = None
        self.menu.display_menu()


if __name__ == "__main__":
    #Menu()
    Game_Engine()
