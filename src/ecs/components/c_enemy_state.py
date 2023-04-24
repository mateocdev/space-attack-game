
from enum import Enum
import pygame


class CEnemyState:
    def __init__(self, start_pos: pygame.Vector2):
        self.state = EnemyState.IDLE
        self.start_pos = pygame.Vector2(start_pos.x, start_pos.y)


class EnemyState(Enum):
    IDLE = 0
    HUNTING = 1
    EXPLODING = 2
