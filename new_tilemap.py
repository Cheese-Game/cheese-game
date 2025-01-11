import pytmx
import pyglet


class Tilemap:
    def __init__(self, filename, screen_size):
        self.tiled_map = pytmx.TiledMap(filename)
        self.screen_width, self.screen_height = screen_size

        self.position = [self.screen_width // 2, self.screen_height // 2]

        self.tiles = []

        self.get_images()

    def get_images(self):
        for layer in self.tiled_map.layers:
            for tile in layer.tiles():
                tile_image = pyglet.resource.image(tile[2][0].replace('tilemap\\../', '').replace('\\', '/'))
                self.tiles.append((tile_image, (tile[0], tile[1])))

    def draw(self):
        for tile in self.tiles:
            x, y = tile[1][0], tile[1][1]
            tile[0].blit(x * 16 + self.position[0],
                         y * 16 + self.position[1])

    def adjust_position(self, player_pos) -> None:
        x, y = player_pos
        self.position = [
            self.screen_width // 2 - x * 16,
            self.screen_height // 2 - y * 16
        ]

