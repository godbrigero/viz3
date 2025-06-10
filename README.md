# Viz3 - 3D Visualization Tool

A 3D visualization tool with DeltaV integration for real-time 3D visualization and multi-window support.

## Installation

### Development Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd viz3

# Install in development mode
pip install -e .
```

### Regular Installation
```bash
pip install .
```

## Usage

After installation, you can run the tool from anywhere:

```bash
# Run with a single movable window
viz3

# Run with multiple windows
viz3 --number_of_windows_to_open 3 --window_width 800 --window_height 600

# Run with custom window positioning
viz3 --number_of_windows_to_open 2 --window_x_offset 100 --window_y_offset 80

# Run with borderless windows (no title bar, not movable)
viz3 --window_borderless --number_of_windows_to_open 2

# Run with resizable windows
viz3 --window_resizable --number_of_windows_to_open 1

# Run with plugin directories
viz3 --plugin-dir /path/to/plugins --plugin-exclude __init__.py --plugin-exclude test.py

# Run a single DeltaV window directly (alternative entry point)
viz3-delta --window_width 1024 --window_height 768 --host localhost --port 8080
```

## Command Line Options

### Window Configuration
- `--number_of_windows_to_open`: Number of windows to open (default: 1)
- `--window_width`: Width of each window in pixels (default: 600)
- `--window_height`: Height of each window in pixels (default: 500)
- `--window_x_offset`: X offset between multiple windows in pixels (default: 50)
- `--window_y_offset`: Y offset between multiple windows in pixels (default: 50)
- `--window_borderless`: Make windows borderless - removes title bar and makes windows unmovable (default: False)
- `--window_resizable`: Make windows resizable by dragging edges/corners (default: False)

### Network Configuration
- `--host`: Host address for the DeltaV server (default: localhost)
- `--port`: Port number for the DeltaV server (default: 8080)

### Plugin Configuration
- `--plugin-dir`: Add a plugin directory (can be used multiple times)
- `--plugin-exclude`: Files to exclude from plugin loading (can be used multiple times, default: __init__.py)

## Window Behavior

By default, viz3 creates windows with:
- **Title bars and borders** - making them fully movable with your mouse
- **Fixed size** - windows are not resizable unless `--window_resizable` is specified
- **Automatic positioning** - multiple windows are offset to prevent overlap

### Moving Windows
- **With title bar** (default): Drag the title bar to move the window
- **Borderless mode**: Windows cannot be moved as they have no title bar

### Multiple Windows
When opening multiple windows, each window is automatically positioned with offsets to prevent them from appearing on top of each other.

## Development

To work on this project:

1. Install in development mode: `pip install -e .`
2. Make your changes
3. Test with `viz3` commands
4. Run with different configurations to test window behavior 

## Commands

### `viz3` (Main Command)
The primary command that supports multiple windows and full window management features.

### `viz3-delta` (Single Window)
A direct entry point that starts a single DeltaV visualization window. This command supports all the same window configuration options as `viz3` but always creates exactly one window (ignoring `--number_of_windows_to_open`). 