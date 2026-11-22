import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame
from constants import BLUE
from game import Starter
from vec2d import vec2d


class SimulationTest(unittest.TestCase):
    def tearDown(self):
        pygame.quit()

    def test_launch_from_another_directory_and_reuse_palette(self):
        palette = {"blue": BLUE}
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as elsewhere:
            try:
                os.chdir(elsewhere)
                for _ in range(2):
                    game = Starter((800, 600), palette, 20, 24)
                    game.startgui()
                    game.game_running = True
                    for _ in range(12):
                        game.update()
                        game.draw()
                    self.assertEqual(palette, {"blue": BLUE})
            finally:
                os.chdir(previous)

    def test_nearest_cell_and_shared_index_coordinates(self):
        game = Starter((800, 600), {"blue": BLUE}, 2, 24)
        first, second = game.world.population.values()
        first.pos, second.pos = vec2d(90, 100), vec2d(99, 100)
        population = game.world.population
        population.refresh()
        with patch.object(game, "show_info"):
            game.click_cell(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(100, 100)))
        self.assertIs(game.values["infocell"], second)
        second.pos = vec2d(99, 150)
        population.refreshItem(second)
        self.assertEqual(population.inrange(first.pos, 1), {first})
        self.assertEqual(population.inrange(second.pos, 1), {second})
        del population[second.name]
        self.assertEqual(population.inrange(first.pos, 1), {first})
        first.energyMod(10)
        self.assertEqual(first.energy, first.energy_max)
        first.energyMod(-200)
        self.assertEqual(first.energy, 0)
