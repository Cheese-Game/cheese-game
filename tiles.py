import json
import pyglet

from logger import log
from numpy import array, flipud


class Tileset:

    TILE_SIZE = 16

    def __init__(self, path) -> None:
        self.path = path

        self.image = pyglet.resource.image(path)
        self.tiles = []

        self.load()

    def load(self) -> None:
        w, h = self.image.width // Tileset.TILE_SIZE, self.image.height // Tileset.TILE_SIZE

        for x in range(0, w):
            for y in range(0, h):
                self.tiles.append(self.image.get_region(Tileset.TILE_SIZE * x, Tileset.TILE_SIZE * y,
                                                        Tileset.TILE_SIZE, Tileset.TILE_SIZE))

    def update_tileset(self, path):
        self.path = path

        self.image = pyglet.resource.image(path)
        self.tiles = []

        self.load()

def get_map(tilemap):
    with open(tilemap, 'r') as file:
        data = json.load(file)
    a = array(data['layer0'])
    a = flipud(a)
    return a, a.shape


class Tilemap:

    def __init__(self, tileset, path, screen_size) -> None:
        self.tileset = tileset
        self.screen_width, self.screen_height = screen_size

        self.map, self.size = get_map(path)

        self.position_offset = [
            self.screen_width // 2 - (self.size[0] + 1) *
            (Tileset.TILE_SIZE // 2), self.screen_height // 2 -
            (self.size[1] + 1) * (Tileset.TILE_SIZE // 2)
        ]

        self.position = [self.position_offset[0], self.position_offset[1]]

    def draw(self) -> None:
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                tile = self.tileset.tiles[self.map[i, j]]

                tile.blit(j * Tileset.TILE_SIZE + self.position[0],
                          i * Tileset.TILE_SIZE + self.position[1])

    def adjust_position(self, player_pos) -> None:
        x, y = player_pos
        self.position = [
            self.position_offset[0] - x + self.screen_width // 2,
            self.position_offset[1] - y + self.screen_height // 2
        ]

    def update_tilemap(self, tileset, path, screen_size):
        self.tileset = tileset
        self.screen_width, self.screen_height = screen_size

        self.map, self.size = get_map(path)

        self.position_offset = [
            self.screen_width // 2 - (self.size[0] + 1) *
            (Tileset.TILE_SIZE // 2), self.screen_height // 2 -
            (self.size[1] + 1) * (Tileset.TILE_SIZE // 2)
        ]

        self.position = [self.position_offset[0], self.position_offset[1]]