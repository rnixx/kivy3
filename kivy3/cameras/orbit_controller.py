import math
from kivy.uix.widget import Widget


class OrbitControl(Widget):
    def __init__(self, renderer, radius, **kw):
        super(OrbitControl, self).__init__(**kw)
        self.camera = renderer.camera
        self.radius = radius
        self.target = [0., 0., 0.]
        self.phi = 0.
        self.theta = 0.

        self.update_cam()
        pass

    def on_touch_down(self, touch):
        # print("Touch Down", touch)
        pass

    def on_touch_up(self, touch):
        # print("Touch Up", touch)
        if 'button' in touch.profile:
            if touch.button == 'scrollup':
                self.radius *= 1.1
                self.update_cam()
            if touch.button == 'scrolldown':
                self.radius *= 0.9
                self.update_cam()
        pass

    def on_touch_move(self, touch):
        # print("Touch Move", touch)
        if 'button' in touch.profile:
            if touch.button == "left":
                self.theta += 0.02 * float(touch.dx)
                self.phi -= 0.02 * float(touch.dy)
                self.phi = min([self.phi, math.pi/2])
                self.phi = max([self.phi, -math.pi/2])
                self.update_cam()
            if touch.button == "right":
                self.target[0] += 0.001 * (float(touch.dy)
                                           * math.cos(self.theta)
                                           - float(touch.dx)
                                           * math.sin(self.theta)) \
                                        * self.radius
                self.target[2] += 0.001 * (float(touch.dx)
                                           * math.cos(self.theta)
                                           + float(touch.dy)
                                           * math.sin(self.theta)) \
                                        * self.radius
                self.update_cam()

    def update_cam(self):
        # self.camera.pos[2] = 1.2
        # print(self.camera.pos)
        # pass
        # self.camera.pos.x = 3.
        self.camera.pos[0] = self.radius * math.cos(self.phi) \
                                         * math.cos(self.theta) \
                                         + self.target[0]
        self.camera.pos[2] = self.radius * math.cos(self.phi) \
                                         * math.sin(self.theta) \
                                         + self.target[2]
        self.camera.pos[1] = self.radius * math.sin(self.phi) + self.target[1]
        self.camera.look_at(self.target[0], self.target[1], self.target[2])
        return
