

class Player():
    def __init__(self, ball, name="CPU", type = None):

        self.name = name
        self.score = 0
        self.collision_record = [] 
        self.ball = ball
        self.ball_id = ball.id
        self.played = False
        self.turn_count = 1
        self.type = type
        

class Game():

    def __init__(self, player1, player2, spheres):

        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.spheres = spheres
        self.played_time = 0
        self.mode = None
        self.game_speed = 60 # FPS

    def get_scores(self):
        # Returns players scores in str format

        scores = "[ {0}: {1} --- {2}: {3} ]"
        scores = scores.format(self.player1.name, self.player1.score,
                                self.player2.name, self.player2.score)
        return scores

    def changeCurrentPlayer(self, scored):
        # Changes active player only
        # If the current player has scored
        # it keeps playing

        self.current_player.played = False

        if not scored:
            
            self.current_player.turn_count += 1

            if self.current_player == self.player1:
                self.current_player = self.player2

            else:
                self.current_player = self.player1

        return

    
    def getTurnStatus(self):
        # Returns status:
        #   - "initial" = player has not made a shot yet
        #   - "played"  = player has made a shoty and spheres are 
        #                 still in movement
        #   - "ended"   = turn has ended
        #   - "IA"      = IA turn simulation in progress

        if self.current_player.type == "IA" and not self.current_player.played:
            return "IA"

        elif not self.current_player.played:
            return "initial"

        for sphere in self.spheres:
            if sum(abs(sphere.velocity)) != 0:
                return "played"
        
        return "ended"

    def get_sphere_position_z(self):
        z_pos = []
        for sphere in self.spheres:
            if sphere.id != 3:
                z_pos.append(sphere.pos[2])

        return z_pos
    

    def get_match_status(self):
        # Returns True if match has ended

        max_turn = self.mode.max_turn 
        max_score = self.mode.max_score

        # Match ended because turn oount equals limit in mode
        if max_turn != None:
            if self.player1.turn_count == self.player2.turn_count == max_turn:
                return True

        if max_score != None:
            if self.player1.score == max_score or self.player2.score == max_score:
                return True

        return False