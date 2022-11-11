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

    def __init__(self):
        ...

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



            
