import math
from kivy.uix.widget import Widget


class OrbitControlWidget(Widget):
    def __init__(self, renderer, radius, **kw):
        super(OrbitControlWidget, self).__init__()
        # self.camera = renderer.camera
        self.renderer = renderer
        self.radius = radius
        self.target = [0., 0., 0.]
        # Tilt angle
        self.phi = 0.
        # Yaw angle
        self.theta = 0.
        self.activated = False
        self.light = renderer.main_light


        self.update_cam()
        pass

    def on_touch_down(self, touch):
        # print("Touch Down", touch)
        if 'button' in touch.profile:
            if touch.button == 'left' or touch.button == 'right':
                touch.grab(self)
                self.activated = True

        return True

    def on_touch_up(self, touch):
        # print("Touch Up", touch)
        if 'button' in touch.profile:
            if touch.button == 'scrollup':
                self.radius *= 1.1
                self.update_cam()
            if touch.button == 'scrolldown':
                self.radius *= 0.9
                self.update_cam()
            if touch.button == 'left' or touch.button == 'right':
                touch.ungrab(self)
                self.activated = False

        return True

    def on_touch_move(self, touch):
        # print("Touch Move", touch)
        if 'button' in touch.profile and self.activated:
            if touch.button == "left":
                self.theta += 0.01 * float(touch.dx)
                self.phi -= 0.01 * float(touch.dy)
                self.phi = min([self.phi, math.pi/2])
                self.phi = max([self.phi, -math.pi/2])
                self.update_cam()
            if touch.button == "right":
                #x
                self.target[0] += 0.001 * (float(touch.dy)
                                           * math.cos(self.theta) * math.sin(self.phi)
                                           - float(touch.dx)
                                           * math.sin(self.theta)) \
                                        * self.radius
                # y
                self.target[2] += 0.001 * (float(touch.dx)
                                           * math.cos(self.theta)
                                           + float(touch.dy)
                                           * math.sin(self.theta) * math.sin(self.phi)) \
                                        * self.radius
                # z
                self.target[1] += 0.001 * -float(touch.dy) * math.cos(self.phi) * self.radius
                self.update_cam()
        return True

    def update_cam(self):
        # self.camera.pos[2] = 1.2
        # print(self.camera.pos)
        # pass
        # self.camera.pos.x = 3.
        if self.renderer.camera is not None:

            self.renderer.camera.pos[0] = self.radius * math.cos(self.phi) \
                                             * math.cos(self.theta) \
                                             + self.target[0]
            self.renderer.camera.pos[2] = self.radius * math.cos(self.phi) \
                                             * math.sin(self.theta) \
                                             + self.target[2]
            self.renderer.camera.pos[1] = self.radius * math.sin(self.phi) + self.target[1]
            self.renderer.camera.look_at(self.target[0], self.target[1], self.target[2])

            # self.light.pos_x = -self.camera.pos[0]
            # self.light.pos_y = -self.camera.pos[1]
            # self.light.pos_z = -self.camera.pos[2]
        return
