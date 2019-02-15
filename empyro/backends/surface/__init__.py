import pygame

from empyro.coord import Size
from empyro import color
from empyro.glyph import Glyph
from empyro.key import Key, KeyCode, KeyMod
from empyro.terminal import RenderableTerminal
from empyro.mixin import DrawMixin
from empyro import font as font_
from empyro.font import Font


class SurfaceTerminal(DrawMixin, RenderableTerminal):
    """A renderable terminal using pygame surfaces

    properties
        size -- the size (width and height) of the terminal in characters.
        font -- the font used to render the glyphs. fonts are images,
                loaded using `font.load_fonts` function.
        char_width -- the character width. taken from the font.
        line_height -- the line height of a character. taken from the font.
        display -- the underlying pygame surface (also the pygame display)
                used to render the terminal.
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
        try:
            self.display = pygame.display.set_mode(size)
            self._font_surface, self._glyph_surfaces = _load_glyphs(self.font)
            pygame.event.set_allowed(None)
            pygame.event.set_allowed([pygame.KEYDOWN])
            pygame.key.set_repeat(500, 200)
        except:
            pygame.display.quit()
            raise

    def _get_render_surfaces(self):
        draw_surf = pygame.Surface(self.font.size)
        draw_surf.set_colorkey(color.BLACK)
        for at, glyph in self.consume_changed_cells():
            glyph_surf = self._glyph_surfaces[glyph.code.altcode]
            draw_surf.blit(glyph_surf, (0, 0))
            draw_surf.fill(glyph.fg_color, None, pygame.BLEND_MULT)
            draw_rect = (at[0] * self.char_width,
                         at[1] * self.line_height,
                         self.char_width, self.line_height)
            self.display.fill(glyph.bg_color, draw_rect)
            yield draw_surf, draw_rect
            draw_surf.fill(color.BLACK)

    def render(self):
        rects = self.display.blits(self._get_render_surfaces())
        pygame.display.update(rects)

    def get_key(self):
        pygame.event.clear()
        while True:
            c = map_key_code(pygame.event.wait())
            if c is not None:
                # get the mods state
                m = KeyMod.NO_MOD
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    m |= KeyMod.CTRL
                if mods & pygame.KMOD_SHIFT:
                    m |= KeyMod.SHIFT
                if mods & pygame.KMOD_ALT:
                    m |= KeyMod.ALT
                return Key(c, m)


def map_key_code(event):
    try:
        return KeyCode(event.key)
    except:
        return None

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
