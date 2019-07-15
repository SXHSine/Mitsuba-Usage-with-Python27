# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append('D:/ProgramFiles/Mitsuba 0.5.0/python/2.7')
os.environ['PATH'] = 'path-to-mitsuba-directory' + \
    os.pathsep + os.environ['PATH']

import mitsuba
import numpy as np
from mitsuba.core import *


class BasicPos:

    def __init__(self, position, forward):
        self.position = position
        self.forward = forward

    def __add__(self, other):
        pos_temp = BasicPos(Point(0, 0, 0), Point(0, 0, 0))
        for i in range(len(self.position)):
            pos_temp.position[i] = self.position[i] + other.position[i]
        for i in range(len(self.forward)):
            pos_temp.forward[i] = self.forward[i] + other.forward[i]
        return pos_temp

    def __sub__(self, other):
        pos_temp = BasicPos(Point(0, 0, 0), Point(0, 0, 0))
        for i in range(len(self.position)):
            pos_temp.position[i] = self.position[i] - other.position[i]
        for i in range(len(self.forward)):
            pos_temp.forward[i] = self.forward[i] - other.forward[i]
        return pos_temp


class BasicAnim:

    def __init__(self, start, end, frames):
        self.start = start
        self.end = end
        self.frames = frames


class BasicAnimList:

    def __init__(self):
        self.list_Anim = {}
        self.frame_now = 0

    def addAnimation(self, name, basicAnim):
        if self.list_Anim.has_key(name):
            self.list_Anim[name].append(basicAnim)
        else:
            self.list_Anim[name] = [basicAnim]

    def getLinMotion(self, basicAnim):
        pos_arr, for_arr = np.array(
            [[0.0] * 3] * basicAnim.frames), np.array([[0.0] * 3] * basicAnim.frames)
        for i in range(3):
            pos_linears, for_linears = np.linspace(
                start=basicAnim.start.position[i],
                stop=basicAnim.end.position[i],
                num=basicAnim.frames,
                endpoint=True
            ), np.linspace(
                start=basicAnim.start.forward[i],
                stop=basicAnim.end.forward[i],
                num=basicAnim.frames,
                endpoint=True
            )
            for j in range(basicAnim.frames):
                pos_arr[j][i] = pos_linears[j]
                for_arr[j][i] = for_linears[j]
        poses, fors = [], []
        for i in range(basicAnim.frames):
            poses.append(Point(pos_arr[i][0], pos_arr[i][1], pos_arr[i][2]))
            fors.append(Point(for_arr[i][0], for_arr[i][1], for_arr[i][2]))
        return {"poses": poses, "fors": fors}

    # return {"name": {"pos": [], "for": []}}
    def beginAnmiation(self):
        self.list_motion = {}
        for name in self.list_Anim.keys():
            while(len(self.list_Anim[name]) != 0):
                anim_now = self.list_Anim[name].pop(0)
                motion_now = self.getLinMotion(anim_now)
                if self.list_motion.has_key(name):
                    self.list_motion[name]['postions'].extend(
                        motion_now["poses"])
                    self.list_motion[name][
                        'forwards'].extend(motion_now["fors"])
                else:
                    self.list_motion[name] = {}
                    self.list_motion[name]['postions'] = motion_now["poses"]
                    self.list_motion[name]['forwards'] = motion_now["fors"]

    def update(self, name):
        postion_now, forward_now = None, None
        if self.list_motion.has_key(name):
            if len(self.list_motion[name]['postions']) > 1:
                postion_now = self.list_motion[name]['postions'].pop(0)
                forward_now = self.list_motion[name]['forwards'].pop(0)
            else:
                postion_now = self.list_motion[name]['postions'][0]
                forward_now = self.list_motion[name]['forwards'][0]
        return postion_now, forward_now


# USAGE
if __name__ == '__main__':
    USAGE()


def USAGE():
    bal = BasicAnimList()
    bp1 = BasicPos(p1, p1)
    bp2 = BasicPos(p2, p2)
    frames = 60
    ba = BasicAnim(bp1, bp2, frames)
    bal.addAnimation("cow", ba)
    bal.beginAnmiation()
    for i in range(frames + 10):
        print(bal.update("cow"))
