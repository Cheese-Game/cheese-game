from pyglet import resource, sprite, graphics
from xml.etree.ElementTree import parse
from numpy import zeros
from math import floor, ceil

from logger import log


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

            path_to_tsx = self.filename
            while path_to_tsx[-1] != '/':
                path_to_tsx = path_to_tsx[:-1]

            path = path_to_tsx + tile[0].attrib['source']

            image = resource.image(path)

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
        self.tilemap_size = [0, 0]

        self.sprite_list = []

        self.tile_list = None

        self.parse_map()

    def set_screen_size(self, zoom) -> None:
        self.screen_width = self.screen_width/zoom
        self.screen_height = self.screen_height/zoom

    def parse_map(self) -> None:
        with open(self.filename) as tmap:
            root = parse(tmap).getroot()

        self.tilemap_size = [
            int(root.attrib['width']), 
            int(root.attrib['height'])
        ]

        self.tileset = Tileset(root[0].attrib['source'].replace('..', 'assets'))
        self.tileset.parse_tileset()

        tile_list = self.tileset.get_tiles()

        self.tilemap = []

        for layer in root:
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
                            tile_sprite = sprite.Sprite(
                                tile_list[tile_id],
                                x * 16 + self.screen_width // 2 - x * 16, 
                                y * 16 + self.screen_height // 2 - y * 16,
                                batch=self.batch)
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
    
    def get_tile(self, position: tuple, layer: int) -> sprite.Sprite | int:
        try:
            return self.tilemap[layer][position]
        except IndexError:
            return 0
    
    def test_collisions(self, pos: list, direction: int) -> bool:
        match direction:
            # moving up
            case 0: 
                tiles = [(round(pos[0]), floor(pos[1] + 1))]

                if pos[0] - floor(pos[0]) <= 0.25:
                    tiles.append((round(pos[0]) - 1, floor(pos[1] + 1)))
                elif pos[0] - floor(pos[0]) >= 0.75:
                    tiles.append((round(pos[0]) + 1, floor(pos[1] + 1)))
            # moving down
            case 1:
                tiles = [(round(pos[0]), ceil(pos[1] - 1))]
                
                if pos[0] - floor(pos[0]) <= 0.25:
                    tiles.append((round(pos[0]) - 1, floor(pos[1] - 1)))
                elif pos[0] - floor(pos[0]) >= 0.75:
                    tiles.append((round(pos[0]) + 1, floor(pos[1] - 1)))
            # moving left
            case 2:
                tiles = [(ceil(pos[0] - 1), round(pos[1]))]

                if pos[1] - floor(pos[1]) <= 0.25:
                    tiles.append((floor(pos[0] - 1), round(pos[1]) + 1))
            # moving right
            case 3:
                tiles = [(floor(pos[0] + 1), round(pos[1]))]

                if pos[1] - floor(pos[1]) <= 0.25:
                    tiles.append((floor(pos[0] + 1), round(pos[1]) + 1))

        for tile in tiles:
            if self.get_tile(tile, 1) != 0:
                return True
        return False

