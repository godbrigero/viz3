from dataclasses import dataclass
from viz3.render.world import World
from typing import Dict, Type
from ursina import color


@dataclass
class AxesOptions:
    length: float = 1
    thickness: float = 0.02
    show: bool = True


@dataclass
class PlaneOptions:
    size: int = 10
    spacing: float = 1.0
    thickness: float = 0.01
    line_color = color.light_gray
    show: bool = True


@dataclass
class PipelineOptions:
    pipeline_type: Type["Pipeline"]
    window_number_to_show_in: int | list[int] | None = None
    axes_options: AxesOptions | None = AxesOptions()
    plane_options: PlaneOptions | None = PlaneOptions()


@dataclass
class PipelineTopicOptions:
    topics: list[str] | str

    def __eq__(self, other):
        if isinstance(other, PipelineTopicOptions):
            return self.topics == other.topics
        return False

    def __hash__(self):
        if isinstance(self.topics, list):
            return hash(tuple(self.topics))
        return hash(self.topics)

    def is_single_topic(self) -> bool:
        return isinstance(self.topics, str)

    def is_multiple_topics(self) -> bool:
        return isinstance(self.topics, list)

    def get_topics(self) -> list[str]:
        if self.is_single_topic():
            return [self.topics]  # type: ignore
        return self.topics  # type: ignore


class Pipeline:
    """Base class for processing pipelines.

    This class provides a registry for pipeline implementations and defines
    the interface for pipeline processing.
    """

    _registry: Dict[PipelineTopicOptions, PipelineOptions] = {}

    @classmethod
    def get_registry(cls) -> Dict[PipelineTopicOptions, PipelineOptions]:
        """Get the pipeline registry.

        Returns:
            Dict[str, Type['Pipeline']]: The registry mapping topic names to pipeline classes
        """
        return cls._registry

    @classmethod
    def register(
        cls,
        topic: str | list[str],
        window_number_to_show_in: int | list[int] | None = None,
        axes_options: AxesOptions | None = None,
        plane_options: PlaneOptions | None = None,
    ):
        """Decorator to register a pipeline class for a specific topic.

        Args:
            topic: The topic name to register the pipeline for
            window_number_to_show_in: The window number to show the pipeline in, or a list of window numbers to show the pipeline in. Default is None, which means the pipeline will not be shown in all windows.
        """

        def decorator(pipeline_class):
            cls._registry[PipelineTopicOptions(topic)] = PipelineOptions(
                pipeline_type=pipeline_class,
                window_number_to_show_in=window_number_to_show_in,
                axes_options=axes_options,
                plane_options=plane_options,
            )

            return pipeline_class

        return decorator

    async def process(self, world: World, topic_pub_data: bytes):
        raise NotImplementedError

    def tick(self, world: World):
        pass
