# Viz3 - 3D Visualization Tool

A 3D visualization tool with DeltaV integration.

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
# Run the main visualization tool
viz3 --number_of_windows_to_open 3 --window_width 800 --window_height 600

# Run a single DeltaV window
viz3-delta --window_width 1024 --window_height 768 --host localhost --port 8080
```

## Command Line Options

- `--number_of_windows_to_open`: Number of windows to open (default: 1)
- `--window_width`: Width of each window (default: 600)
- `--window_height`: Height of each window (default: 500)
- `--host`: Host address for the server (default: localhost)
- `--port`: Port number for the server (default: 8080)

## Development

To work on this project:

1. Install in development mode: `pip install -e .`
2. Make your changes
3. Test with `viz3` or `viz3-delta` commands 