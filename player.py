import pyglet

from camera import Camera


class Player:
  SPEED = 3

  def __init__(self, sprite_path, screen_size):
      self.screen_width, self.screen_height = screen_size

      self.position = [self.screen_width // 2, self.screen_height // 2]
      self.sprites = PlayerSprites(sprite_path)
      self.sprite = self.sprites.sprite_front_default

      self.camera = Camera(0, 0, 0)

  def get_pos(self):
      return self.position

  def set_pos(self, x, y):
      self.position = [x, y]

  def reset_pos(self):
      self.position = [self.screen_width // 2, self.screen_height // 2]
      self.camera.x = 0
      self.camera.y = 0

  def move(self, x, y):
      self.position[0] += x
      self.position[1] += y

      self.camera.x += x
      self.camera.y += y

  def draw(self):
      self.sprite.blit(self.position[0] - self.camera.x,
                       self.position[1] - self.camera.y)


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