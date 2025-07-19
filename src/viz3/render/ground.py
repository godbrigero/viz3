from ursina import Entity, Mesh, color
from ursina.vec3 import Vec3


class GroundGrid(Entity):
    def __init__(
        self,
        *,
        size: int = 10,  # number of cells per side
        spacing: float = 1.0,  # world-units between lines
        thickness: float = 0.01,  # line thickness
        line_color=color.gray,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Store parameters as instance variables
        self.size = size
        self.spacing = spacing
        self.thickness = thickness
        self.line_color = line_color

        # Build initial mesh
        self._build_mesh()

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def _build_mesh(self):
        verts = []
        lines = []
        half = self.size * self.spacing / 2

        # vertical lines (parallel to Z)
        for i in range(self.size + 1):
            x = -half + i * self.spacing
            start = Vec3(x, 0, -half)
            end = Vec3(x, 0, half)
            verts.extend([start, end])
            idx = len(verts)
            lines.append((idx - 2, idx - 1))

        # horizontal lines (parallel to X)
        for j in range(self.size + 1):
            z = -half + j * self.spacing
            start = Vec3(-half, 0, z)
            end = Vec3(half, 0, z)
            verts.extend([start, end])
            idx = len(verts)
            lines.append((idx - 2, idx - 1))

        mesh = Mesh(vertices=verts, triangles=lines, mode="line", thickness=self.thickness)  # type: ignore
        self.model = mesh
        self.color = self.line_color

    def set_size(self, size: int):
        self.size = size
        self._build_mesh()

    def set_spacing(self, spacing: float):
        self.spacing = spacing
        self._build_mesh()

    def set_thickness(self, thickness: float):
        self.thickness = thickness
        self._build_mesh()

    def set_line_color(self, line_color):
        self.line_color = line_color
        self.color = line_color
