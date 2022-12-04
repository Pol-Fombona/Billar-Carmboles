# Links interes
# https://www.youtube.com/watch?v=p6f486Kf6YE&list=PLNBRtqdsYrKQM49nOWn4SjP7O1q0CpjXN&index=4
# https://www.euroinnova.edu.es/blog/como-se-juega-al-billar-a-tres-bandas
# https://www.youtube.com/watch?v=-aVlH07wqbA
# https://www.youtube.com/watch?v=xOlRWK222Ag


class Caramboles():
    ...

class FreeCarambole():
    # To get a score, the player needs to collide with two different balls
    # There is no need to collide with the table and the order does not matter
    # Returns True if player scored, else False

    def __init__(self, max_score = None, max_turn = None):
        self.max_score = max_score
        self.max_turn = max_turn
        

    def update_score(self, player):

        sphere_collisioned = set()

        for coll_type, detail in player.collision_record:
            if coll_type == "Sphere":
                sphere_collisioned.add(detail)
                
        # Empty list for next turn
        player.collision_record.clear()

        if len(sphere_collisioned) >= 2:
            player.score += 1
            return True

        return False

    
    def update_score_IA_simulation(self, player):
        # Return 1 if scored, 0.5 if colision with one other sphere
        # O if no colision
        
        sphere_collisioned = set()

        for coll_type, detail in player.collision_record:
            if coll_type == "Sphere":
                sphere_collisioned.add(detail)
                
        # Empty list for next turn
        player.collision_record.clear()

        if len(sphere_collisioned) >= 2:
            return 1
            
        elif len(sphere_collisioned) == 1:
            return 0.5

        else:
            return 0


class ThreeWayCarambole():
    # To get a score, the player needs to collide with two different balls 
    # and three times with the table edge, does not matter it is the same edge
    # Returns True if player scored, else False

    def __init__(self, max_score = None, max_turn = None):
        self.max_score = max_score
        self.max_turn = max_turn

            
    def update_score(self, player):

        sphere_collisioned = set()
        edge_collisions = 0

        for coll_type, detail in player.collision_record:
            if coll_type == "Sphere":
                sphere_collisioned.add(detail)

            elif coll_type == "Edge":
                edge_collisions += 1 
                
        # Empty list for next turn
        player.collision_record.clear()
        if edge_collisions >= 3 and len(sphere_collisioned) >= 2:
            player.score += 1
            return True

        return False

    def update_score_IA_simulation(self, player):
        # Return 1 if scored, 0.5 if colision with one other sphere
        # O if no colision
        
        sphere_collisioned = set()
        edge_collisions = 0

        for coll_type, detail in player.collision_record:
            if coll_type == "Sphere":
                sphere_collisioned.add(detail)

            elif coll_type == "Edge":
                edge_collisions += 1
                
        # Empty list for next turn
        player.collision_record.clear()

        total_collisions = len(sphere_collisioned) + min(edge_collisions, 3)

        if total_collisions >= 5:
            return 1
            
        elif total_collisions == 0:
            return 0

        else:
            return 1 - (1/total_collisions)