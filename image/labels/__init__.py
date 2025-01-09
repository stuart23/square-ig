from labels.label import generate_label  # noqa: F401
from pathlib import Path

"""
Helper to locate the assets directory
"""

assets_dir = Path(__file__).parent.resolve() / "assets"
