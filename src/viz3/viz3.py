from typing import List
from ursina import *
from viz3.object_pipeline.pipeline import Pipeline
from viz3.object_pipeline.plugin_manager import PluginManager, Directory
import asyncio
import threading
from viz3.render.world import World
from autobahn_client.client import Autobahn
from autobahn_client.util import Address
from viz3.config_parser import parse_args
from pathlib import Path

from viz3.util import subscribe_to_multiple_topics

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


async def main() -> None:
    global world
    """Main async function that sets up pipelines and runs the application.

    This function initializes the Autobahn server, creates pipelines for each
    registered topic, and subscribes to those topics with appropriate callbacks.
    """
    autobahn_server = Autobahn(Address(args.host, args.port))
    await autobahn_server.begin()

    pipelines: List[Pipeline] = []

    for topic in Pipeline.get_registry():
        pipeline_options = Pipeline.get_registry()[topic]
        pipeline = pipeline_options.pipeline_type()
        if pipeline_options.window_number_to_show_in is not None:
            if isinstance(pipeline_options.window_number_to_show_in, int) and int(
                window_number
            ) != int(pipeline_options.window_number_to_show_in):
                print(
                    f"Skipping topic {topic} - window number mismatch: {window_number} != {pipeline_options.window_number_to_show_in}"
                )
                continue
            if (
                isinstance(pipeline_options.window_number_to_show_in, list)
                and int(window_number) not in pipeline_options.window_number_to_show_in
            ):
                print(f"Skipping topic {topic} - window number not in list")
                continue

        pipelines.append(pipeline)
        print(f"Loaded pipeline for topic: {topic.get_topics()}")

        async def create_callback(pipeline_instance):
            async def callback(message: bytes):
                global world
                await pipeline_instance.process(world, message)

            return callback

        await subscribe_to_multiple_topics(
            autobahn_server, topic.get_topics(), await create_callback(pipeline)
        )

        if (
            pipeline_options.axes_options is not None
            and pipeline_options.axes_options.show
        ):
            world_axes = world.get_axes()
            world_axes.set_thickness(pipeline_options.axes_options.thickness)
            world_axes.set_scale(
                Vec3(
                    pipeline_options.axes_options.length,
                    pipeline_options.axes_options.length,
                    pipeline_options.axes_options.length,
                )
            )

        if (
            pipeline_options.plane_options is not None
            and pipeline_options.plane_options.show
        ):
            world_grid = world.get_ground_grid()
            world_grid.set_size(pipeline_options.plane_options.size)
            world_grid.set_spacing(pipeline_options.plane_options.spacing)
            world_grid.set_thickness(pipeline_options.plane_options.thickness)
            world_grid.set_line_color(pipeline_options.plane_options.line_color)

    while True:
        for pipeline in pipelines:
            pipeline.tick(world)
        await asyncio.sleep(0.04)


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
