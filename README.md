# Kundalini

[LÖVE](http://www.love2d.org/) is an **awesome** framework you can use
to make 2D games in [Lua](http://www.lua.org/), in a very similar way
with [PyGame](http://www.pygame.org/).

Kundalini intends to offer an API similar to that of LÖVE to develop
games using PyGame.


## Usage

Subclass `kundalini.FrameManager` and override the method:
```
    @abstractmethod
    def build_screen(self) -> Surface:
        pass
```


It must return a `pygame.surface.Surface`, like, for example, the
object returned by `pygame.display.set_mode()`.

You also can override:
```
    def load(self) -> None:
        pass


    def draw(self) -> None:
        self.screen.fill((0, 0, 0))


    def handle_event(self, event:Event) -> None:
        pass


    def update(self, delta:float) -> None:
        pass
```


The method `load()` is performed by `init()` call, just after
`pygame.init()`.

The method `draw()` is performed every drawing loop.

The method `handle_event()` is performed for each occuring event. It
receives the event as parameter.

The method `update()` is performed about 1024 times a second, and
receives the time delta in seconds since last performing as parameter.

The property `screen` represents the surface returned by
`build_screen()`.


## Running the code

Call the classmethod ``main()``.


## Complete example

```
#!/usr/bin/env python3

import sys
from os import path
from collections import namedtuple
import pygame
from pygame.locals import *
from kundalini import FrameManager, Surface, Event

ColorTriad = namedtuple('ColorTriad', 'r g b')


#-----------------------------------------------------------------------
class ColorTweaker(FrameManager):

    def build_screen(self) -> Surface:
        return pygame.display.set_mode((300, 200), HWSURFACE|DOUBLEBUF, 24)


    def load(self) -> None:
        pygame.display.set_caption('Pygame Color Test - #808080')
        self.size = (300, 200)
        self.scales = [0x80, 0x80, 0x80]


    def update(self, delta:float) -> None:
        x, y = pygame.mouse.get_pos()
        self.size = width, sheight = self.screen.get_size()
        self.height = height = int(sheight / 6)
        scales = self.scales

        if pygame.mouse.get_pressed()[0] and 0 < y < height * 3:
            for c in range(3):
                if c * height < y < (c + 1) * height:
                    scales[c] = max(min(int(x * 0x100 / width), 0xff), 0)
            pygame.display.set_caption('Pygame Color Test - {}'.format(hexcolor(scales)))


    def draw(self) -> None:
        screen = self.screen
        scales = self.scales
        width, _ = self.size
        height = self.height
        screen.fill((0x00, 0x00, 0x00))

        for c in range(3):
            left, right = scales[:], scales[:]
            left[c], right[c] = 0x00, 0xff
            ss = create_scale(ColorTriad(*left),
                              ColorTriad(*right),
                              (width, height))
            pos = int(scales[c] * width / 0x100), int((c + .5) * height)
            screen.blit(ss, (0, c * height))
            pygame.draw.circle(screen, (0xff, 0xff, 0xff), pos, height // 3)

        pygame.draw.rect(screen, tuple(scales),
                         Rect(0, 3 * height,width, screen.get_height() - 3 * height))


    def handle_event(self, event:Event) -> None:
        if event.type == KEYDOWN and event.key == K_q and event.mod & KMOD_META:
            sys.exit()


#-----------------------------------------------------------------------
def create_scale(left:ColorTriad, right:ColorTriad, size:tuple) -> Surface:
    width, height = size
    s = Surface(size)
    s.lock()
    for x in range(width):
        r = int(left.r + (right.r - left.r) * x / width)
        g = int(left.g + (right.g - left.g) * x / width)
        b = int(left.b + (right.b - left.b) * x / width)
        r = max(min(r, 0xff), 0x00)
        g = max(min(g, 0xff), 0x00)
        b = max(min(b, 0xff), 0x00)
        pygame.draw.line(s, (r, g, b), (x, 0), (x, height))
    s.unlock()
    return s


#-----------------------------------------------------------------------
def hexcolor(color:list) -> str:
    r, g, b = color
    return '#{:06x}'.format((r << 16) | (g << 8) | b)


#-----------------------------------------------------------------------
if __name__ == '__main__':
    ColorTweaker.main()
```
