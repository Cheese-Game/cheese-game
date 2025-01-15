from pyglet import resource
from xml.etree.ElementTree import parse
from numpy import zeros, fliplr, int16

import cProfile
import re


class Tileset:
    def __init__(self, filename):
        self.filename = filename

        self.tiles = []

    def get_tiles(self):
        return self.tiles
    
    def parse_tileset(self):
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
    def __init__(self, filename, screen_size):
        self.filename = filename
        self.screen_width, self.screen_height = screen_size

        self.tileset = None
        self.map = None
        self.position = [self.screen_width // 2, self.screen_height // 2]

        self.tilemap_size = [0, 0]

        self.parse_map()

    def get_screen_size(self, zoom):
        self.screen_width = self.screen_width/zoom
        self.screen_height = self.screen_height/zoom

    def draw(self):

        for i in range(0, self.tilemap_size[1] - 1):
            for j in range(0, self.tilemap_size[0] - 1):
                self.tile_list[self.map[j, i]].blit(j * 16 + self.position[0],
                                                    i * 16 + self.position[1])

    def parse_map(self):
        with open(self.filename) as tmap:
            root = parse(tmap).getroot()

        self.tilemap_size = [
            int(root.attrib['width']), 
            int(root.attrib['height'])
        ]

        self.tileset = Tileset(root[0].attrib['source'].replace('..', 'assets'))

        self.tileset.parse_tileset()

        self.tile_list = self.tileset.get_tiles()
        
        for layer in root:
            if layer.tag == 'tileset':
                continue

            data = layer[0].text
            layer_size = int(layer.attrib['width']), int(layer.attrib['height'])

            self.map = zeros(layer_size, int16)
            
            for y, row in enumerate(data.split('\n')[1:-1]):
                tiles = row.split(',')[:-1]

                offset = 0
                
                for x, tile in enumerate(tiles):
                    tile_id = int(tile) - 1

                    condition = True
                    while condition:
                        try:
                            self.map[x, y] = tile_id + offset
                            condition = False
                        except KeyError:
                            offset += 1
                           
        self.map = fliplr(self.map)

    def adjust_position(self, player_pos) -> None:
        x, y = player_pos
        self.position = [
            self.screen_width // 2 - x * 16,
            self.screen_height // 2 - y * 16
        ]

