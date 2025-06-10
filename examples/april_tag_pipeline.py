import time
import numpy as np
from generated.proto.python.AprilTag_pb2 import AprilTags, RawAprilTagCorners
from viz3.render.world import World
from viz3.render.objects.apriltag import AprilTag
from viz3.object_pipeline.pipeline import Pipeline
from ursina import Vec3


@Pipeline.register("apriltag/tag")
class AprilTagPipeline(Pipeline):
    """Pipeline for processing AprilTag detection data."""

    def __init__(self) -> None:
        """Initialize the AprilTag pipeline."""
        super().__init__()
        self.tags: list[int] = []

    async def process(self, world: World, topic_pub_data: bytes) -> None:
        """Process AprilTag detection data.

        Args:
            world: The 3D world instance
            topic_pub_data: The raw message data containing AprilTag information
        """
        try:
            raw_tags = AprilTags.FromString(topic_pub_data)
            for tag in raw_tags.tags:
                if tag.tag_id not in self.tags:
                    self.tags.append(tag.tag_id)

                tag_key = f"tag_{tag.tag_id}"
                if world.contains_object(tag_key):
                    tag_entity = world.get_object(tag_key).get_entity()
                else:
                    tag_entity = AprilTag(tag.tag_id)
                    world.add_object(tag_key, tag_entity)

                assert isinstance(tag_entity, AprilTag)
                tag_entity.set_position((tag.pose_t[0], tag.pose_t[1], tag.pose_t[2]))
                tag_entity.set_rotation_matrix(np.array(tag.pose_R).reshape(3, 3))
        except Exception as e:
            print(f"Error processing AprilTag message: {e}")

    def tick(self, world: World) -> None:
        """Update the pipeline state and remove outdated tags.

        Args:
            world: The 3D world instance
        """
        tags_to_remove = []
        for tag_id in self.tags:
            tag_key = f"tag_{tag_id}"
            if world.contains_object(tag_key):
                tag_entity = world.get_object(tag_key)
                if time.time() - tag_entity.get_last_update() > 2:
                    world.remove_object(tag_key)
            else:
                tags_to_remove.append(tag_id)

        for tag_id in tags_to_remove:
            self.tags.remove(tag_id)
