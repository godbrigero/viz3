from viz3.render.ground import GroundGrid
from viz3.render.axes import Axes
from ursina import *
from typing import Dict, List, Optional
import time


class Object:
    """Wrapper for entities in the world with metadata."""

    def __init__(self, name: str, entity: Entity, last_update: float) -> None:
        """Initialize an Object.

        Args:
            name: The name/identifier of the object
            entity: The Ursina entity
            last_update: Timestamp of last update
        """
        self._name = name
        self._entity = entity
        self._last_update = last_update

    def get_entity(self) -> Entity:
        """Get the entity and update the timestamp.

        Returns:
            Entity: The Ursina entity
        """
        self._last_update = time.time()
        return self._entity

    def get_last_update(self) -> float:
        """Get the timestamp of last update.

        Returns:
            float: Timestamp of last update
        """
        return self._last_update

    def get_name(self) -> str:
        """Get the object name.

        Returns:
            str: The object name
        """
        return self._name


class World:
    """Main world class that manages the 3D scene and its components.

    This class handles the initialization and management of the 3D world,
    including the ground grid, axes, and various objects in the scene.
    """

    def __init__(self, add_base_objects: bool = True) -> None:
        """Initialize the world with default components.

        Args:
            add_base_objects: Whether to add default objects like ground and axes
        """
        self.objects: Dict[str, Object] = {}
        self.ground_grid: Optional[GroundGrid] = None
        self.axes: Optional[Axes] = None

        # Set up camera
        self.camera = EditorCamera(move_speed=0.5)
        self.camera.rotation = (90, 0, 0)

        if add_base_objects:
            # Initialize default world components
            self._setup_world()

    def _setup_world(self) -> None:
        """Set up the basic world components."""
        # Create ground grid
        ground = GroundGrid(
            size=30, spacing=1.0, thickness=0.01, line_color=color.light_gray
        )
        self.add_object("ground", ground)

        # Create coordinate axes
        axes = Axes(length=1, thickness=0.02)
        self.add_object("axes", axes)

        # Set up full brightness lighting
        # Add ambient light for overall illumination
        ambient = AmbientLight(color=color.white)
        ambient.color = (0.8, 0.8, 0.8, 1)  # Bright ambient light

        # Add multiple directional lights for full coverage
        sun = DirectionalLight()
        sun.look_at(Vec3(1, -1, -1))
        sun.color = (1, 1, 1, 1)  # Full white brightness

        # Add additional lights from different angles for even coverage
        light2 = DirectionalLight()
        light2.look_at(Vec3(-1, -1, 1))
        light2.color = (0.7, 0.7, 0.7, 1)
        print("light2", light2)

        light3 = DirectionalLight()
        light3.look_at(Vec3(0, 1, 0))
        light3.color = (0.5, 0.5, 0.5, 1)

    def contains_object(self, name: str) -> bool:
        """Check if an object with the given name exists.

        Args:
            name: The name of the object to check

        Returns:
            bool: True if the object exists, False otherwise
        """
        return name in self.objects

    def add_object(self, name: str, entity: Entity) -> None:
        """Add an object to the world.

        Args:
            name: The name/identifier for the object
            entity: The Ursina entity to add
        """
        self.objects[name] = Object(name, entity, time.time())

    def get_object(self, name: str) -> Object:
        """Get an object by name.

        Args:
            name: The name of the object to retrieve

        Returns:
            Object: The object wrapper
        """
        return self.objects[name]

    def get_all_objects(self) -> List[Object]:
        """Get all objects in the world.

        Returns:
            List[Object]: List of all object wrappers
        """
        return list(self.objects.values())

    def remove_object(self, name: str) -> None:
        """Remove an object from the world.

        Args:
            name: The name of the object to remove
        """
        if name in self.objects:
            destroy(self.objects[name].get_entity())
            del self.objects[name]

    def clear_objects(self) -> None:
        """Clear all objects from the world."""
        for obj in self.objects.values():
            if hasattr(obj.get_entity(), "destroy"):
                obj.get_entity().destroy()
        self.objects.clear()

    def update(self) -> None:
        """Update the world state."""
        # Update any dynamic objects
        for obj in self.objects.values():
            entity = obj.get_entity()
            if hasattr(entity, "update"):
                entity.update()
