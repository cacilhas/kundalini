#!/usr/bin/env python3
from unittest import TestCase, main
from unittest.mock import Mock, call, patch
from pygame.locals import *
from kundalini import FrameManager


#-----------------------------------------------------------------------
class TestFrameManager(TestCase):

    @patch('kundalini.pygame', Mock())
    @patch('kundalini.asyncio', Mock())
    def test_is_abstract_1(self):
        with self.assertRaises(TypeError):
            FrameManager()


    @patch('kundalini.pygame', Mock())
    @patch('kundalini.asyncio', Mock())
    def test_is_abstract_2(self):
        class Game(FrameManager):
            pass

        with self.assertRaises(TypeError):
            Game()


    @patch('kundalini.pygame', Mock())
    @patch('kundalini.asyncio', Mock())
    def test_implemented(self):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        Game()


    @patch('kundalini.pygame', Mock())
    @patch('kundalini.asyncio', Mock())
    def test_screen(self):
        screen = Mock()

        class Game(FrameManager):
            build_screen = lambda self: screen

        game = Game()
        self.assertEqual(game.screen, screen)


    @patch('kundalini.pygame', Mock())
    @patch('kundalini.asyncio', Mock())
    def test_retain_screen(self):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        game = Game()
        screen = game.screen
        self.assertEqual(game.screen, screen)


    @patch('kundalini.pygame', Mock())
    @patch('kundalini.asyncio', Mock())
    def test_reset_1(self):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        game = Game()
        screen = game.screen
        game.reset_screen()
        self.assertNotEqual(game.screen, screen)


    @patch('kundalini.pygame', Mock())
    @patch('kundalini.asyncio', Mock())
    def test_reset_2(self):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        game = Game()
        screen = Mock()
        game.reset_screen(screen)
        self.assertEqual(game.screen, screen)


    @patch('kundalini.time')
    @patch('kundalini.pygame')
    @patch('kundalini.asyncio')
    def test_init(self, asyncio:Mock, pygame:Mock, time:Mock):
        loop = asyncio.get_event_loop.return_value
        t = time.return_value

        class Game(FrameManager):
            build_screen = lambda self: Mock()
            load = Mock()

        game = Game()
        game.init()
        self.assertEqual(game.loop, loop)
        pygame.init.assert_called_once_with()
        asyncio.get_event_loop.assert_called_once_with()
        game.load.assert_called_once_with()
        time.assert_called_once_with()
        loop.call_soon.assert_calls_has([
            call(game._event_callback),
            call(game._update_callback, t),
            call(game._draw_callback, t),
        ], any_order=True)


    @patch('kundalini.pygame')
    @patch('kundalini.asyncio')
    def test_start(self, asyncio:Mock, pygame:Mock):
        loop = asyncio.get_event_loop.return_value

        class Game(FrameManager):
            build_screen = lambda self: Mock()

        game = Game()
        game.init()
        game.start()
        loop.run_forever.assert_called_once_with()
        loop.close.assert_called_once_with()


    @patch('kundalini.pygame')
    @patch('kundalini.asyncio')
    def test_loop_error(self, asyncio:Mock, pygame:Mock):
        loop = asyncio.get_event_loop.return_value
        loop.run_forever.side_effect = ValueError

        class Game(FrameManager):
            build_screen = lambda self: Mock()

        game = Game()
        game.init()
        with self.assertRaises(ValueError):
            game.start()
        loop.close.assert_called_once_with()


    @patch('kundalini.pygame', Mock())
    @patch('kundalini.asyncio', Mock())
    def test_main(self):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        with patch.object(Game, 'init') as init, patch.object(Game, 'start') as start:
            Game.main()
            init.assert_called_once_with()
            start.assert_called_once_with()


    @patch('kundalini.asyncio', Mock())
    @patch('kundalini.pygame')
    @patch('kundalini.traceback')
    def test_event_callback(self, traceback:Mock, pygame:Mock):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        with patch.object(Game, 'handle_event') as handle_event:
            game = Game()
            game.loop = Mock()
            event = Mock()
            event.type = None
            pygame.event.get.return_value = [event]

            game._event_callback()
            handle_event.assert_called_once_with(event)
            game.loop.call_later.assert_called_once_with(
                pow(2, -10), game._event_callback,
            )
            self.assertFalse(traceback.print_exc.called)


    @patch('kundalini.asyncio', Mock())
    @patch('kundalini.pygame')
    @patch('kundalini.traceback')
    def test_event_quit(self, traceback:Mock, pygame:Mock):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        with patch.object(Game, 'handle_event') as handle_event:
            game = Game()
            game.loop = Mock()
            event = Mock()
            event.type = QUIT
            pygame.event.get.return_value = [event]

            with self.assertRaises(SystemExit):
                game._event_callback()
            self.assertFalse(handle_event.called)
            self.assertFalse(game.loop.call_later.called)
            self.assertFalse(traceback.print_exc.called)


    @patch('kundalini.asyncio', Mock())
    @patch('kundalini.pygame')
    @patch('kundalini.traceback')
    def test_event_exception(self, traceback:Mock, pygame:Mock):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        with patch.object(Game, 'handle_event') as handle_event:
            game = Game()
            game.loop = Mock()
            event = Mock()
            event.type = None
            handle_event.side_effect = ValueError
            pygame.event.get.return_value = [event]

            game._event_callback()
            handle_event.assert_called_once_with(event)
            game.loop.call_later.assert_called_once_with(
                pow(2, -10), game._event_callback,
            )
            traceback.print_exc.assert_called_once_with()


    @patch('kundalini.asyncio', Mock())
    @patch('kundalini.pygame', Mock())
    @patch('kundalini.time')
    @patch('kundalini.traceback')
    def test_update_callback(self, traceback:Mock, time:Mock):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        with patch.object(Game, 'update') as update:
            time.return_value = 1.
            game = Game()
            game.loop = Mock()
            game._update_callback(.25)
            update.assert_called_once_with(.75)
            self.assertFalse(traceback.print_exc.called)
            game.loop.call_later.assert_called_once_with(
                pow(2, -10), game._update_callback, 1.,
            )


    @patch('kundalini.asyncio', Mock())
    @patch('kundalini.pygame', Mock())
    @patch('kundalini.time')
    @patch('kundalini.traceback')
    def test_update_exception(self, traceback:Mock, time:Mock):
        class Game(FrameManager):
            build_screen = lambda self: Mock()

        with patch.object(Game, 'update') as update:
            time.return_value = 1.
            game = Game()
            game.loop = Mock()
            update.side_effect = ValueError
            game._update_callback(.25)
            update.assert_called_once_with(.75)
            traceback.print_exc.assert_called_once_with()
            self.assertFalse(game.loop.call_later.called)


    @patch('kundalini.asyncio', Mock())
    @patch('kundalini.pygame')
    @patch('kundalini.time')
    @patch('kundalini.traceback')
    def test_draw_callback(self, traceback:Mock, time:Mock, pygame:Mock):
        screen = Mock()
        screen.get_flags.return_value = 0

        class Game(FrameManager):
            build_screen = lambda self: screen

        with patch.object(Game, 'draw') as draw:
            time.return_value = 1.
            game = Game()
            game.loop = Mock()
            game._draw_callback(1 - pow(2, -10))
            draw.assert_called_once_with()
            pygame.display.update.assert_called_once_with()
            self.assertFalse(pygame.display.flip.called)
            self.assertFalse(traceback.print_exc.called)
            game.loop.call_later.assert_called_once_with(
                0.015690104166666607, game._draw_callback, 1.,
            )


    @patch('kundalini.asyncio', Mock())
    @patch('kundalini.pygame')
    @patch('kundalini.time')
    @patch('kundalini.traceback')
    def test_draw_doublebuf(self, traceback:Mock, time:Mock, pygame:Mock):
        screen = Mock()
        screen.get_flags.return_value = DOUBLEBUF

        class Game(FrameManager):
            build_screen = lambda self: screen

        with patch.object(Game, 'draw') as draw:
            time.return_value = 1.
            game = Game()
            game.loop = Mock()
            game._draw_callback(1 - pow(2, -10))
            draw.assert_called_once_with()
            pygame.display.flip.assert_called_once_with()
            self.assertFalse(pygame.display.update.called)
            self.assertFalse(traceback.print_exc.called)
            game.loop.call_later.assert_called_once_with(
                0.015690104166666607, game._draw_callback, 1.,
            )


    @patch('kundalini.asyncio', Mock())
    @patch('kundalini.pygame')
    @patch('kundalini.time')
    @patch('kundalini.traceback')
    def test_draw_exception(self, traceback:Mock, time:Mock, pygame:Mock):
        screen = Mock()
        screen.get_flags.return_value = 0

        class Game(FrameManager):
            build_screen = lambda self: screen

        with patch.object(Game, 'draw') as draw:
            time.return_value = 1.
            game = Game()
            game.loop = Mock()
            draw.side_effect = ValueError
            game._draw_callback(1 - pow(2, -10))
            draw.assert_called_once_with()
            self.assertFalse(pygame.display.update.called)
            self.assertFalse(pygame.display.flip.called)
            self.assertFalse(game.loop.call_later.print_exc.called)
            traceback.print_exc.assert_called_once_with()


#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()
