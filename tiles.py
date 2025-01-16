from pyglet import resource, sprite, graphics
from xml.etree.ElementTree import parse


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

            self.batch = graphics.Batch()
            self.sprite_list = []
            
            for y, row in enumerate(data.split('\n')[1:-1]):
                tiles = row.split(',')[:-1]

                offset = 0
                
                for x, tile in enumerate(tiles):
                    tile_id = int(tile) - 1

                    condition = True
                    while condition:
                        try:
                            tile_sprite = sprite.Sprite(
                                self.tile_list[tile_id + offset], 
                                x * 16 + self.position[0], 
                                y * 16 + self.position[1],
                                batch=self.batch)
                            self.sprite_list.append(tile_sprite)
                            condition = False
                        except KeyError:
                            offset += 1
                

    def adjust_position(self, player_pos) -> None:
        x, y = player_pos
        self.position = [
            self.screen_width // 2 - x * 16,
            self.screen_height // 2 - y * 16
        ]

        for i, tile in enumerate(self.sprite_list):
            tile.x = i % self.tilemap_size[0] * 16 + self.position[0]
            tile.y = 2 * self.tilemap_size[1] - (i // self.tilemap_size[0]) * 16 + self.position[1]

