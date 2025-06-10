# Viz3 Plugin System

This directory contains example plugins for the Viz3 visualization system.

## How to Create a Plugin

1. **Create a Python file** with your pipeline classes
2. **Inherit from Pipeline** and specify a topic name
3. **Implement the required methods**:
   - `async def process(self, world: World, topic_pub_data: bytes)` - Process incoming data
   - `def tick(self, world: World)` - Called every frame (optional)

## Example Plugin Structure

```python
from src.object_pipelines.pipeline import Pipeline
from src.render.world import World

class MyPipeline(Pipeline, topic="my/custom/topic"):
    async def process(self, world: World, topic_pub_data: bytes):
        # Process your data here
        data = topic_pub_data.decode('utf-8')
        print(f"Received: {data}")
        
        # Add/update objects in the 3D world
        # world.add_object("my_object", some_entity)
```

## Using Plugins

### Method 1: Command Line
```bash
# Single plugin directory
viz3 --plugin-dir /path/to/your/plugins

# Multiple plugin directories  
viz3 --plugin-dir /path/to/plugins1 --plugin-dir /path/to/plugins2

# Exclude specific files
viz3 --plugin-dir /path/to/plugins --plugin-exclude unwanted.py
```

### Method 2: Default Directories
Place your plugins in one of these default locations:
- `~/.viz3/plugins/` (user's home directory)
- `./viz3_plugins/` (current working directory)

## Plugin Development Tips

1. **Always handle exceptions** in your `process()` method
2. **Use descriptive topic names** like "sensor/temperature" or "camera/feed"
3. **Check if objects exist** before creating them: `world.contains_object("name")`
4. **Clean up resources** in your plugin if needed
5. **Test with the example plugin** first to ensure your setup works

## Available World Methods

- `world.add_object(name, entity)` - Add a new object
- `world.get_object(name)` - Get an existing object
- `world.contains_object(name)` - Check if object exists
- `world.remove_object(name)` - Remove an object

## Example Commands

```bash
# Run with the example plugin
viz3 --plugin-dir examples/plugins

# Run multiple windows with plugins
viz3 --number_of_windows_to_open 2 --plugin-dir examples/plugins

# Test the example plugin
viz3 --plugin-dir examples/plugins --window_width 1024 --window_height 768
``` 