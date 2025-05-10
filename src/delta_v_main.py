from typing import List
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from object_pipelines.pipeline import Pipeline
from render.cube_point_cloud import CubePointCloud
from render.user import FlyController
from render.axes import Axes
from render.ground import GroundGrid
from render.objects.apriltag import AprilTag
import random
import math
import sys
import asyncio
import threading
from render.world import World
from autobahn_client.client import Autobahn
from autobahn_client.util import Address


app = Ursina()
world = World()


async def main():
    autobahn_server = Autobahn(Address("localhost", 8080))
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
        await asyncio.sleep(0.04)
        pipeline.tick(world)


def run_main():
    asyncio.run(main())


thread = threading.Thread(target=run_main)
thread.daemon = True
thread.start()

app.run()
