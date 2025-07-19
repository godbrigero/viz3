from typing import List
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from viz3.object_pipeline.pipeline import (
    Pipeline,
    PipelineGlobalConfig,
    PipelineOptions,
    PointOfView,
)
from viz3.object_pipeline.plugin_manager import PluginManager, Directory
import asyncio
import threading
from viz3.render.world import World
from autobahn_client.client import Autobahn
from autobahn_client.util import Address
from viz3.config_parser import parse_args
from pathlib import Path

from viz3.util import print_cool_ascii_art, subscribe_to_multiple_topics

args = parse_args(additional_args=["--window-number"])

window_number = args.window_number

plugin_dirs = []
if args.plugin_directories:
    plugin_dirs = [
        Directory(
            path=Path(plugin_directory),
            exclude_files=args.plugin_exclude_files or ["__init__.py"],
        )
        for plugin_directory in args.plugin_directories
    ]

plugin_manager = PluginManager(plugin_dirs)
plugin_manager.load_plugins()

available_topics = plugin_manager.list_topics()
print(f"Available pipeline topics: {available_topics}")

app = Ursina(
    window_size=(args.window_width, args.window_height),
    window_title="viz3",
    window_position=(
        args.window_index * args.window_x_offset,
        args.window_index * args.window_y_offset,
    ),
    borderless=args.window_borderless,
    resizable=args.window_resizable,
)
world = World()


def should_show_pipeline(pipeline_options: PipelineOptions, window_number: int) -> bool:
    if pipeline_options.window_number_to_show_in is None:
        return True

    if (
        isinstance(pipeline_options.window_number_to_show_in, int)
        and window_number == pipeline_options.window_number_to_show_in
    ):
        return True

    if (
        isinstance(pipeline_options.window_number_to_show_in, list)
        and window_number in pipeline_options.window_number_to_show_in
    ):
        return True

    return False


def set_point_of_view(config: PipelineGlobalConfig, world: World):
    point_of_view_options = config.point_of_view_options
    if point_of_view_options == PointOfView.FIRST_PERSON:
        fps_controller = FirstPersonController(speed=1, gravity=0, y=0)
        fps_controller.cursor.enabled = False
        world.set_camera(fps_controller)
    else:
        world.set_camera(EditorCamera(move_speed=0.5))
        world.set_camera_rotation(Vec3(90, 0, 0))


def set_world_options(config: PipelineGlobalConfig, world: World):
    axes_options = config.axes_options
    plane_options = config.plane_options

    world_axes = world.get_axes()
    world_axes.set_enabled(axes_options.show)
    world_axes.set_thickness(axes_options.thickness)
    world_axes.set_scale(
        Vec3(
            axes_options.length,
            axes_options.length,
            axes_options.length,
        )
    )

    world_grid = world.get_ground_grid()
    world_grid.set_enabled(plane_options.show)
    world_grid.set_size(plane_options.size)
    world_grid.set_spacing(plane_options.spacing)
    world_grid.set_thickness(plane_options.thickness)
    world_grid.set_line_color(plane_options.line_color)

    set_point_of_view(config, world)


async def main() -> None:
    global world
    """Main async function that sets up pipelines and runs the application.

    This function initializes the Autobahn server, creates pipelines for each
    registered topic, and subscribes to those topics with appropriate callbacks.
    """
    autobahn_server = Autobahn(Address(args.host, args.port))
    await autobahn_server.begin()

    global_config = PipelineGlobalConfig.get_registry()
    set_world_options(global_config, world)

    pipelines = []
    registry = Pipeline.get_registry()
    print()
    print("-" * 50)
    print_cool_ascii_art()
    print()
    print("-" * 50)
    for topic, pipeline_options in registry.items():
        if not should_show_pipeline(pipeline_options, window_number):
            print(
                f"Skipping pipeline for topic: {topic.get_topics()} in window {window_number}"
            )
            continue

        pipeline = pipeline_options.pipeline_type()
        pipelines.append(pipeline)  # TODO: potential error
        print(
            f"Loaded pipeline for topic: {topic.get_topics()} in window {window_number}"
        )

        async def create_callback(pipeline_instance):
            async def callback(message: bytes):
                global world
                await pipeline_instance.process(world, message)

            return callback

        await subscribe_to_multiple_topics(
            autobahn_server, topic.get_topics(), await create_callback(pipeline)
        )

    print("-" * 50)
    for pipeline in pipelines:
        print(f"loaded pipeline: {pipeline.__class__.__name__}")

    print("-" * 50)
    print()

    while True:
        for pipeline in pipelines:
            pipeline.tick(world)
        await asyncio.sleep(0.05)


def run_main() -> None:
    """Run the main async function."""
    asyncio.run(main())


def start() -> None:
    """Start the application with threading support."""
    thread = threading.Thread(target=run_main)
    thread.daemon = True
    thread.start()
    app.run()


if __name__ == "__main__":
    start()
else:
    # When run as entry point, execute the full application
    thread = threading.Thread(target=run_main)
    thread.daemon = True
    thread.start()
    app.run()
