from dataclasses import dataclass, field
from pathlib import Path
import importlib.util
import random
import sys
from typing import Dict, Type
from viz3.object_pipeline.pipeline import (
    Pipeline,
    PipelineOptions,
    PipelineTopicOptions,
)


@dataclass
class Directory:
    path: Path
    exclude_files: list[str] = field(default_factory=lambda: ["__init__.py"])


class PluginManager:
    def __init__(self, plugin_directories: list[Directory]):
        self.plugins = []
        self.plugin_directories = plugin_directories

    def load_plugins(self):
        """Load plugins from all configured directories."""
        for directory in self.plugin_directories:
            if not directory.path.exists():
                print(f"Warning: Plugin directory does not exist: {directory.path}")
                continue

            print(f"Loading plugins from: {directory.path}")

            for file in directory.path.glob("*.py"):
                if file.name not in directory.exclude_files:
                    try:
                        self._load_plugin_file(file)
                    except Exception as e:
                        print(f"Error loading plugin {file}: {e}")

    def _load_plugin_file(self, file_path: Path):
        """Load a single Python file as a plugin module."""
        module_name = f"viz3_plugin_{file_path.stem}"

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot create spec for {file_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        print(f"Loaded plugin: {file_path.name}")

    def get_available_pipelines(
        self,
    ) -> Dict[PipelineTopicOptions, PipelineOptions]:
        """Get all available pipelines including loaded plugins."""
        return Pipeline.get_registry()

    def list_topics(self) -> list[PipelineTopicOptions]:
        """List all available pipeline topics."""
        return list(Pipeline.get_registry().keys())
