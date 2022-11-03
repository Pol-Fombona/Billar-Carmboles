

class Player():
    def __init__(self, ball, name="CPU"):

        self.name = name
        self.score = 0
        self.ball = ball
        self.played = False

class Game():

    def __init__(self, player1, player2, spheres):

        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.spheres = spheres
        self.played_time = 0

    def get_scores(self):
        # Returns players scores
        return None

    def changeCurrentPlayer(self):
        # Changes active player

        self.current_player.played = False

        if self.current_player == self.player1:
            self.current_player = self.player2

        else:
            self.current_player = self.player1

    
    def checkTurnEnded(self):
        # Check if active player turn has ended

        if not self.current_player.played:
            return False

        for sphere in self.spheres:
            if sum(abs(sphere.velocity)) != 0:
                return False
        
        return True
    