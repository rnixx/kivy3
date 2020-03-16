import math
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock

class OrbitControlWidget(RelativeLayout):
    def __init__(self, renderer, radius=1, theta=0, phi=0, target=(0, 0, 0), smooth_cam=True, **kw):
        super(OrbitControlWidget, self).__init__()
        # self.camera = renderer.camera
        self.renderer = renderer
        self.radius = radius
        self.target = list(target)
        # Tilt angle
        self.phi = phi
        # Yaw angle
        self.theta = theta
        self.activated = False
        self.light = renderer.main_light
        self.low_pass = smooth_cam

        #multitouch controls
        self.touch1 = None
        self.touch2 = None

        #Setpoint values
        self.sp_target = list(target)
        self.sp_radius = radius
        self.sp_phi = phi
        self.sp_theta = theta

        self.initial = [theta, phi, radius, target]
        if smooth_cam:
            Clock.schedule_interval(self.low_pass_cam, 1./30.)
        self.update_cam()

    def low_pass_cam(self, dt):
        alpha = dt/(0.03 +dt)

        self.radius = alpha * self.sp_radius + (1-alpha)*self.radius
        self.phi = alpha * self.sp_phi + (1 - alpha) * self.phi
        self.theta = alpha * self.sp_theta + (1 - alpha) * self.theta

        self.target[0] = alpha * self.sp_target[0] + (1 - alpha) * self.target[0]
        self.target[1] = alpha * self.sp_target[1] + (1 - alpha) * self.target[1]
        self.target[2] = alpha * self.sp_target[2] + (1 - alpha) * self.target[2]
        self.update_cam()
        #self.theta = alpha * self.sp_theta + (1 - alpha) * self.theta

    def set_home(self, theta, phi, radius, target):
        self.initial = [theta, phi, radius, target]

    def reset_cam(self):
        self.target = list(self.initial[3])
        self.theta = self.initial[0]
        self.phi = self.initial[1]
        self.radius = self.initial[2]

        self.sp_target = list(self.initial[3])
        self.sp_theta = self.initial[0]
        self.sp_phi = self.initial[1]
        self.sp_radius = self.initial[2]
        self.update_cam()


    def on_touch_down(self, touch):
        # print("Touch Down", touch)
        if self.collide_point(*touch.pos):
            if 'multitouch_sim' in touch.profile or 'button' not in touch.profile:
                if self.touch1 is None:
                    self.touch1 = touch
                    touch.grab(self)
                elif self.touch2 is None:
                    self.touch2 = touch
                    touch.grab(self)

            elif 'button' in touch.profile:
                if touch.button == 'left' or touch.button == 'right':
                    touch.grab(self)
                    self.activated = True
            return True




    def on_touch_up(self, touch):
        # print("Touch Up", touch)
        if self.collide_point(*touch.pos):
            if 'button' in touch.profile:
                if touch.button == 'scrollup':
                    self.sp_radius *= 1.1
                    if not self.low_pass:
                        self.update_cam()
                if touch.button == 'scrolldown':
                    self.sp_radius *= 0.9
                    if not self.low_pass:
                        self.update_cam()
                if touch.button == 'left' or touch.button == 'right':
                    touch.ungrab(self)
                    self.update_cam(instant=True)
                    self.activated = False
            if 'multitouch_sim' in touch.profile or 'button' not in touch.profile:
                if self.touch1 and self.touch1.id == touch.id:
                    self.touch1 = None
                    touch.ungrab(self)
                if self.touch2 and self.touch2.id == touch.id:
                    self.touch2 = None
                    touch.ungrab(self)
            return True

    def on_touch_move(self, touch):
        # print("Touch Move", touch)
        if self.collide_point(*touch.pos):

            if 'multitouch_sim' in touch.profile or 'button' not in touch.profile:
                if self.touch1 and touch.id == self.touch1.id:
                    self.touch1 = touch
                    if self.touch2 is None:
                        self.sp_theta += 0.01 * float(touch.dx)
                        self.sp_phi -= 0.01 * float(touch.dy)
                        self.sp_phi = min([self.sp_phi, math.pi / 2])
                        self.sp_phi = max([self.sp_phi, -math.pi / 2])
                        if not self.low_pass:
                            self.update_cam()
                    else:
                        # Update target
                        self.sp_target[0] += 0.001 * (float(touch.dy)
                                                      * math.cos(self.theta) * math.sin(self.phi)
                                                      - float(touch.dx)
                                                      * math.sin(self.theta)) \
                                             * self.radius
                        # y
                        self.sp_target[2] += 0.001 * (float(touch.dx)
                                                      * math.cos(self.theta)
                                                      + float(touch.dy)
                                                      * math.sin(self.theta) * math.sin(self.phi)) \
                                             * self.radius
                        # z
                        self.sp_target[1] += 0.001 * -float(touch.dy) * math.cos(self.phi) * self.radius
                        if not self.low_pass:
                            self.update_cam()

                        # Update radius

                        orig_dist = math.sqrt((self.touch1.px-self.touch2.px)**2 + (self.touch1.py-self.touch2.py)**2)
                        new_dist = math.sqrt(((self.touch1.px + touch.dx)-self.touch2.px)**2 + ((self.touch1.py+touch.dy) - self.touch2.py)**2)
                        factor = 1 + float(new_dist - orig_dist)*0.0025
                        self.sp_radius *= factor
                        if not self.low_pass:
                            self.update_cam()


                elif self.touch2 and touch.id == self.touch2.id:
                    self.touch2 = touch
                    if self.touch1 is None:
                        self.sp_theta += 0.01 * float(touch.dx)
                        self.sp_phi -= 0.01 * float(touch.dy)
                        self.sp_phi = min([self.sp_phi, math.pi / 2])
                        self.sp_phi = max([self.sp_phi, -math.pi / 2])
                        if not self.low_pass:
                            self.update_cam()
                    else:
                        # Update target
                        self.sp_target[0] += 0.001 * (float(touch.dy)
                                                      * math.cos(self.theta) * math.sin(self.phi)
                                                      - float(touch.dx)
                                                      * math.sin(self.theta)) \
                                             * self.radius
                        # y
                        self.sp_target[2] += 0.001 * (float(touch.dx)
                                                      * math.cos(self.theta)
                                                      + float(touch.dy)
                                                      * math.sin(self.theta) * math.sin(self.phi)) \
                                             * self.radius
                        # z
                        self.sp_target[1] += 0.001 * -float(touch.dy) * math.cos(self.phi) * self.radius
                        if not self.low_pass:
                            self.update_cam()

                        # Update radius

                        orig_dist = math.sqrt(
                            (self.touch1.px - self.touch2.px) ** 2 + (self.touch1.py - self.touch2.py) ** 2)
                        new_dist = math.sqrt((self.touch1.px - (self.touch2.px+touch.dx)) ** 2 + (
                                    self.touch1.py - (self.touch2.py+touch.dy)) ** 2)
                        factor = 1 + float(new_dist - orig_dist) * 0.0025
                        self.sp_radius *= factor
                        if not self.low_pass:
                            self.update_cam()





            if 'button' in touch.profile and self.activated:
                if touch.button == "left":
                    self.sp_theta += 0.01 * float(touch.dx)
                    self.sp_phi -= 0.01 * float(touch.dy)
                    self.sp_phi = min([self.sp_phi, math.pi/2])
                    self.sp_phi = max([self.sp_phi, -math.pi/2])
                    if not self.low_pass:
                        self.update_cam()
                if touch.button == "right":
                    #x
                    self.sp_target[0] += 0.001 * (float(touch.dy)
                                               * math.cos(self.theta) * math.sin(self.phi)
                                               - float(touch.dx)
                                               * math.sin(self.theta)) \
                                            * self.radius
                    # y
                    self.sp_target[2] += 0.001 * (float(touch.dx)
                                               * math.cos(self.theta)
                                               + float(touch.dy)
                                               * math.sin(self.theta) * math.sin(self.phi)) \
                                            * self.radius
                    # z
                    self.sp_target[1] += 0.001 * -float(touch.dy) * math.cos(self.phi) * self.radius
                    if not self.low_pass:
                        self.update_cam()
            return True

    def update_cam(self, instant=False):
        # self.camera.pos[2] = 1.2
        # print(self.camera.pos)
        # pass
        # self.camera.pos.x = 3.
        if not self.low_pass or instant:
            self.target = self.sp_target
            self.radius = self.sp_radius
            self.phi = self.sp_phi
            self.theta = self.sp_theta

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
