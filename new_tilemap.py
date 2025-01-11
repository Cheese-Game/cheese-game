import pytmx


class Tileset:
    def __init__(self, filename):
        self.filename = filename
        self.tiles = []


class Tilemap:
    def __init__(self, filename, screen_size):
        self.tiled_map = pytmx.TiledMap(filename)
        self.screen_width, self.screen_height = screen_size

        self.get_images()

        self.position = [self.screen_width // 2, self.screen_height // 2]

    def get_images(self):
        layers = self.tiled_map.layers
        for layer in layers:
            for tile in layer.tiles():
                print(tile[2])
                #tile.blit(tile[0] * 16 + self.position[0],
                #          tile[1] * 16 + self.position[1])


tm = Tilemap('assets/tilemap/area1.tmx', (640, 480))
