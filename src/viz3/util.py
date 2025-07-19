from typing import Awaitable, Callable
from autobahn_client import Autobahn


async def subscribe_to_multiple_topics(
    self: Autobahn,
    topics: list[str],
    callback: Callable[[bytes], Awaitable[None]],
) -> None:
    # TODO: add this to the autobahn client library itself.
    for topic in topics:
        await self.subscribe(topic, callback)


def print_cool_ascii_art():
    print(
        """
 __      _____ ______ ____  
 \ \    / /_ _|____  |___ \ 
  \ \  / / | |   / /   __) |
   \ \/ /  | |  / /   |__ < 
    \  /  _|_| /_/_   ___) |
     \/  |_____|___| |____/ 
                            
    3D Visualization Made Awesome!
    """
    )
