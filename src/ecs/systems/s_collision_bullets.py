

import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_bullets(world: esper.World, explosion_info: dict):
    components_bullets = world.get_components(
        CSurface, CTransform, CTagBullet)
    components_enemies = world.get_components(
        CSurface, CTransform, CTagEnemy)
    for bullet_entity, (c_bull_s, c_bull_t, _) in components_bullets:
        bull_rect = CSurface.get_area_relative(
            c_bull_s.area, c_bull_t.pos)
        for enemy_entity, (c_ene_s, c_ene_t, _) in components_enemies:
            ene_rect = c_ene_s.area.copy()
            ene_rect.topleft = c_ene_t.pos
            if ene_rect.colliderect(bull_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, c_ene_t.pos, explosion_info)
