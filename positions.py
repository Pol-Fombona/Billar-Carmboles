TABLE_WIDTH = 41.64
TABLE_LENGTH = 83.28
TABLE_HEIGHT = 0.5
MARGIN_WIDTH = 1
LEGS_HEIGHT = 500
LEGS_SIZE = 0.5
TABLE_PROF = (
    TABLE_HEIGHT / 2
)  # Aixo es la profunditat de la moqueta a l'interor de la taula
# Per a tenir la moqueta de la taula a 0,0,0 aquestes son les coordenades de la taula => (-MARGIN_WIDTH, -TABLE_PROF, -MARGIN_WIDTH)
TABLE_POSITION = (-MARGIN_WIDTH, -TABLE_PROF, -MARGIN_WIDTH)
LEG_1 = (TABLE_POSITION[0], TABLE_POSITION[1], TABLE_POSITION[2])
LEG_2 = (
    TABLE_POSITION[0] + TABLE_WIDTH + MARGIN_WIDTH,
    TABLE_POSITION[1],
    TABLE_POSITION[2],
)
LEG_3 = (
    TABLE_POSITION[0] + TABLE_WIDTH + MARGIN_WIDTH,
    TABLE_POSITION[1],
    TABLE_POSITION[2] + TABLE_LENGTH + MARGIN_WIDTH,
)
LEG_4 = (
    TABLE_POSITION[0],
    TABLE_POSITION[1],
    TABLE_POSITION[2] + TABLE_LENGTH + MARGIN_WIDTH,
)
TABLE_FLOOR = (
    TABLE_POSITION[0] + MARGIN_WIDTH,
    TABLE_POSITION[1] + TABLE_PROF,
    TABLE_POSITION[2] + +MARGIN_WIDTH,
)

### BALLS
SLICES = 20
STACKS = 20
RADIUS = 1
BALL_COLOR = (1, 0, 1)

# SubDivision ball colour
SDCOLOR1 = (1, 0, 0)
SDCOLOR2 = (1, 1, 0)
SDDEPTH = 4
