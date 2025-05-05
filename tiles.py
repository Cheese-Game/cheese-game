from pyglet import resource, sprite, graphics, image
from xml.etree.ElementTree import parse
from numpy import zeros
from math import floor, ceil
from os import path

from logger import log

class Tile(sprite.Sprite):
    def __init__(self, img: image.Texture, x: float, y: float, batch: graphics.Batch, action=None) -> None:
        super().__init__(img, x, y, batch=batch)
        self.action = action


class Tileset:
    def __init__(self, filename: str) -> None:
        self.filename = filename

        self.tiles = []

    def get_tiles(self) -> list[image.Texture]:
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
    CHUNK_SIZE = 16

    def __init__(self, filename: str, screen_size: tuple[int]) -> None:
        self.filename = filename
        self.screen_width, self.screen_height = screen_size

        self.tileset = None

        self.fg_batch = graphics.Batch()
        self.bg_batch = graphics.Batch()

        self.tilemap_size = [0, 0]

        self.sprite_list = []

        self.tile_list = None

        self.has_updated_x, self.has_updated_y = True, True
        self.previous_player_position: list[float] = [0.0, 0.0]

        self.parse_map()

    def set_screen_size(self, zoom: float) -> None:
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

        tile_list: list[image.Texture] = self.tileset.get_tiles()

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
                                img=tile_list[tile_id],
                                x=x * 16 + self.screen_width // 2 - x * 16, 
                                y=y * 16 + self.screen_height // 2 - y * 16,
                                batch=self.bg_batch if i < 3 else self.fg_batch)
                            layer_map[self.tilemap_size[1] - y - 1, x] = tile_sprite
                            condition = False
                        except KeyError:
                            offset += 1
                        except IndexError:
                            break

            self.tilemap.append(layer_map)

    def adjust_position(self, player_pos: list[float]) -> None:
        x, y = player_pos[0], player_pos[1]

        min_x = max(0, floor(x - self.screen_width/32 - 1))
        min_y = max(0, floor(y - self.screen_height/32 - 1))
        max_x = min(self.tilemap_size[0] - 1, ceil(x + self.screen_width/32 + 1))
        max_y = min(self.tilemap_size[1] - 1, ceil(y + self.screen_height/32 + 1))

        #log(self.previous_player_position, x, y, min_x, min_y, max_x, max_y)

        if self.previous_player_position[0] < x:
            for layer in self.tilemap:
                for tile in layer[min_y:max_y, min_x]:
                    if tile == 0:
                        continue
                    tile.batch = None
                for tile in layer[min_y:max_y, max_x]:
                    if tile == 0:
                        continue
                    tile.batch = self.bg_batch
                if x - self.previous_player_position[0] >= 0.5:
                    for tile in layer[min_y:max_y, max_x-1]:
                        if tile == 0:
                            continue
                        tile.batch = self.bg_batch
        elif self.previous_player_position[0] > x:
            for layer in self.tilemap:
                for tile in layer[min_y:max_y, min_x]:
                    if tile == 0:
                        continue
                    tile.batch = self.bg_batch
                for tile in layer[min_y:max_y, max_x]:
                    if tile == 0:
                        continue
                    tile.batch = None
                if self.previous_player_position[0] - x >= 0.5:
                    for tile in layer[min_y:max_y, min_x+1]:
                        if tile == 0:
                            continue
                        tile.batch = self.bg_batch
                
        if self.previous_player_position[1] < y:
            for layer in self.tilemap:
                for tile in layer[min_y, min_x:max_x]:
                    if tile == 0:
                        continue
                    tile.batch = None
                for tile in layer[max_y, min_x:max_x]:
                    if tile == 0:
                        continue
                    tile.batch = self.bg_batch
                if y - self.previous_player_position[1] >= 0.5:
                    for tile in layer[max_y-1, min_x:max_x]:
                        if tile == 0:
                            continue
                        tile.batch = self.bg_batch
        elif self.previous_player_position[1] > y:
            for layer in self.tilemap:
                for tile in layer[min_y, min_x:max_x]:
                    if tile == 0:
                        continue
                    tile.batch = self.bg_batch
                for tile in layer[max_y, min_x:max_x]:
                    if tile == 0:
                        continue
                    tile.batch = None
                if self.previous_player_position[1] - y >= 0.5:
                    for tile in layer[min_y+1, min_x:max_x]:
                        if tile == 0:
                            continue
                        tile.batch = self.bg_batch
        
        for layer in self.tilemap:
            for j, row in enumerate(layer[min_y:max_y], min_y):
                for k, tile in enumerate(row[min_x:max_x], min_x):
                    if tile == 0:   
                        continue
                    
                    tile.x = k * 16 + self.screen_width // 2 - x * 16
                    tile.y = j * 16 + self.screen_height // 2 - y * 16
        
        self.previous_player_position = [*player_pos]


    def get_tile(self, position: tuple, layer: int) -> Tile | int:
        if position[0] <= -1 or position[1] <= -1 or position[0] == self.tilemap_size[0] or position[1] > self.tilemap_size[1]:
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

        for tile in tiles:
            if self.get_tile(tile, 2) != 0:
                return True
        return False
    
    def load_new_tilemap(self, filename: str) -> None:
        self.filename = filename
        
        self.tileset = None

        self.batch = graphics.Batch()
        self.above_batch = graphics.Batch()
        self.tilemap_size = [0, 0]

        self.sprite_list = []

        self.tile_list = None

        self.parse_map()
