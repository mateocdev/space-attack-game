import random
import pygame
import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = pygame.image.load(enemy_info["image"]).convert_alpha()
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy())


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    size = pygame.Vector2(player_info["size"]["x"],
                          player_info["size"]["y"])
    color = pygame.Color(player_info["color"]["r"],
                         player_info["color"]["g"],
                         player_info["color"]["b"])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size.x / 2),
                         player_lvl_info["position"]["y"] - (size.y / 2))
    vel = pygame.Vector2(0, 0)
    player_entity = create_square(world, size, pos, vel, color)
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_fire = world.create_entity()
    input_down = world.create_entity()

    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up,
                        CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down,
                        CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    """Adding support for mouse input and spacebar fire"""
    world.add_component(input_fire, CInputCommand(
        "PLAYER_SHOOT", pygame.K_SPACE))
    world.add_component(input_fire, CInputCommand(
        "PLAYER_SHOOT", pygame.BUTTON_LEFT))


def create_bullets(world: esper.World, player_size: pygame.Vector2, player_pos: pygame.Vector2, mouse_pos: pygame.Vector2, bullet_desc: dict):
    size = pygame.Vector2(bullet_desc["size"]["x"],
                          bullet_desc["size"]["y"])
    color = pygame.Color(bullet_desc["color"]["r"],
                         bullet_desc["color"]["g"],
                         bullet_desc["color"]["b"])
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2),
                         player_pos.y + (player_size[1] / 2))
    vel = mouse_pos - player_pos
    vel.scale_to_length(bullet_desc["velocity"])
    bullets_entity = create_square(world, size, pos, vel, color)
    world.add_component(bullets_entity, CTagBullet())
