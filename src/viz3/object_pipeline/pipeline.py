from viz3.render.world import World
from typing import Dict, Type


class Pipeline:
    """Base class for processing pipelines.

    This class provides a registry for pipeline implementations and defines
    the interface for pipeline processing.
    """

    _registry: Dict[str, tuple[Type["Pipeline"], int | list[int] | None]] = {}

    @classmethod
    def get_registry(cls) -> Dict[str, tuple[Type["Pipeline"], int | list[int] | None]]:
        """Get the pipeline registry.

        Returns:
            Dict[str, Type['Pipeline']]: The registry mapping topic names to pipeline classes
        """
        return cls._registry

    @classmethod
    def register(
        cls, topic: str, window_number_to_show_in: int | list[int] | None = None
    ):
        """Decorator to register a pipeline class for a specific topic.

        Args:
            topic: The topic name to register the pipeline for
            window_number_to_show_in: The window number to show the pipeline in, or a list of window numbers to show the pipeline in. Default is None, which means the pipeline will not be shown in all windows.
        """

        def decorator(pipeline_class):
            cls._registry[topic] = (pipeline_class, window_number_to_show_in)
            return pipeline_class

        return decorator

    async def process(self, world: World, topic_pub_data: bytes):
        raise NotImplementedError

    def tick(self, world: World):
        pass
