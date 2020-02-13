from scipy.spatial import Delaunay
import time
import threading
import math
from kivy.uix.relativelayout import RelativeLayout


class Object3DWidget(RelativeLayout):
    def __init__(self, object3d, renderer, scale=2., threading=True, **kw):
        super(Object3DWidget, self).__init__(**kw)
        self.object = object3d
        self.renderer = renderer
        self.points = []
        self.distance = 1
        #This should equal to the maximum distance from the center radius
        self.scale = scale
        #With Threading enabled, the touch event will not be consumed.
        #Without threading the touch object is consumed but depending on the geometry it can stall the program.
        self.threading = threading
        # Clock.schedule_once(self,update_centre_position, 0.2)
        # self.update_centre_position()
        self.touch_response = ["right", "left"]


    def on_touch_down(self, touch):
        if touch.button == "scrolldown" or touch.button == "scrollup":
            self.update_centre_position()
            #Clock.schedule_once(self.update_centre_position), 3)
        if self.collide_point(*touch.pos):
            if touch.button in self.touch_response:
                if self.threading:
                    threading.Thread(target=self.check_touched, args=(touch,)).start()
                else:
                    #Clock.schedule_once(partial(self.check_touched, touch), 3)
                    if self.touched(touch.pos):
                        self.on_object_touch(touch)
                        return True
        pass

    def on_object_touch(self,touch):
        #Function to override of what to do when touching objects.
        print("Object was touched")
        pass

    def update_centre_position(self):
        xyz, _ = self.object.calculate_forward_kinematics()
        _2d_point = self.renderer.camera.projection_matrix.project(
            xyz[0], xyz[1], xyz[2], self.renderer.camera.modelview_matrix,
            self.renderer.camera.projection_matrix,
            self.renderer._viewport.pos[0],
            self.renderer._viewport.pos[1],
            self.renderer._viewport.size[0],
            self.renderer._viewport.size[1])
        distance = math.sqrt((self.renderer.camera.pos[0]-xyz[0])**2 + (self.renderer.camera.pos[1]-xyz[1])**2 +(self.renderer.camera.pos[2]-xyz[2])**2)
        self.center = _2d_point[0:2]
        rad = 1./distance * self.renderer.size[1] * self.scale
        self.size = [rad, rad]
        #print(self.center, rad)

    def on_touch_up(self, touch):

        if touch.button == "left" or touch.button == "right":
            #Recalculate the xy centre_position:
            self.update_centre_position()
            #Calculate distance:


        # threading.Thread(target=self.calculate_points).start()

    def check_touched(self,touch, *dt):
        if self.touched(touch.pos):
            self.on_object_touch(touch)
        return

    def calculate_points(self):
        self.points=[]
        if len(self.object.bounding_vertices) < 3:
            return False
        #1. Produce an array of xyz coordinates.
        start_time = time.time()

        for _3d_point in self.object.bounding_vertices:
            xyz, _ = self.object.calculate_forward_kinematics(offset_xyz=_3d_point)
            _2d_point = self.renderer.camera.projection_matrix.project(
                xyz[0], xyz[1], xyz[2], self.renderer.camera.modelview_matrix,
                self.renderer.camera.projection_matrix,
                self.renderer._viewport.pos[0],
                self.renderer._viewport.pos[1],
                self.renderer._viewport.size[0],
                self.renderer._viewport.size[1])

            self.points.append((_2d_point[0], _2d_point[1]))
        elapsed_time = time.time() - start_time
        # print(elapsed_time)

    def touched(self, pos):
        self.calculate_points()

        if len(self.points)<3:
            return False
        if self.in_hull(pos, self.points):
            return True
        else:
            return False

    @staticmethod
    def in_hull(p, hull):
        """
        Test if points in `p` are in `hull`

        `p` should be a `NxK` coordinates of `N` points in `K` dimensions
        `hull` is either a scipy.spatial.Delaunay object or the `MxK` array of the
        coordinates of `M` points in `K`dimensions for which Delaunay triangulation
        will be computed
        """

        if not isinstance(hull,Delaunay):
            hull = Delaunay(hull)

        return hull.find_simplex(p)>=0
    pass
