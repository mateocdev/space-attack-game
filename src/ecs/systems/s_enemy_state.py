

import esper
from src.ecs.components.c_animation import CAnimation,  set_animation
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_enemy_state(world: esper.World, player_entitity: int, enemy_state: dict):
    pl_t = world.component_for_entity(player_entitity, CTransform)
    components = world.get_components(
        CEnemyState, CAnimation, CTransform, CVelocity)
    for _, (c_st, c_a, c_t, c_v) in components:
        if c_st.state == EnemyState.IDLE:
            _do_enemy_idle(c_st, c_a, c_t, c_v, pl_t, enemy_state)
        elif c_st.state == EnemyState.HUNTING:
            _do_enemy_hunting(c_st, c_a, c_t, c_v, pl_t, enemy_state)
        elif c_st.state == EnemyState.EXPLODING:
            _do_enemy_exploding(c_st, c_a, c_t, c_v, pl_t, enemy_state)


def _do_enemy_idle(c_st: CEnemyState, c_a: CAnimation, c_t: CTransform, c_v: CVelocity, pl_t: CTransform, enemy_state: dict):
    set_animation(c_a, "IDLE")
    c_v.vel.x = 0
    c_v.vel.y = 0

    distance = c_t.pos.distance_to(pl_t.pos)
    if distance < enemy_state["distance_start_chase"]:
        c_st.state = EnemyState.HUNTING


def _do_enemy_hunting(c_st: CEnemyState, c_a: CAnimation, c_t: CTransform, c_v: CVelocity, pl_t: CTransform, enemy_state: dict):
    set_animation(c_a, "MOVE")

    c_v.vel = (pl_t.pos - c_t.pos).normalize() * enemy_state["velocity_chase"]
    distance = c_st.start_pos.distance_to(c_t.pos)
    if distance >= enemy_state["distance_stop_return"]:
        c_st.state = EnemyState.EXPLODING


def _do_enemy_exploding(c_st: CEnemyState, c_a: CAnimation, c_t: CTransform, c_v: CVelocity, pl_t: CTransform, enemy_state: dict):
    set_animation(c_a, "MOVE")
    c_v.vel = (c_st.start_pos - c_t.pos).normalize() * \
        enemy_state["velocity_return"]
    distance = c_st.start_pos.distance_to(c_t.pos)
    if distance <= 2:
        c_t.post.xy = c_st.start_pos.xy
        c_st.state = EnemyState.IDLE
