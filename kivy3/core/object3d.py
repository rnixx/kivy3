"""
The MIT License (MIT)

Copyright (c) 2013 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
Object3D class
=============

"""

from kivy.properties import (
    NumericProperty, ListProperty,
    ObjectProperty, AliasProperty
)
from kivy.graphics import (
    Scale, Rotate, PushMatrix, PopMatrix,
    Translate, UpdateNormalMatrix
)
from kivy.graphics.instructions import InstructionGroup
from kivy.event import EventDispatcher
from kivy.uix.relativelayout import RelativeLayout
from kivy3.math.vectors import Vector3
import numpy as np
import math
from scipy.spatial.transform import Rotation as R




class Object3D(EventDispatcher):
    """Base class for all 3D objects in rendered
    3D world.
    """

    def __init__(self, **kw):
        self.name = kw.pop('name', '')
        super(Object3D, self).__init__(**kw)
        self.children = list()
        self.parent = None

        self._mat_instruction = None

        self._scale = Scale(1., 1., 1.)
        self._position = Vector3(0, 0, 0)
        self._rotation = Vector3(0, 0, 0)
        self._position.set_change_cb(self.on_pos_changed)
        self._rotation.set_change_cb(self.on_angle_change)

        # general instructions
        self._pop_matrix = PopMatrix()
        self._push_matrix = PushMatrix()
        self._translate = Translate(*self._position)
        self._rotors = {
            "x": Rotate(self._rotation.x, 1, 0, 0),
            "y": Rotate(self._rotation.y, 0, 1, 0),
            "z": Rotate(self._rotation.z, 0, 0, 1),
        }

        self._instructions = InstructionGroup()

        #Vertices Object contating an approximate bound box of the object.
        self.bounding_vertices = []


    def add_object(self, *objs):
        #Add object after rendering has begun
        for obj in objs:
            self._add_child(obj)
            self._instructions.add(self._push_matrix)
            self._instructions.add(self._translate)
            self._instructions.add(self.scale)
            for rot in self._rotors.values():
                self._instructions.add(rot)
            self._instructions.add(obj.as_instructions())
            self._instructions.add(self._pop_matrix)


    def remove_object(self, object):
        instr = object.as_instructions()
        if instr in self._instructions.children:
            self._instructions.remove(instr)
        else:
            print("Object not found")
        pass

    def add(self, *objs):
        for obj in objs:
            self._add_child(obj)

    def _add_child(self, obj):
        self.children.append(obj)
        obj.parent = self

    def _set_position(self, val):
        if isinstance(val, Vector3):
            self._position = val
        else:
            self._position = Vector3(val)
        self._position.set_change_cb(self.on_pos_changed)

    def _get_position(self):
        return self._position

    position = AliasProperty(_get_position, _set_position)
    pos = position  # just shortcut

    def _set_rotation(self, val):
        if isinstance(val, Vector3):
            self._rotation = val
        else:
            self._rotation = Vector3(val)
        self._rotation.set_change_cb(self.on_angle_change)
        self._rotors["x"].angle = self._rotation.x
        self._rotors["y"].angle = self._rotation.y
        self._rotors["z"].angle = self._rotation.z

    def _get_rotation(self):
        return self._rotation

    rotation = AliasProperty(_get_rotation, _set_rotation)
    rot = rotation

    def _set_scale(self, val):
        if isinstance(val, Scale):
            self._scale = val
        else:
            self._scale = Scale(*val)

    def _get_scale(self):
        return self._scale

    scale = AliasProperty(_get_scale, _set_scale)

    def on_pos_changed(self, coord, v):
        """ Some coordinate was changed """
        self._translate.xyz = self._position

    def on_angle_change(self, axis, angle):
        self._rotors[axis].angle = angle

    def calculate_forward_kinematics(self, offset_xyz=[0, 0, 0], offset_rpy=[0, 0, 0], base=None):
        # Return [[xyz],[rpy]]
        xyz = offset_xyz
        offset_ypr = [offset_rpy[2],offset_rpy[1], offset_rpy[0]]
        ypr = R.from_euler('zyx', offset_ypr, degrees=True)

        # Iterate through objects down the list and apply transformation to find forward kinematics.
        current_object = self
        while current_object is not base:
            # print(current_object.name, self.pos, g_c)
            # Rotate.
            a = math.radians(current_object.rot[0])
            b = math.radians(current_object.rot[1])
            c = math.radians(current_object.rot[2])
            rx = np.array([[1, 0, 0],
                          [0, math.cos(a), -math.sin(a)],
                          [0, math.sin(a), math.cos(a)]])
            ry = np.array([[math.cos(b), 0, math.sin(b)],
                          [0, 1, 0],
                          [-math.sin(b), 0, math.cos(b)]])

            rz = np.array([[math.cos(c), -math.sin(c), 0],
                          [math.sin(c), math.cos(c), 0],
                          [0, 0, 1]])
            xyz = rx.dot(xyz)
            xyz = ry.dot(xyz)
            xyz = rz.dot(xyz)

            # Calculate transform
            # g_c = Vector3(g_c[0],g_c[1],g_c[2])
            cur_rot = [current_object.rot[2],current_object.rot[1],current_object.rot[0]]
            current_ypr = R.from_euler('zyx', cur_rot, degrees=True)

            ypr = current_ypr*ypr

            rpy=ypr.as_euler("zyx", degrees=True)
            rpy = [rpy[2],rpy[1],rpy[0]]

            xyz[0] += current_object.pos[0]
            xyz[1] += current_object.pos[1]
            xyz[2] += current_object.pos[2]
            current_object = current_object.parent

        return [xyz, rpy]

    def set_material(self, mat):
        # Override function to change the material of an object
        pass

    def get_material(self,mat):
        # Override to return the current material
        pass


    def as_instructions(self):
        """ Get instructions set for renderer """
        if not self._instructions.children:
            self._instructions.add(self._push_matrix)
            self._instructions.add(self._translate)
            self._instructions.add(self.scale)
            for rot in self._rotors.values():
                self._instructions.add(rot)
            self._instructions.add(UpdateNormalMatrix())
            for instr in self.custom_instructions():
                self._instructions.add(instr)
            for child in self.get_children_instructions():
                self._instructions.add(child)
            self._instructions.add(self._pop_matrix)
        return self._instructions

    def custom_instructions(self):
        """ Should be overriden in subclasses to provide some extra
            instructions
        """
        return []

    def get_children_instructions(self):
        for child in self.children:
            yield child.as_instructions()
