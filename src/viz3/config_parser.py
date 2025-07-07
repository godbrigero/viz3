import argparse


def parse_args(additional_args: list[str] = []):
    """Parse command line arguments for the viz3 application.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--number_of_windows_to_open", type=int, default=1)
    parser.add_argument("--window_width", type=int, default=600)
    parser.add_argument("--window_height", type=int, default=500)
    parser.add_argument(
        "--window_x_offset",
        type=int,
        default=50,
        help="X offset between multiple windows",
    )
    parser.add_argument(
        "--window_y_offset",
        type=int,
        default=50,
        help="Y offset between multiple windows",
    )
    parser.add_argument(
        "--window_borderless",
        action="store_true",
        help="Make windows borderless (removes title bar)",
    )
    parser.add_argument(
        "--window_resizable", action="store_true", help="Make windows resizable"
    )
    parser.add_argument(
        "--window_index",
        type=int,
        default=0,
        help="Index of the window (used for positioning multiple windows)",
    )

    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8080)

    parser.add_argument(
        "--plugin-dir",
        action="append",
        dest="plugin_directories",
        help="Add a plugin directory (can be used multiple times)",
    )
    parser.add_argument(
        "--plugin-exclude",
        action="append",
        dest="plugin_exclude_files",
        default=["__init__.py"],
        help="Files to exclude from plugin loading",
    )

    if additional_args:
        for arg in additional_args:
            parser.add_argument(arg)

    return parser.parse_args()
