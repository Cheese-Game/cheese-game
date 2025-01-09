import pyglet


class Player:
    SPEED = 12.0

    def __init__(self, sprite_path, screen_size, tilemap):
        self.tilemap = tilemap
        self.screen_width, self.screen_height = screen_size

        self.position = [0.0, 0.0]
        self.sprites = PlayerSprites(sprite_path)
        self.sprite = self.sprites.sprite_front_default
        #self.sprite.opacity=50


    def get_pos(self):
        return self.position

    def set_pos(self, x, y):
        self.position = [x, y]

    def reset_pos(self):
        self.position = [0.0, 0.0]

    def move_up(self, dt):
        self.position[1] += Player.SPEED * dt
        self.sprite = self.sprites.sprite_back_default

    def move_down(self, dt):
        self.position[1] -= Player.SPEED * dt
        self.sprite = self.sprites.sprite_front_default

    def move_left(self, dt):
        self.position[0] -= Player.SPEED * dt
        self.sprite = self.sprites.sprite_left_default

    def move_right(self, dt):
        self.position[0] += Player.SPEED * dt
        self.sprite = self.sprites.sprite_right_default

    def draw(self):
        self.sprite.blit(self.screen_width // 2, self.screen_height // 2)
    

class PlayerSprites:
    def __init__(self, sprite_path):
      self.sprite_path_front_default = sprite_path + 'front-default.png'
      self.sprite_path_back_default = sprite_path + 'back-default.png'
      self.sprite_path_left_default = sprite_path + 'left-default.png'
      self.sprite_path_right_default = sprite_path + 'right-default.png'
    
      self.sprite_front_default = pyglet.resource.image(self.sprite_path_front_default)
      self.sprite_back_default = pyglet.resource.image(self.sprite_path_back_default)
      self.sprite_left_default = pyglet.resource.image(self.sprite_path_left_default)
      self.sprite_right_default = pyglet.resource.image(self.sprite_path_right_default)