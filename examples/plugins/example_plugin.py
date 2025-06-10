"""
Example Plugin for Viz3

This is a template plugin that shows how to create custom pipelines for Viz3.
Users can copy this file and modify it to create their own data processing pipelines.
"""

from typing import TYPE_CHECKING
import asyncio
import numpy as np
from viz3.object_pipeline.pipeline import Pipeline
from viz3.render.world import World
from ursina import Entity, Vec3, color

if TYPE_CHECKING:
    pass


@Pipeline.register("example/topic")
class ExamplePipeline(Pipeline):
    """
    Example pipeline that processes custom data.

    To use this plugin:
    1. Copy this file to your plugin directory
    2. Modify the topic name and processing logic
    3. Run viz3 with --plugin-dir pointing to your plugin directory
    """

    def __init__(self) -> None:
        """Initialize the example pipeline."""
        super().__init__()
        self.data_count = 0

    async def process(self, world: World, topic_pub_data: bytes) -> None:
        """
        Process incoming data from the topic.

        Args:
            world: The 3D world where objects can be added/modified
            topic_pub_data: Raw bytes data received from the topic
        """
        try:
            # Example: Convert bytes to string (modify as needed)
            data_str = topic_pub_data.decode("utf-8")
            print(f"Received data: {data_str}")

            # Example: Create or update a 3D object in the world
            object_name = "example_object"

            if not world.contains_object(object_name):
                # Create a new cube object
                cube = Entity(
                    model="cube",
                    color=color.blue,
                    scale=Vec3(1, 1, 1),
                    position=Vec3(0, 0, 0),
                )
                world.add_object(object_name, cube)
                print("Created example cube in world")
            else:
                # Update existing object
                obj = world.get_object(object_name)
                if obj:
                    entity = obj.get_entity()
                    # Example: Move the cube based on data count
                    entity.position = Vec3(self.data_count % 10, 0, 0)

            self.data_count += 1

        except Exception as e:
            print(f"Error in ExamplePipeline.process: {e}")

    def tick(self, world: World) -> None:
        """
        Called periodically (every frame/tick) regardless of data reception.
        Use this for animations or periodic updates.
        """
        # Example: Rotate the example object if it exists
        print("tick")
        if world.contains_object("example_object"):
            obj = world.get_object("example_object")
            if obj:
                entity = obj.get_entity()
                entity.rotation_y += 1  # Rotate 1 degree per tick
