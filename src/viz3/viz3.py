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

args = parse_args()

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
    window_title="DeltaV",
    window_position=(
        args.window_index * args.window_x_offset,
        args.window_index * args.window_y_offset,
    ),
    borderless=args.window_borderless,
    resizable=args.window_resizable,
)
world = World()


async def main() -> None:
    """Main async function that sets up pipelines and runs the application.

    This function initializes the Autobahn server, creates pipelines for each
    registered topic, and subscribes to those topics with appropriate callbacks.
    """
    autobahn_server = Autobahn(Address(args.host, args.port))
    await autobahn_server.begin()

    pipelines: List[Pipeline] = []

    for topic in Pipeline.get_registry():
        print(topic)
        pipeline_class = Pipeline.get_registry()[topic]
        if pipeline_class:
            pipeline = pipeline_class()
            pipelines.append(pipeline)

            async def create_callback(pipeline_instance):
                async def callback(message: bytes):
                    global world
                    await pipeline_instance.process(world, message)

                return callback

            await autobahn_server.subscribe(topic, await create_callback(pipeline))

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
