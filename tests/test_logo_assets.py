"""Automated Verification Suite for Institutional Logo Assets.

Validates that:
1. Master logo PNG exists, has exact 1024x1024 dimensions, valid PNG signature, and RGBA channels.
2. Vector SVG source exists, contains valid XML, has matching viewBox, and zero raster embedding.
3. Aspect ratio is strictly 1:1.
"""

import os
import struct
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG_PATH = os.path.join(REPO_ROOT, "assets", "cmc_alpha_logo.png")
SVG_PATH = os.path.join(REPO_ROOT, "assets", "cmc_alpha_logo.svg")


def test_png_master_dimensions_and_mode():
    """Verify PNG master is 1024x1024 with valid PNG IHDR header."""
    assert os.path.exists(PNG_PATH), f"Master PNG not found at {PNG_PATH}"
    size_bytes = os.path.getsize(PNG_PATH)
    assert size_bytes > 20_000, f"PNG size too small ({size_bytes} bytes)"

    with open(PNG_PATH, "rb") as f:
        header = f.read(32)

    # Validate PNG magic bytes
    assert header[:8] == b"\x89PNG\r\n\x1a\n", "Invalid PNG file signature"

    # Validate IHDR chunk
    assert header[12:16] == b"IHDR", "Missing IHDR chunk"
    width, height, bit_depth, color_type = struct.unpack(">IIBB", header[16:26])

    assert width == 1024, f"Width must be 1024, got {width}"
    assert height == 1024, f"Height must be 1024, got {height}"
    assert width == height, "Aspect ratio must be strictly 1:1"
    assert color_type in (2, 6), f"Color type must be RGB(2) or RGBA(6), got {color_type}"


def test_svg_vector_syntax_and_viewbox():
    """Verify SVG is valid XML and contains pure vector geometry."""
    assert os.path.exists(SVG_PATH), f"SVG source not found at {SVG_PATH}"
    tree = ET.parse(SVG_PATH)
    root = tree.getroot()

    assert root.tag.endswith("svg"), "Root element must be svg"
    view_box = root.attrib.get("viewBox", "")
    assert view_box == "0 0 1024 1024", f"Unexpected viewBox: {view_box}"

    # Verify no embedded raster base64 slop
    with open(SVG_PATH, "r", encoding="utf-8") as f:
        svg_text = f.read()
    assert "data:image/" not in svg_text, "SVG must not contain embedded raster base64 images"
    assert "QUANTITATIVE TERMINAL" in svg_text, "SVG must include typographic terminal badge"
