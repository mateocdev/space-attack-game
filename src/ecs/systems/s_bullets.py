

import pygame

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_bullets(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CSurface, CTransform, CTagBullet)
    scr_rect = screen.get_rect()
    for bullets_entity, (c_bull_s, c_bull_t, _) in components:
        s_bullet_rect = CSurface.get_area_relative(
            c_bull_s.area, c_bull_t.pos)
        if not scr_rect.colliderect(s_bullet_rect):
            world.delete_entity(bullets_entity)
