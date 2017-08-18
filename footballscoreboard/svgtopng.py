#!/usr/bin/env python3

# Python standard library imports
import io
# Imports from external modules
import cairosvg


def svg_to_png(svg_file_path):
    data = None
    with open(svg_file_path, "r") as svg_file_handle:
        svg_code = svg_file_handle.read()
        png_buffer = io.StringIO()
        cairosvg.svg2png(bytestring=svg_code, write_to=png_buffer)
        data = png_buffer.read()
    return data
