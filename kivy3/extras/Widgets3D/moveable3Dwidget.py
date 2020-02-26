from kivy3.widgets.object3d_widget import Object3DWidget
from kivy3 import Object3D
from kivy.clock import Clock
import math

class Moveable3DWidget(Object3DWidget):
    def __init__(self, object3d, renderer, orbit_camera, axis=[1,1,1],  **kw):
        # Information needed: Orbit Camera:
        super(Moveable3DWidget, self).__init__(object3d, renderer)
        self.renderer = renderer
        self.camera = self.renderer.camera
        self.orbit = orbit_camera
        self.theta = 0
        self.phi = 0
        self.axis = axis
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
        # print("Object was touched up")
        if touch.grab_current is self:
            touch.ungrab(self)
        return True

    def on_touch_move(self, touch):
        #Function to override of what to do when touching objects.

        if touch.grab_current is self:
            self.update_cam_angles()
            self.object.pos.x -= 0.001 * (float(touch.dy)
                                       * math.cos(self.theta) * math.sin(self.phi)
                                       - float(touch.dx)
                                       * math.sin(self.theta)) * self.orbit.radius * abs(self.axis[0])

            self.object.pos.y += 0.001 * (float(touch.dx)
                                       * math.cos(self.theta)
                                       + float(touch.dy)
                                       * math.sin(self.theta) * math.sin(self.phi)) \
                                       * self.orbit.radius * abs(self.axis[1])
            # z
            self.object.pos.z -= 0.001 * -float(touch.dy) * math.cos(self.phi) * self.orbit.radius *  abs(self.axis[2])

            self.on_pos_change()
        return True

    def on_pos_change(self):
        """Override this function to recieve a callback on a position change.
"""
        pass
