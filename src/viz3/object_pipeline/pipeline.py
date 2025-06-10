from viz3.render.world import World
from typing import Dict, Type


class Pipeline:
    """Base class for processing pipelines.

    This class provides a registry for pipeline implementations and defines
    the interface for pipeline processing.
    """

    _registry: Dict[str, Type["Pipeline"]] = {}

    @classmethod
    def get_registry(cls) -> Dict[str, Type["Pipeline"]]:
        """Get the pipeline registry.

        Returns:
            Dict[str, Type['Pipeline']]: The registry mapping topic names to pipeline classes
        """
        return cls._registry

    @classmethod
    def register(cls, topic: str):
        """Decorator to register a pipeline class for a specific topic.

        Args:
            topic: The topic name to register the pipeline for
        """

        def decorator(pipeline_class):
            cls._registry[topic] = pipeline_class
            return pipeline_class

        return decorator

    async def process(self, world: World, topic_pub_data: bytes):
        raise NotImplementedError

    def tick(self, world: World):
        pass
