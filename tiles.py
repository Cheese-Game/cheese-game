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
        w = self.image.width // Tileset.TILE_SIZE
        h = self.image.height // Tileset.TILE_SIZE

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
    doors = data['doors']
    return flipud(a), a.shape, doors


class Tilemap:

    def __init__(self, tileset, path, screen_size) -> None:
        self.tileset = tileset
        self.screen_width, self.screen_height = screen_size

        self.map, self.size, self.doors_obj = get_map(path)

        self.position = [self.screen_width // 2, self.screen_height // 2]

    def get_size(self):
        return self.size

    def check_for_door(self, pos):
        try:
            for door in self.doors:
                if door['pos'] == [int(pos[0]), int(pos[1])]:
                    return door['to']
            return None
        except Exception:
            return None

    def draw(self) -> None:
        self.doors = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                tile_id = self.map[i, j]
                
                if tile_id == 0:
                    continue
                elif tile_id < 0:
                    currentDoorObj = self.doors_obj[-1-tile_id]
                    tile_id = currentDoorObj['tile']
                    self.doors.append({
                        "to": currentDoorObj['to'],
                        "pos": [j, i]
                    })
                
                tile = self.tileset.tiles[tile_id]

                tile.blit(j * Tileset.TILE_SIZE + self.position[0],
                          i * Tileset.TILE_SIZE + self.position[1])

    def adjust_position(self, player_pos) -> None:
        x, y = player_pos
        self.position = [
            self.screen_width // 2 - player_pos[0] * 16,
            self.screen_height // 2 - player_pos[1] * 16
        ]

    def update_tilemap(self, tileset, path, screen_size):
        self.tileset = tileset
        self.screen_width, self.screen_height = screen_size

        self.map, self.size, self.doors_obj = get_map(path)

        self.position = [self.screen_width // 2, self.screen_height // 2]