"""Support for code page 437 renderable fonts.

Fonts are images with 16x16 glyphs.

Several fonts are loaded by default. Importing this module will
automatically load the fonts in the resources package.

defines the following:
    Font -- a namedtuple that hold the properties of the font.
    load_fonts -- helper function for auto discovery of fonts.
"""
import sys
from typing import NamedTuple, Text
from pathlib import Path

from .coord import Size


Font = NamedTuple('Font', [
    ('size', Size), ('path', Text), ('filename', Text)
])


def load_fonts(path: Text = None):
    """Discover all files in the directory given by `path`
    and load them as fonts.

    font filename format:
        [font name]_[char width]x[line height].[image extension]
    """
    # if no path is supplied the fonts are loaded into the module
    # from the resources package.
    if path is None:
        # TODO find a better way to do this
        path = Path(__file__).resolve().parent / 'resources'
        load_to = sys.modules[__name__].__dict__
    else:
        path = Path(path)
        load_to = {}
    for file in path.iterdir():
        if file.is_dir():
            continue
        try:
            name, dims = file.stem.rsplit('_', maxsplit=1)
            name = ''.join((name.upper(), '_', dims))
            size = Size(*map(int, dims.split('x')))
            load_to[name] = Font(size, file.as_posix(), file.name)
        except:
            # couldn't get the font name and dimensions
            # silently ignore the file
            continue
    return load_to


load_fonts()
