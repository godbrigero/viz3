from typing import Any
from ursina import *
import numpy as np


class Axes(Entity):
    def __init__(self, scale: Vec3 = Vec3(1, 1, 1), thickness: float = 0.02, **kwargs):
        super().__init__(**kwargs)
        self.scale = scale

        # X axis
        self.x_axis = Entity(
            parent=self,
            model="cube",
            color=color.red,
            scale=(1, thickness, thickness),
            position=(0.5, 0, 0),
        )
        # Y axis
        self.y_axis = Entity(
            parent=self,
            model="cube",
            color=color.green,
            scale=(thickness, 1, thickness),
            position=(0, 0.5, 0),
        )
        # Z axis
        self.z_axis = Entity(
            parent=self,
            model="cube",
            color=color.blue,
            scale=(thickness, thickness, 1),
            position=(0, 0, 0.5),
        )

        self.set_scale(scale)

    def set_scale(self, scale: Vec3):
        self.scale = scale

    def set_thickness(self, thickness: float):
        self.x_axis.scale = (self.x_axis.scale.x, thickness, thickness)
        self.y_axis.scale = (thickness, self.y_axis.scale.y, thickness)
        self.z_axis.scale = (thickness, thickness, self.z_axis.scale.z)

    def set_position(self, position: Vec3):
        self.position = position

    def set_rotation_matrix(self, rotation_matrix: np.ndarray):
        if rotation_matrix.shape != (3, 3):
            raise ValueError("Rotation matrix must be 3x3")

        # Convert rotation matrix to quaternion
        # Using Shepperd's method for numerical stability
        trace = np.trace(rotation_matrix)

        if trace > 0:
            s = np.sqrt(trace + 1.0) * 2
            w = 0.25 * s
            x = (rotation_matrix[2, 1] - rotation_matrix[1, 2]) / s
            y = (rotation_matrix[0, 2] - rotation_matrix[2, 0]) / s
            z = (rotation_matrix[1, 0] - rotation_matrix[0, 1]) / s
        elif (
            rotation_matrix[0, 0] > rotation_matrix[1, 1]
            and rotation_matrix[0, 0] > rotation_matrix[2, 2]
        ):
            s = (
                np.sqrt(
                    1.0
                    + rotation_matrix[0, 0]
                    - rotation_matrix[1, 1]
                    - rotation_matrix[2, 2]
                )
                * 2
            )
            w = (rotation_matrix[2, 1] - rotation_matrix[1, 2]) / s
            x = 0.25 * s
            y = (rotation_matrix[0, 1] + rotation_matrix[1, 0]) / s
            z = (rotation_matrix[0, 2] + rotation_matrix[2, 0]) / s
        elif rotation_matrix[1, 1] > rotation_matrix[2, 2]:
            s = (
                np.sqrt(
                    1.0
                    + rotation_matrix[1, 1]
                    - rotation_matrix[0, 0]
                    - rotation_matrix[2, 2]
                )
                * 2
            )
            w = (rotation_matrix[0, 2] - rotation_matrix[2, 0]) / s
            x = (rotation_matrix[0, 1] + rotation_matrix[1, 0]) / s
            y = 0.25 * s
            z = (rotation_matrix[1, 2] + rotation_matrix[2, 1]) / s
        else:
            s = (
                np.sqrt(
                    1.0
                    + rotation_matrix[2, 2]
                    - rotation_matrix[0, 0]
                    - rotation_matrix[1, 1]
                )
                * 2
            )
            w = (rotation_matrix[1, 0] - rotation_matrix[0, 1]) / s
            x = (rotation_matrix[0, 2] + rotation_matrix[2, 0]) / s
            y = (rotation_matrix[1, 2] + rotation_matrix[2, 1]) / s
            z = 0.25 * s

        # Set the rotation using quaternion
        self.quaternion = Vec4(x, y, z, w)

    def set_all_entity_attr(self, attr_name: str, value: Any):
        setattr(self.x_axis, attr_name, value)
        setattr(self.y_axis, attr_name, value)
        setattr(self.z_axis, attr_name, value)
