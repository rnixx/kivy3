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
from kivy3 import Vector3
from kivy3.core.geometry import Geometry
from kivy3.core.face3 import Face3
from kivy3.core.line2 import Line2


class GridGeometry(Geometry):
    """
        Generate a grid on xy plane centered about origin.
        To create grid on another plane, use this geometry
        in a Lines() object and rotate/translate the mesh.

    """
    def __init__(self, size=(10, 10), spacing=1, **kw):
        """
        :param size: Size of grid. Tuple (width, length)
        :param spacing: Distance between lines
        """
        name = kw.pop('name', '')
        super(GridGeometry, self).__init__(name)

        self.size = size
        self.spacing = spacing
        self._build_grid()

    def _build_grid(self):
        axes = 2
        v_idx = 0
        for axis in range(axes):
            # number of lines to draw
            num_lines = int(self.size[axis]/self.spacing) + 1

            for line_idx in range(num_lines):
                # work out starting and ending positions
                start_x = -(self.size[axis] / 2) + (line_idx * self.spacing)
                start_y = -(self.size[1-axis] / 2)
                end_x = start_x
                end_y = start_y + self.size[1-axis]

                if axis == 0:
                    v_front = Vector3(start_x, start_y, 0)
                    v_back = Vector3(end_x, end_y, 0)
                elif axis == 1:
                    v_front = Vector3(start_y, start_x, 0)
                    v_back = Vector3(end_y, end_x, 0)

                self.vertices.append(v_front)
                self.vertices.append(v_back)

                self.lines.append(Line2(a=v_idx, b=v_idx + 1))
                v_idx += 2
