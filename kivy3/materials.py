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

from kivy.graphics import ChangeState

# Map for material attributes to shader
# uniform variables
MATERIAL_TO_SHADER_MAP = {
    "color": "Ka",
    "transparency": "Tr",
    "diffuse": "Kd",
    "specular": "Ks",
    "shininess": "Ns",  # specular coefficient
    "texture_ratio": "tex_ratio",
    "id_color": "id_color"
}


def set_attribute_to_uniform(attr_name, uniform_var):
    MATERIAL_TO_SHADER_MAP[attr_name] = uniform_var


class Material(ChangeState):

    def __init__(self, map=None, transparency=1.0, color=(1, 1, 1),
                 diffuse=(0, 0, 0), specular=(0, 0, 0),
                 shininess=10.0, texture_ratio=0.0, id_color=None, **kwargs):
        self.map = map
        super(Material, self).__init__()
        transparency = float(transparency)
        color = tuple(float(c) for c in color)
        diffuse = tuple(float(d) for d in diffuse)
        specular = tuple(float(s) for s in specular)
        shininess = float(shininess)
        texture_ratio = float(texture_ratio)

        if id_color == None:
            id_color = [0., 0., 0., 0.]
        else:
            id_color = list(id_color)
            id_color[0] = id_color[0]/255.
            id_color[1] = id_color[1]/255.
            id_color[2] = id_color[2]/255.
            id_color.append(1)
        id_color = tuple(id_color)

        # set attribute from locals
        for k, v in list(locals().items()):
            setattr(self, k, v)

    def clear_id(self):
        setattr(self,"id_color",(0,0,0,1))

    def __setattr__(self, k, v):
        if k in MATERIAL_TO_SHADER_MAP:
            uniform_var = MATERIAL_TO_SHADER_MAP[k]
            self.changes[uniform_var] = v
        else:
            if k == 'map' and v:
                self.changes['tex_ratio'] = 1.0
            if type(v) in [float, int, str, list]:
                self.changes[k] = v
        super(Material, self).__setattr__(k, v)
