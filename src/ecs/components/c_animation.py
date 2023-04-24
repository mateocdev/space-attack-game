
from typing import List


class CAnimation:
    def __init__(self, animations: dict):
        self.number_frames = animations['number_frames']
        self.animations_list: List[AnimationData] = []
        for anim in animations['list']:
            anim_data = AnimationData(
                anim['name'], anim['start'], anim['end'], anim['framerate'])
            self.animations_list.append(anim_data)

        self.curr_anim = 0
        self.current_animation_time = 0.0
        self.curr_frame = self.animations_list[self.curr_anim].start


class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float):
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate


def set_animation(c_a: CAnimation, anim_name: str):
    for i, anim in enumerate(c_a.animations_list):
        if anim.name == anim_name and c_a.curr_anim != i:
            c_a.curr_anim = i
            c_a.current_animation_time = 0.0
            c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
