import pyglet
import xml.etree.ElementTree as ET


class Tileset:
    def __init__(self, filename):
        self.filename = filename

        self.tiles = {}

    def get_tiles(self):
        return self.tiles
    
    def parse_tileset(self):
        with open(self.filename) as tset:
            root = ET.parse(tset).getroot()
        
        for tile in root:
            if tile.tag == "grid":
                continue

            path_to_tsx = self.filename
            while path_to_tsx[-1] != '/':
                path_to_tsx = path_to_tsx[:-1]

            path = path_to_tsx + tile[0].attrib['source']

            image = pyglet.resource.image(path)

            self.tiles[int(tile.attrib['id'])] = image

class Tilemap:
    def __init__(self, filename, screen_size):
        self.filename = filename
        self.screen_width, self.screen_height = screen_size

        self.tileset = None
        self.map = []
        self.position = [self.screen_width // 2, self.screen_height // 2]

        self.tilemap_size = [0, 0]

        self.parse_map()

    def draw(self):
        
        for i in range(0, self.tilemap_size[1] - 1):
            for j in range(0, self.tilemap_size[0] - 1):
                self.tile_dict[self.map[i][j]].blit(j * 16 + self.position[0],
                                               i * 16 + self.position[1])
                
    def parse_map(self):
        with open(self.filename) as tmap:
            root = ET.parse(tmap).getroot()

        self.tilemap_size = [
            int(root.attrib['width']), 
            int(root.attrib['height'])
        ]


        self.tileset = Tileset(root[0].attrib['source'].replace('..', 'assets'))

        self.tileset.parse_tileset()


        self.tile_dict = self.tileset.get_tiles()
        
        for layer in root:
            if layer.tag == 'tileset':
                continue

            data = layer[0].text
            layer_size = layer.attrib['width'], layer.attrib['height']

            
            for row in data.split('\n')[1:-1]:
                tiles = row.split(',')[:-1]

                offset = 0
                
                self.map.append([])
                
                for tile in tiles:
                    tile_id = int(tile) - 1

                    condition = True
                    while condition:
                       try:
                           self.map[-1].append(tile_id + offset)
                           condition = False
                       except KeyError:
                           offset += 1


    def adjust_position(self, player_pos) -> None:
        x, y = player_pos
        self.position = [
            self.screen_width // 2 - x * 16,
            self.screen_height // 2 - y * 16
        ]
    