from itertools import product

import pygame

from empyro.coord import Point, Size, Rect
from empyro import color
from empyro.glyph import Glyph
from empyro.terminal import RenderableTerminal

from empyro import font as font_
from empyro.font import Font


class SurfaceTerminal(RenderableTerminal):
    """A renderable terminal using pygame surfaces

    properties
        size -- the size (width and height) of the terminal in characters.
        font -- the font used to render the glyphs. fonts are images,
                loaded using `font.load_fonts` function.
        char_width -- the character width. taken from the font.
        line_height -- the line height of a character. taken from the font.
        surface -- the underlying pygame surface used to render the terminal.
    """

    def __init__(self, size: Size = None, font: Font = None):
        super().__init__(size)
        pygame.display.init()
        pygame.mouse.set_visible(False)
        self.font = font_.CP437_9x16 if font is None else font
        self.char_width = self.font.size.width
        self.line_height = self.font.size.height
        size = (self.size.width * self.font.size.width,
                self.size.height * self.font.size.height)
        self._update_rects = []
        try:
            self.surface = pygame.display.set_mode(size)
            self._font_surface, self._glyph_surfaces = _load_glyphs(self.font)
        except:
            pygame.display.quit()
            raise

    def draw_glyph(self, glyph: Glyph, at: Point):
        glyph_surf = self._glyph_surfaces[glyph.code.altcode]
        draw_surf = pygame.Surface(self.font.size)
        draw_surf.set_colorkey(color.BLACK)
        draw_surf.blit(glyph_surf, (0, 0))
        draw_surf.fill(glyph.fg_color, None, pygame.BLEND_MULT)
        draw_rect = (at[0] * self.char_width,
                     at[1] * self.line_height,
                     self.char_width, self.line_height)
        self.surface.fill(glyph.bg_color, draw_rect)
        rect = self.surface.blit(draw_surf, draw_rect)
        self._update_rects.append(rect)

    def render(self):
        pygame.display.update(self._update_rects)
        self._update_rects = []


def _load_glyphs(font: Font):
    char_width, line_height = font.size
    font_surface = pygame.image.load(font.path).convert()
    font_surface.set_colorkey(color.BLACK)
    glyph_surfaces = [
        font_surface.subsurface(
            (x * char_width, y * line_height, char_width, line_height))
        for y in range(16) for x in range(16)
    ]
    return font_surface, glyph_surfaces
