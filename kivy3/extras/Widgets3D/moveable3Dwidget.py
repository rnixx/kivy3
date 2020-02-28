from kivy3.widgets.object3d_widget import Object3DWidget
from kivy3 import Object3D
from kivy.clock import Clock
import math
import numpy as np

class Moveable3DWidget(Object3DWidget):
    def __init__(self, object3d, renderer, orbit_camera, axis=[1,1,1], base=None,  **kw):
        # Information needed: Orbit Camera:
        super(Moveable3DWidget, self).__init__(object3d, renderer)
        self.renderer = renderer
        self.camera = self.renderer.camera
        self.orbit = orbit_camera
        self.theta = 0
        self.phi = 0
        self.axis = axis
        self.base = base
        # self.theta = self.camera.rot[1]
        # self.phi = self.camera.rot[0]

        # Clock.schedule_interval(self.get_cam_angles, 0.05)

    def update_cam_angles(self, *dt):

        self.theta = self.orbit.theta
        self.phi = self.orbit.phi
        # print(self.theta, self.phi)

    def on_object_touch_down(self, touch):
        # Function to override of what to do when touching objects.
        # print("Object was touched down")

        touch.grab(self)
        return True

    def on_touch_up(self, touch):
        # Function to override of what to do when touching objects.
        if touch.grab_current is self:
            touch.ungrab(self)
        return True

    def on_touch_move(self, touch):
        #Function to override of what to do when touching objects.
        if self.base is None:
            phi_offset = 0;
            theta_offset = 0;
            a = 0.
            b = 0.
            c = 0.
        else:
            _, rpy = self.object.parent.calculate_forward_kinematics(base=self.base, offset_xyz=self.object.pos)


            a = -math.radians(rpy[0])
            b = -math.radians(rpy[1])
            c = -math.radians(rpy[2])
            # print(__name__, "on_touch_move()", a,b,c)
        # a = 0.
        # b = 0.
        # c = 0.
        # c = math.radians(45.)
        if touch.grab_current is self:
            self.update_cam_angles()
            dx = 0.001 * (-float(touch.dy)
                                       * math.cos(self.theta) * math.sin(self.phi)
                                       + float(touch.dx)
                                       * math.sin(self.theta)) * self.orbit.radius

            dy = 0.001 * (float(touch.dx)
                                       * math.cos(self.theta)
                                       + float(touch.dy)
                                       * math.sin(self.theta) * math.sin(self.phi)) \
                                       * self.orbit.radius
            # z
            dz = 0.001 * float(touch.dy) * math.cos(self.phi) * self.orbit.radius

            xyz = np.array([dx,dy,dz])
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

            self.object.pos.x += float(xyz[0])*  abs(self.axis[0])
            self.object.pos.y += float(xyz[1])*  abs(self.axis[1])
            self.object.pos.z += float(xyz[2])*  abs(self.axis[2])
            self.on_pos_change()
        return True

    def on_pos_change(self):
        """Override this function to recieve a callback on a position change.
"""
        pass
