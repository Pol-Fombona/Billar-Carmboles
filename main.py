import pygame as pg
import moderngl as mgl
import time
import sys
import pandas as pd

from model import *
from FreeCamera import *
from mesh import Mesh
from scene import Scene
from MenuManager import pause_manager, progress_manager, format_time

from Light import Light
from MovementManagement import checkCollisions
from GameManager import *
from SoundManager3D import *
from ScoreManager import *
from PickleManager import save_game_record_to_pickle
from IAManager import make_turn



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


class Engine():
    # Base game engine

    def __init__(self) -> None:
        pass

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
        
        info = time_info + " | " + curent_player_info + " | " + p1_score_info + p2_score_info + " | "
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
    def __init__(self, win_size=(1280, 720)):

        # Init pygame module
        pg.init()

        self.WIN_SIZE = win_size
        
        # Set PyGame attributes
        self.set_pg_attributes()

        # Detect and use exixting opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST)
        # self.ctx.viewport(0,0,self.WIN_SIZE[0]/2,self.WIN_SIZE[1]/2)
        self.clock = pg.time.Clock()
        # camera
        '''
        self.camera = Camera(
            self,
            position=(
                TABLE_POSITION[0] + TABLE_WIDTH + 1,
                TABLE_POSITION[1] + TABLE_HEIGHT + 1,
                TABLE_POSITION[2] + TABLE_LENGTH,
            ),
            table_information=(TABLE_POSITION, TABLE_WIDTH, TABLE_HEIGHT, TABLE_LENGTH),
        )
        '''
        self.game_started = True
        self.camera = Camera(self)
        # scene
        self.light = Light()
        self.light2 = Light(position=(0, 5, 100))
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.delta_time = 0
        self.pause = False
        self.quit = False
        self.game = None
        self.sound = SoundManager(self)
        self.sound.playSong()

        # Game history 
        # (contains: sphere1.pos, sphere2.pos, sphere3.pos, 
        #   p1.score, p2.score)
        self.game_record = [] 


    def check_events(self):
        if self.quit:
            self.mesh.destroy()
            pg.quit()
            self.save_game_record()
            sys.exit()

        for event in pg.event.get():

            if not self.pause:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.pause = True
        
                elif event.type == pg.KEYDOWN and event.key == pg.K_b:
                    self.camera.bird_camera = not self.camera.bird_camera

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


    def init_game_params(self):
        # Aqui és on preguntarem nom dels jugador i mode que volen jugar
        
        player1 = Player(name = "P1", ball = self.scene.ball_objects[0])
        player2 = Player(name = "P2", ball = self.scene.ball_objects[1])

        self.game = Game(player1, player2, self.scene.ball_objects)
        self.game.mode = FreeCarambole()

    
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

    def start_game(self):
        if not self.game_started:
            last_timestamp = time.time()
            shots_taken = 0

            while True and shots_taken < 2:

                self.check_events()

                if self.pause:
                    self.quit = pause_manager(self.game)
                    last_timestamp = self.unpause()

                else:

                    self.camera.update()
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
                                self.game.current_player.played = True

                        case "played":
                            # Shot made but spheres are in movement
                            self.render_status_played()
                        
                        case "ended":
                            # Shot made and all spheres have stopped
                            self.render()
                            scored = self.game.mode.update_score(self.game.current_player)
                            self.game.changeCurrentPlayer(scored)
                            shots_taken += 1


                    self.delta_time = self.clock.tick(self.game.game_speed)
                    self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())
            
            z_pos = self.game.get_sphere_position_z()
            min_z = 100
            player1 = None
            for index, z in enumerate(z_pos):
                if z < min_z:
                    min_z = z
                    player1 = index

            # Aqui tenim el player 1 sera el que mes a prop tingui la pilota del 0 en el eix z, falta com decidir posarlo com a P1

            self.game_started = True
    
    def simulate_IA_turn(self):
        # Simulates turn made by IA

        #self.camera.bird_camera = True # Bird camera is defaulted when IA plays
        #self.camera.update()
        #self.render()
        pg.display.set_caption("Processing IA turn...")
        turn_data = make_turn(50, self.scene.ball_objects, self.game)
        self.game.current_player.ball.velocity = turn_data
        self.game.current_player.played = True
        pg.event.clear()

        return

    def run(self):
        # Render the scene with all the spheres again
        self.scene = Scene(self)

        last_timestamp = time.time()
        record_game = False # Allow to save a record of the game 

        while True:

            self.check_events()

            if self.pause:
                self.quit = pause_manager(self.game)
                last_timestamp = self.unpause()

            else:

                self.camera.update()
                self.sound.update()

                turn_status = self.game.getTurnStatus()

                if turn_status == "IA":
                    self.simulate_IA_turn()

                else:
                    if turn_status == "initial":
                        # Aqui és quan s'ha de mostrar el pal perquè el jugador encara no ha tirat
                        self.render_with_cue()

                        # Temporal per fer proves, per mirar si ha jugat comprovo si la velocitat
                        # de la seva bola no és zero. Aixo s'haura de canviar per a 
                        # modificar l'status de played quan s'allibera el pal, 
                        # es a dir quan s'ha fet el tir
                        if sum(abs(self.game.current_player.ball.velocity)) != 0:
                            self.game.current_player.played = True


                    elif turn_status == "played":
                        # Shot made but spheres are in movement
                        self.render_status_played()
                    
                    elif turn_status == "ended":
                        # Shot made and all spheres have stopped
                        self.render()
                        scored = self.game.mode.update_score(self.game.current_player)
                        self.game.changeCurrentPlayer(scored)

                self.delta_time = self.clock.tick(self.game.game_speed)
                self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())

            if record_game:
                self.record_frame_data()


class ReplayEngine(Engine):
    # Engine used when replaying a game

    def __init__(self, win_size=(1280, 720)):
        
        # Init pygame module
        pg.init()

        self.WIN_SIZE = win_size
        
        # Set PyGame attributes
        self.set_pg_attributes()

        # Detect and use exixting opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST)

        self.clock = pg.time.Clock()
        self.camera = Camera(self)
        self.light = Light()
        self.light2 = Light(position=(0, 5, 100))
        self.mesh = Mesh(self)
        self.scene = Scene(self)

        self.delta_time = 0

        self.mode_bird_cam = True
        self.pause = False
        self.quit = False

        # ReplayData
        self.replay_data = pd.read_pickle("GameData\\Replays\\2022-11-19_19-37-08.pkl")
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
                    # Changes between bird and free cam mode
                    self.camera.bird_camera = not self.camera.bird_camera

    def init_game_params(self):
        # Aqui és on preguntarem nom dels jugador i mode que volen jugar
        
        player1 = Player(name = "P1", ball = self.scene.ball_objects[0])
        player2 = Player(name = "P2", ball = self.scene.ball_objects[1])

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
            print("\nReplay Ended")
            sys.exit()

        return


    def run(self):
        
        last_timestamp = time.time()

        while True:

            self.set_frame_data()

            self.check_events()

            if self.pause:
                    self.quit = pause_manager(self.game)
                    last_timestamp = self.unpause()

            else:

                self.camera.update()
                self.render()
            
                self.delta_time = self.clock.tick(self.game.game_speed)
                self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())
                



if __name__ == "__main__":

    app = GraphicsEngine()
    app.init_game_params()
    app.start_game()
    app.run()
