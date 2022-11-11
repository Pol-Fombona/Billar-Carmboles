

class Player():
    def __init__(self, ball, name="CPU"):

        self.name = name
        self.score = 0
        self.collision_record = [] 
        self.ball = ball
        self.played = False
        self.turn_count = 1
        

class Game():

    def __init__(self, player1, player2, spheres):

        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.spheres = spheres
        self.played_time = 0
        self.mode = ""

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

        if not self.current_player.played:
            return "initial"

        for sphere in self.spheres:
            if sum(abs(sphere.velocity)) != 0:
                return "played"
        
        return "ended"
    
