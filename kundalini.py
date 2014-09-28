import sys
import traceback
from time import monotonic as time
from abc import ABCMeta, abstractmethod
import asyncio
import pygame
from pygame.locals import *

__all__ = ['FrameManager']

EventLoop = asyncio.base_events.BaseEventLoop
Event = pygame.event.Event
Surface = pygame.surface.Surface


#-----------------------------------------------------------------------
class FrameManager(metaclass=ABCMeta):

    DELAY = pow(2, -10)
    FRAME_RATE = 1 / 60
    __screen = None


    #---------------------------------------------------------------
    # Override
    #

    @abstractmethod
    def build_screen(self) -> Surface:
        pass


    def load(self) -> None:
        pass


    def draw(self) -> None:
        self.screen.fill((0, 0, 0))


    def handle_event(self, event:Event) -> None:
        pass


    def update(self, delta:float) -> None:
        pass


    #---------------------------------------------------------------
    # API
    #

    @property
    def screen(self) -> Surface:
        if self.__screen is None:
            self.__screen = self.build_screen()
        return self.__screen


    def init(self) -> None:
        pygame.init()
        loop = self.loop = asyncio.get_event_loop()
        self.load()
        t = time()
        loop.call_soon(self._event_callback)
        loop.call_soon(self._update_callback, t)
        loop.call_soon(self._draw_callback, t)


    def start(self) -> None:
        loop = self.loop
        try:
            loop.run_forever()
        finally:
            loop.close()


    def reset_screen(self, screen:Surface=None) -> None:
        self.__screen = screen


    @classmethod
    def main(cls):
        self = cls()
        self.init()
        self.start()


    #---------------------------------------------------------------
    # Internals
    #

    def _event_callback(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            else:
                try:
                    self.handle_event(event)
                except (SystemExit, KeyboardInterrupt):
                    raise
                except:
                    traceback.print_exc()
        self.loop.call_later(self.DELAY, self._event_callback)


    def _update_callback(self, last:float) -> None:
        t = time()
        try:
            self.update(t - last)

        except:
            traceback.print_exc()

        else:
            self.loop.call_later(self.DELAY, self._update_callback, t)


    def _draw_callback(self, last:float) -> None:
        t = time()
        try:
            self.draw()
            if self.screen.get_flags() & DOUBLEBUF:
                pygame.display.flip()
            else:
                pygame.display.update()

        except:
            traceback.print_exc()

        else:
            self.loop.call_later(
                max(self.FRAME_RATE + last - t, 0),
                self._draw_callback, t,
            )
