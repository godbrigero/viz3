# Image processing pipeline example
#
# This pipeline demonstrates how to handle image data
# and create visual objects in the 3D world

from typing import TYPE_CHECKING
import numpy as np
from viz3.render.world import World
from viz3.render.objects.apriltag import AprilTag
from viz3.object_pipeline.pipeline import Pipeline
from generated.proto.python.AprilTag_pb2 import AprilTags, RawAprilTagCorners
from generated.proto.python.Image_pb2 import ImageMessage
from project.example.position_debug.three_d.render.objects.image_object import (
    ImageObject,
)
from ursina import Vec3

if TYPE_CHECKING:
    pass


@Pipeline.register("image/data")
class ImagePipeline(Pipeline):
    """Pipeline for processing image data."""

    def __init__(self) -> None:
        """Initialize the image pipeline."""
        super().__init__()
        self.image_count = 0
        self.tags = []

    async def process(self, world: World, topic_pub_data: bytes) -> None:
        """Process image data.

        Args:
            world: The 3D world instance
            topic_pub_data: Raw image data bytes
        """
        try:
            # Example image processing logic
            self.image_count += 1
            print(f"Processed image #{self.image_count}")

            raw_image = ImageMessage.FromString(topic_pub_data)
            image = np.frombuffer(raw_image.image, dtype=np.uint8)
            image = image.reshape(raw_image.height, raw_image.width, 3)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if not world.contains_object("image"):
                img_obj = ImageObject(image, scale=10)
                img_obj.rotation = Vec3(0, 0, 0)
                img_obj.position = Vec3(0, 1, 5)
                world.add_object("image", img_obj)
            else:
                entity = world.get_object("image").get_entity()
                assert isinstance(entity, ImageObject)
                entity.update_texture(image)

        except Exception as e:
            print(f"Error processing image: {e}")

    def tick(self, world: World) -> None:
        """Update the pipeline state.

        Args:
            world: The 3D world instance
        """
        # Periodic processing logic here
        pass
