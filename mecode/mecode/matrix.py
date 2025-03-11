import math
import copy
import numpy as np
from .main import G

class GMatrix(G):
    """
    This class applies 3D transformation matrices to CNC moves, supporting
    translation, scaling, and reflection in 3D, while restricting rotations
    to only the Z-axis to maintain GCode ARC compatibility.
    """

    def __init__(self, *args, **kwargs):
        super(GMatrix, self).__init__(*args, **kwargs)
        self._matrix_setup()
        self.position_savepoints = []

    # Position savepoints #####################################################
    def save_position(self):
        self.position_savepoints.append((
            self.current_position["x"],
            self.current_position["y"],
            self.current_position["z"]
        ))

    def restore_position(self):
        x, y, z = self.position_savepoints.pop()
        self.abs_move(x, y, z)

    # Matrix manipulation #####################################################
    def _matrix_setup(self):
        """Initialize the transformation matrix stack with 4x4 matrices."""
        self.matrix_stack = [np.identity(4)]

    def push_matrix(self):
        """Save a copy of the current transformation matrix."""
        self.matrix_stack.append(copy.deepcopy(self.matrix_stack[-1]))

    def pop_matrix(self):
        """Restore the previous transformation matrix."""
        if len(self.matrix_stack) > 1:
            self.matrix_stack.pop()

    def translate(self, tx, ty, tz=0):
        """Apply a 3D translation."""
        translation_matrix = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])
        self.matrix_stack[-1] = translation_matrix @ self.matrix_stack[-1]

    def rotate(self, angle):
        """Rotate around the Z axis only (in radians)."""
        rotation_matrix = np.array([
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.matrix_stack[-1] = rotation_matrix @ self.matrix_stack[-1]

    def scale(self, scale):
        """Scale the transformation matrix in 3D."""

        if isinstance(scale, (int, float)):
            sx = sy = sz = scale
        elif len(scale) == 3:
            sx, sy, sz = scale
        else:
            sx = sy = scale
            sz = 1

        scale_matrix = np.array([
            [sx, 0,  0,  0],
            [0, sy,  0,  0],
            [0,  0, sz,  0],
            [0,  0,  0,  1]
        ])

        self.matrix_stack[-1] = scale_matrix @ self.matrix_stack[-1]

    def reflect(self, angle):
        """Reflect in the XY plane about a given angle from the X-axis."""
        x_axis = self.matrix_stack[-1] @ np.array([1, 0, 0, 1])
        x_angle = math.atan2(x_axis[1], x_axis[0])

        tt = 2 * (x_angle + angle)

        reflection_matrix = np.array([
            [math.cos(tt), math.sin(tt), 0, 0],
            [math.sin(tt), -math.cos(tt), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.matrix_stack[-1] = reflection_matrix @ self.matrix_stack[-1]

    def transform(self, x, y, z):
        """Apply the current transformation matrix to (x, y, z)."""
        point = np.array([x or 0, y or 0, z or 0, 1])
        x, y, z, u = self.matrix_stack[-1] @ point
        return x, y, z

    def _matrix_transform_length(self, length):
        """Transform a length while considering scaling."""
        transformed = self.transform(length, 0, 0)
        return math.sqrt(sum(coord ** 2 for coord in transformed))

    def abs_move(self, x=None, y=None, z=None, **kwargs):
        """Move to an absolute position."""
        x = x if x is not None else self.current_position['x']
        y = y if y is not None else self.current_position['y']
        z = z if z is not None else self.current_position['z']
        super(GMatrix, self).abs_move(x, y, z, **kwargs)

    def move(self, x=None, y=None, z=None, **kwargs):
        """Apply the transformation matrix before moving."""
        tx, ty, tz = self.transform(x, y, z)
        tx, ty = (tx, ty) if x is not None or y is not None else (None, None)
        tz = tz if z is not None else None
        super(GMatrix, self).move(tx, ty, tz, **kwargs)

    def _arc_direction_transform(self, direction):
        """Determine if arc direction needs to be flipped based on transformation."""
        xy_matrix = self.matrix_stack[-1][:2, :2]
        if np.linalg.det(xy_matrix) < 0:
            return 'CCW' if direction == 'CW' else 'CW'
        return direction

    def arc(self, x=None, y=None, z=None, direction='CW', radius='auto',
            helix_dim=None, helix_len=0, **kwargs):
        """Apply transformations to arc movements while maintaining GCode compatibility."""
        (x_prime,y_prime,z_prime) = self.transform(x,y,z)
        if x is None: x_prime = None
        if y is None: y_prime = None
        if z is None: z_prime = None
        if helix_len: helix_len = self._matrix_transform_length(helix_len)

        direction = self._arc_direction_transform(direction)

        super(GMatrix, self).arc(
            x=x_prime, y=y_prime, z=z_prime,
            direction=direction, radius=radius,
            helix_dim=helix_dim, helix_len=helix_len,
            **kwargs
        )

    @property
    def current_position(self):
        """Compute the current position in the transformed coordinate system."""

        current_position = self._current_position.copy()

        x = current_position.get('x', 0)
        y = current_position.get('y', 0)
        z = current_position.get('z', 0)

        point = np.array([x, y, z, 1])
        transform = np.linalg.inv(self.matrix_stack[-1]) @ point

        current_position['x'] = transform[0]
        current_position['y'] = transform[1]
        current_position['z'] = transform[2]

        return current_position