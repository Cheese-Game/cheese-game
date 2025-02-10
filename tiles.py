from pyglet import resource, sprite, graphics
from xml.etree.ElementTree import parse
from numpy import zeros
from math import floor, ceil
from os import path

from logger import log


class Tile(sprite.Sprite):
    def __init__(self, img, x, y, action=None) -> None:
        super().__init__(img, x, y)
        self.action = action


class Tileset:
    def __init__(self, filename) -> None:
        self.filename = filename

        self.tiles = []

    def get_tiles(self) -> list:
        return self.tiles
    
    def parse_tileset(self) -> None:
        with open(self.filename) as tset:
            root = parse(tset).getroot()
        
        for tile in root:
            if tile.tag == "grid":
                continue

            img_path = path.dirname(self.filename) + '/' + tile[0].attrib['source']

            image = resource.image(img_path)

            tile_id = int(tile.attrib['id'])
            while tile_id > len(self.tiles):
                self.tiles.append(None)
            self.tiles.append(image)


class Tilemap:
    def __init__(self, filename, screen_size) -> None:
        self.filename = filename
        self.screen_width, self.screen_height = screen_size

        self.tileset = None
        self.map = None

        self.batch = graphics.Batch()
        self.above_batch = graphics.Batch()
        self.tilemap_size = [0, 0]

        self.sprite_list = []

        self.tile_list = None

        self.parse_map()

    def set_screen_size(self, zoom) -> None:
        self.screen_width /= zoom
        self.screen_height /= zoom

    def parse_map(self) -> None:
        with open(self.filename) as tmap:
            root = parse(tmap).getroot()

        self.tilemap_size = [
            int(root.attrib['width']), 
            int(root.attrib['height'])
        ]

        self.tileset = Tileset(path.dirname(self.filename) + '/' + root[0].attrib['source'])
        self.tileset.parse_tileset()

        tile_list = self.tileset.get_tiles()

        self.tilemap = []

        for i, layer in enumerate(root):
            if layer.tag == 'tileset':
                continue

            data = layer[0].text

            offset = 0

            layer_map = zeros((self.tilemap_size[0], self.tilemap_size[1]), dtype=object)

            for y, row in enumerate(data.split('\n')[1:-1]):
                tiles = row.split(',')[:-1]

                for x, tile in enumerate(tiles):
                    if tile == "0":
                        continue

                    tile_id = int(tile) - 1 + offset

                    condition = True
                    while condition:
                        try:
                            tile_sprite = Tile(
                                tile_list[tile_id],
                                x * 16 + self.screen_width // 2 - x * 16, 
                                y * 16 + self.screen_height // 2 - y * 16)
                            if i < 3:
                                tile_sprite.batch = self.batch
                            else:
                                tile_sprite.batch = self.above_batch
                            layer_map[x, self.tilemap_size[1] - y - 1] = tile_sprite
                            condition = False
                        except KeyError:
                            offset += 1

            self.tilemap.append(layer_map)

    def adjust_position(self, player_pos) -> None:
        x, y = player_pos

        for layer in self.tilemap:
            for i, row in enumerate(layer):
                for j, tile in enumerate(row):
                    if tile == 0:
                        continue

                    tile.x = i * 16 + self.screen_width // 2 - x * 16
                    tile.y = j * 16 + self.screen_height // 2 - y * 16
    
    def get_tile(self, position: tuple, layer: int) -> Tile | int:
        if position[0] <= -1 or position[1] <= -1:
            return 0
        try:
            return self.tilemap[layer][position]
        except IndexError:
            return 0
    
    def test_collisions(self, pos: list, direction: int) -> bool:
        match direction:
            # moving up
            case 0: 
                tiles = [(round(pos[0]), ceil(pos[1]))]

                if pos[0] - floor(pos[0]) <= 0.25:
                    tiles.append((round(pos[0]) - 1, ceil(pos[1])))
                elif pos[0] - floor(pos[0]) >= 0.75:
                    tiles.append((round(pos[0]) + 1, ceil(pos[1])))
            # moving down
            case 1:
                tiles = [(round(pos[0]), floor(pos[1] - 0.5))]
                
                if pos[0] - floor(pos[0]) <= 0.25:
                    tiles.append((round(pos[0]) - 1, floor(pos[1] - 0.5)))
                elif pos[0] - floor(pos[0]) >= 0.75:
                    tiles.append((round(pos[0]) + 1, floor(pos[1] - 0.5)))
            # moving left
            case 2:
                tiles = [(floor(pos[0] - 0.75), floor(pos[1] - 0.25))]

                if pos[1] - floor(pos[1]) >= 0.5:
                    tiles.append((floor(pos[0] - 0.75), floor(pos[1] - 0.25) + 1))
            # moving right
            case 3:
                tiles = [(ceil(pos[0]), floor(pos[1] - 0.25))]

                if pos[1] - floor(pos[1]) >= 0.5:
                    tiles.append((ceil(pos[0]), floor(pos[1] - 0.25) + 1))
        
        #log(pos)
        #log(tiles)

        for tile in tiles:
            if self.get_tile(tile, 1) != 0:
                return True
        return False
    
    def load_new_tilemap(self, filename) -> None:
        self.filename = filename
        
        self.tileset = None
        self.map = None

        self.batch = graphics.Batch()
        self.above_batch = graphics.Batch()
        self.tilemap_size = [0, 0]

        self.sprite_list = []

        self.tile_list = None

        self.parse_map()


