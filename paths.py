"""Locations of game resources and scores."""

import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    executable = Path(sys.executable).resolve()
    app = next((parent for parent in executable.parents if parent.suffix == ".app"), None)
    ROOT = app / "Contents" / "Resources" if sys.platform == "darwin" and app else executable.parent
else:
    ROOT = Path(__file__).resolve().parent


def resource_path(path):
    return str(ROOT / path)


def scores_path():
    return ROOT / "scores.json"
