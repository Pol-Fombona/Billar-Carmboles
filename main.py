import pygame as pg
import pygame_menu as pg_menu
import moderngl as mgl
import time
import sys
import pandas as pd

from model import *
from FreeCamera import *
from mesh import Mesh
from scene import Scene
from MenuManager import pause_manager, progress_manager, format_time, game_ended

from Light import Light
from MovementManagement import checkCollisions
from GameManager import *
from SoundManager3D import *
from ScoreManager import *
from PickleManager import (save_game_record_to_pickle, clean_replay_data_file, 
                        load_replay_data)
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
        self.light = Light()
        self.light2 = Light(position=(0, 5, 100))
        self.mesh = Mesh(self)
        self.scene = Scene(self)

        self.delta_time = 0
        self.pause = False
        self.quit = False

        # Bird està repetida dues vegades correctament
        self.camera_modes = ["Bird", "Free", "Bird", "Sphere"]
        self.camera_mode_index = 0

        

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
    def __init__(self, win_size=(1280, 720)):

        self.game_started = False

        super().__init__(win_size)

        self.game = None
        self.save_game = False


    def check_events(self):
        if self.quit:
            self.mesh.destroy()
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


    def init_game_params(self,names = [], mode = None):
        # Aqui és on preguntarem nom dels jugador i mode que volen jugar
        
        player1 = Player(name = names[0], ball = self.scene.ball_objects[0])
        player2 = Player(name = names[1], ball = self.scene.ball_objects[1], type = mode)

        self.game = Game(player1, player2, self.scene.ball_objects)
        self.game.mode = FreeCarambole(max_turn=25, max_score=10)

        self.sound = SoundManager(self)
        self.sound.playSong()

        # Game history 
        # (contains: sphere1.pos, sphere2.pos, sphere3.pos, 
        #   p1.score, p2.score)
        self.game_record = [] 

    
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

    def start_game(self, names = [], mode = None):
        if not self.game_started:
            last_timestamp = time.time()
            shots_taken = 0

            while True and shots_taken < 2:

                self.check_events()

                if self.pause:
                    self.quit = pause_manager(self.game)
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
            # self.mesh.vao.destroy()
            self.scene = Scene(self)
            self.init_game_params(names, mode)

    
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

        last_timestamp = time.time()

        while True:

            self.check_events()

            if self.pause:
                self.quit = pause_manager(self.game)
                last_timestamp = self.unpause()

            else:

                self.camera.update(self.game.spheres)
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

                        if self.game.get_match_status():
                            # Mostrar guanyador
                            game_ended(self.game)
                            self.quit = True

                self.delta_time = self.clock.tick(self.game.game_speed)
                self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())

            self.record_frame_data()


class ReplayEngine(Engine):
    # Engine used when replaying a game

    def __init__(self, win_size=(1280, 720),replay_name=""):

        self.game_started = True
        
        super().__init__(win_size)

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

            if self.pause:
                    self.quit = pause_manager(self.game, replay=True)
                    last_timestamp = self.unpause()

            else:

                self.camera.update(self.game.spheres)
                self.render()
            
                self.delta_time = self.clock.tick(self.game.game_speed)
                self.game.played_time, last_timestamp = progress_manager(self.game.played_time, last_timestamp, time.time())
                
class Menu:
    def __init__(self):
        pg.init()
        myimage = pg_menu.baseimage.BaseImage(
        #image_path=pg_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
        image_path="MenuResources/Images/background.jpg",
        drawing_mode=pg_menu.baseimage.IMAGE_MODE_REPEAT_XY,
        )

        my_theme = pg_menu.Theme(
            #background_color=(176,224,230),
            title_bar_style = pg_menu.widgets.MENUBAR_STYLE_NONE,
            title_font_size=60,
            #title_font_color=(230,230,250),
            title_offset=(30,100),
            title_font = pg_menu.font.FONT_8BIT,
            background_color=myimage,
            #title_shadow=True,
            title_background_color=(4, 47, 126),
            widget_font=pg_menu.font.FONT_8BIT,
            widget_font_color = (0,0,0),
            widget_font_size = 60
        )
        self.surface = pg.display.set_mode(W_SIZE)
        #self.menu = pg_menu.Menu('Three-cushion billiards', W_SIZE[0]/1.5, W_SIZE[1]/1.5,
        #               theme=my_theme)
        self.menu = pg_menu.Menu('Three cushion billiards', W_SIZE[0], W_SIZE[1],
                       theme=my_theme)
        self.mode = None
        self.name = 'John Doe'
        self.name2 = 'Jane Fey'
        self.replays = [x for x in os.listdir("GameData/Replays")]
        self.on_init()
    
    def on_init(self):
        self.menu.clear()
        self.menu.add.button('Play', self.play)
        self.menu.add.button('View Replay', self.view_replay)
        self.menu.add.button('Quit', pg_menu.events.EXIT)
        self.menu.mainloop(self.surface)

    def set_name(self,name):
        self.name = name
    def set_name2(self,name):
        self.name2 = name
    def select_mode(self,value,mode):
        self.mode = mode   
    def play(self):
        self.mode = None
        self.menu.clear() 
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
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Back', self.play)

    def start_the_game(self):
        app = GraphicsEngine(win_size=W_SIZE)
        app.init_game_params(names = [self.name,self.name2],mode = self.mode)
        app.start_game(names = [self.name,self.name2], mode = self.mode)
        app.run()
    def view_replay(self):
        self.menu.clear()
        for x in self.replays:
            if x[-4:]==".zip":
                self.menu.add.button(x[:-4], self.start_replay,x)    
        self.menu.add.button('Back', self.on_init)
        
    def start_replay(self,file=""):
        app = ReplayEngine(win_size=W_SIZE,replay_name = file)
        app.init_game_params(names = [self.name,self.name2],mode = self.mode)
        app.run()



if __name__ == "__main__":
    Menu()
