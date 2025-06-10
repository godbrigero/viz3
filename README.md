# Viz3 - 3D Visualization Tool

A 3D visualization tool for real-time 3D visualization and multi-window support.

## Architecture Overview

### System Architecture

```mermaid
graph TD
    A[viz3 Command] --> B{Number of Windows}
    B -->|1| C[Single Window Process]
    B -->|Multiple| D[Multiple Window Processes]
    
    C --> E[viz3.py Instance]
    D --> E1[viz3.py Instance 1]
    D --> E2[viz3.py Instance 2] 
    D --> E3[viz3.py Instance N...]
    
    E --> F[Plugin Manager]
    E1 --> F1[Plugin Manager]
    E2 --> F2[Plugin Manager]
    E3 --> F3[Plugin Manager]
    
    F --> G[Load Plugins from Directories]
    F1 --> G
    F2 --> G
    F3 --> G
    
    G --> H[Pipeline Registry]
    H --> I[Pipeline Classes]
    I --> J["Topic: 'sensor_data'<br/>Pipeline: SensorProcessor"]
    I --> K["Topic: 'camera_feed'<br/>Pipeline: VideoProcessor"]
    I --> L["Topic: 'custom_data'<br/>Pipeline: YourPlugin"]
    
    E --> M[Ursina 3D Engine]
    E1 --> M1[Ursina 3D Engine]
    E2 --> M2[Ursina 3D Engine]
    E3 --> M3[Ursina 3D Engine]
    
    M --> N[3D Window with World]
    M1 --> N1[3D Window with World]
    M2 --> N2[3D Window with World]
    M3 --> N3[3D Window with World]
    
    E --> O[Autobahn WebSocket Client]
    E1 --> O1[Autobahn WebSocket Client]
    E2 --> O2[Autobahn WebSocket Client]
    E3 --> O3[Autobahn WebSocket Client]
    
    O --> P[viz3 Server<br/>localhost:8080]
    O1 --> P
    O2 --> P
    O3 --> P
    
    P --> Q[Data Publishers]
    Q --> R[Sensor Data]
    Q --> S[Camera Feeds]
    Q --> T[Custom Data]
    
    R --> U[Process via Pipeline]
    S --> U
    T --> U
    
    U --> V[Update 3D World]
    V --> W[Render in Ursina Window]
    
    style A fill:#e1f5fe
    style P fill:#f3e5f5
    style N fill:#e8f5e8
    style N1 fill:#e8f5e8
    style N2 fill:#e8f5e8
    style N3 fill:#e8f5e8
    style G fill:#fff3e0
    style L fill:#ffebee
```

### Data Flow

```mermaid
graph LR
    A[External Data Source] --> B[viz3 Server]
    B --> C[WebSocket Connection]
    C --> D[Autobahn Client]
    D --> E[Topic Subscription]
    E --> F{Pipeline Registry}
    F --> G[Matching Pipeline]
    G --> H[process&#40;world, data&#41;]
    H --> I[World Object Update]
    I --> J[Ursina 3D Rendering]
    J --> K[Visual Output]
    
    L[Plugin Directory] --> M[Plugin Manager]
    M --> N[Load .py Files]
    N --> O[Register Pipelines]
    O --> F
    
    P[User Input] --> Q[Window Controls]
    Q --> R[Move/Resize Window]
    
    style A fill:#ffcdd2
    style B fill:#f8bbd9
    style F fill:#e1bee7
    style G fill:#c5cae9
    style J fill:#bbdefb
    style K fill:#c8e6c9
    style L fill:#fff9c4
    style M fill:#ffecb3
```

### Key Components

1. **viz3 Command**: Main entry point that spawns one or more window processes
2. **Plugin Manager**: Dynamically loads Python files from plugin directories
3. **Pipeline Registry**: Maps topic names to processing pipeline classes
4. **Autobahn Client**: WebSocket client that connects to viz3 server
5. **Ursina Engine**: 3D rendering engine that creates interactive windows
6. **World Object**: Shared 3D scene state that pipelines can modify

### Plugin System

- **Dynamic Loading**: Plugins are `.py` files loaded at runtime from specified directories
- **Pipeline Registration**: Plugins register processing pipelines for specific data topics
- **External Libraries**: Plugins can use any Python library installed in the environment
- **Auto-Discovery**: All `.py` files in plugin directories are automatically loaded (except excluded files)

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

# Run a single viz3 window directly (alternative entry point)
viz3-single --window_width 1024 --window_height 768 --host localhost --port 8080
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
- `--host`: Host address for the viz3 server (default: localhost)
- `--port`: Port number for the viz3 server (default: 8080)

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

### `viz3-single` (Single Window)
A direct entry point that starts a single viz3 visualization window. This command supports all the same window configuration options as `viz3` but always creates exactly one window (ignoring `--number_of_windows_to_open`). 