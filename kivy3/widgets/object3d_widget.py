from scipy.spatial import Delaunay
import time
import threading
import math
from kivy.uix.relativelayout import RelativeLayout


class Object3DWidget(RelativeLayout):
    def __init__(self, object3d, renderer, **kw):
        super(Object3DWidget, self).__init__(**kw)
        self.object = object3d
        self.renderer = renderer
        self.points = []
        #This should equal to the maximum distance from the center radius
        #With Threading enabled, the touch event will not be consumed.
        #Without threading the touch object is consumed but depending on the geometry it can stall the program.
        # Clock.schedule_once(self,update_centre_position, 0.2)
        # self.update_centre_position()



    def on_object_touch_down(self,touch):
        #Function to override of what to do when touching objects.
        print("Object was touched down")
        pass

    def on_object_touch_up(self,touch):
        #Function to override of what to do when touching objects.
        print("Object was touched up")
        pass

    def on_object_touch_move(self,touch):
        #Function to override of what to do when touching objects.
        print("Object was touched move")
        pass

    def get_centre_position(self):
        xyz, _ = self.object.calculate_forward_kinematics()
        _2d_point = self.renderer.camera.projection_matrix.project(
            xyz[0], xyz[1], xyz[2], self.renderer.camera.modelview_matrix,
            self.renderer.camera.projection_matrix,
            self.renderer._viewport.pos[0],
            self.renderer._viewport.pos[1],
            self.renderer._viewport.size[0],
            self.renderer._viewport.size[1])
        # distance = math.sqrt((self.renderer.camera.pos[0]-xyz[0])**2 + (self.renderer.camera.pos[1]-xyz[1])**2 +(self.renderer.camera.pos[2]-xyz[2])**2)
        # self.center = _2d_point[0:2]
        # rad = 1./distance * self.renderer.size[1] * self.scale
        # self.size = [rad, rad]
        #print(self.center, rad)
        return _2d_point[0:2]
