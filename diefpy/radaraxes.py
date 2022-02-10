import matplotlib.path as mpath
import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars: int, frame: str = 'circle'):
    """
    This function creates a RadarAxes projection with 'num_vars' axes and registers it.


    :param int num_vars: number of axes for the radar chart
    :param str frame: shape of frame surrounding axes {'circle' | 'polygon'}
    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(mtransforms.Transform):
        """
        The base polar transform. This handles projection *theta* and
        *r* into Cartesian coordinate space *x* and *y*, but does not
        perform the ultimate affine transformation into the correct
        position.

        This is copied from Matplotlib version 3.2.2 since in 3.3.0
        the grid lines are using a different interpolation method.
        """
        input_dims = output_dims = 2

        def __init__(self, axis=None, use_rmin=True,
                     _apply_theta_transforms=True):
            mtransforms.Transform.__init__(self)
            self._axis = axis
            self._use_rmin = use_rmin
            self._apply_theta_transforms = _apply_theta_transforms

        def transform_non_affine(self, tr):
            # docstring inherited
            t, r = np.transpose(tr)
            # PolarAxes does not use the theta transforms here, but apply them for
            # backwards-compatibility if not being used by it.
            if self._apply_theta_transforms and self._axis is not None:
                t *= self._axis.get_theta_direction()
                t += self._axis.get_theta_offset()
            if self._use_rmin and self._axis is not None:
                r = (r - self._axis.get_rorigin()) * self._axis.get_rsign()
            r = np.where(r >= 0, r, np.nan)
            return np.column_stack([r * np.cos(t), r * np.sin(t)])

        def transform_path_non_affine(self, path):
            # docstring inherited
            vertices = path.vertices
            if len(vertices) == 2 and vertices[0, 0] == vertices[1, 0]:
                return mpath.Path(self.transform(vertices), path.codes)
            ipath = path.interpolated(path._interpolation_steps)
            return mpath.Path(self.transform(ipath.vertices), ipath.codes)

        def inverted(self):
            # docstring inherited
            return PolarAxes.InvertedPolarTransform(self._axis, self._use_rmin, self._apply_theta_transforms)

    class RadarAxes(PolarAxes):
        """
        Axes for the radar plot. The layout can either be a circle or a polygon with 'num_vars' vertices.
        """
        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5 in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            """ Draw. If frame is polygon, make gridlines polygon-shaped """
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at (0, 0) but we want a polygon
                # of radius 0.5 centered at (0.5, 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5) + self.transAxes)

                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    RadarAxes.PolarTransform = RadarTransform
    register_projection(RadarAxes)
    return theta
