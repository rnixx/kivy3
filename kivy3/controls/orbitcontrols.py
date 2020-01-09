import math
from kivy.uix.boxlayout import BoxLayout


class OrbitControls(BoxLayout):
    def __init__(self, camera, radius, *args, **kw):
        super(OrbitControls, self).__init__(*args, **kw)
        self.camera = camera
        self.radius = radius
        self.phi = 90
        self.theta = 0
        self._touches = []
        self.camera.pos.z = radius
        self.look_at_pos = (0, 0.3, 0)
        camera.look_at(self.look_at_pos)

    def define_rotate_angle(self, touch):
        theta_angle = (touch.dx / self.width) * -360
        phi_angle = -1 * (touch.dy / self.height) * 360
        return phi_angle, theta_angle

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if 'button' in touch.profile:
                if touch.button == 'scrollup':
                    if self.radius > 0:
                        self.radius *= 1.1
                    self.update_after_scroll()
                elif touch.button == 'scrolldown':
                    if self.radius > 0:
                        self.radius *= 0.9
                    self.update_after_scroll()
                else:
                    touch.grab(self)
                    self._touches.append(touch)

    def on_touch_up(self, touch):
        touch.ungrab(self)
        if touch in self._touches:
            self._touches.remove(touch)
        self.camera.update()

    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                if touch.button == 'right':
                    self.do_translate(touch)
                else:
                    self.do_rotate(touch)
            elif len(self._touches) == 2:
                pass

    def do_translate(self, touch):
        scale = 0.001
        x = self.look_at_pos[0] # + (touch.dx * scale)
        y = self.look_at_pos[1] - (touch.dy * scale)
        z = self.look_at_pos[2]
        self.look_at_pos = (x, y, z)
        self.camera.look_at(self.look_at_pos)

    def do_rotate(self, touch):
        d_phi, d_theta = self.define_rotate_angle(touch)
        self.phi += d_phi
        self.theta += d_theta

        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        z += self.look_at_pos[2]
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        x += self.look_at_pos[0]
        y = self.radius * math.cos(_phi)
        y += self.look_at_pos[1]
        self.camera.pos = x, y, z
        self.camera.look_at(self.look_at_pos)

    def update_after_scroll(self):
        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        z += self.look_at_pos[2]
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        x += self.look_at_pos[0]
        y = self.radius * math.cos(_phi)
        y += self.look_at_pos[1]
        self.camera.pos = x, y, z
        self.camera.look_at(self.look_at_pos)