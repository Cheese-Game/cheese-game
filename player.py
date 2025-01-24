from pyglet.resource import image
from pyglet import sprite


class Player:
    SPEED = 16.0

    def __init__(self, sprite_path, screen_size) -> None:
        self.screen_width, self.screen_height = screen_size
        self.position = [0.0, 0.0]
        self.sprites = PlayerSprites(sprite_path, screen_size)
        self.sprite = self.sprites.sprite_front_default
        self.inventory = []
        self.current_item = None
     
    def set_screen_size(self, zoom) -> None:
        self.screen_width = self.screen_width / zoom
        self.screen_height = self.screen_height / zoom

        self.sprites.set_screen_size(self.screen_width, self.screen_height)
    
    def get_pos(self) -> list[float]:
        return self.position

    def set_pos(self, x, y) -> None:
        self.position = [x, y]

    def reset_pos(self) -> None:
        self.position = [0.0, 0.0]

    def move_up(self, dt) -> None:
        self.position[1] += int(Player.SPEED * dt * 4) / 4
        self.sprite = self.sprites.sprite_back_default
        
    def move_down(self, dt) -> None:
        self.position[1] -= int(Player.SPEED * dt * 4) / 4
        self.sprite = self.sprites.sprite_front_default

    def move_left(self, dt) -> None:
        self.position[0] -= int(Player.SPEED * dt * 4) / 4
        self.sprite = self.sprites.sprite_left_default

    def move_right(self, dt) -> None:
        self.position[0] += int(Player.SPEED * dt * 4) / 4
        self.sprite = self.sprites.sprite_right_default

    def draw(self) -> None:
        self.sprite.draw()

    def give(self, item, count, properties=None):
        for i in self.inventory:
            if i['item'] == item:
                i['count'] += count
                return
        if properties is not None:
            self.inventory.append({"item": item, "count": count, "properties": properties})
        else:
            self.inventory.append({"item": item, "count": count})
    
    def set_held_item(self, index) -> None:
        self.current_item = self.inventory[index]
    
    def get_held_item(self) -> dict:
        return self.current_item

class PlayerSprites:
    def __init__(self, sprite_path, screen_size) -> None:
        self.screen_height, self.screen_width = screen_size

        path_front_default = sprite_path + 'front-default.png'
        path_back_default = sprite_path + 'back-default.png'
        path_left_default = sprite_path + 'left-default.png'
        path_right_default = sprite_path + 'right-default.png'

        img_front_default = image(path_front_default)
        img_back_default = image(path_back_default)
        img_left_default = image(path_left_default)
        img_right_default = image(path_right_default)

        self.sprite_front_default = sprite.Sprite(img_front_default, x=self.screen_width // 2, y=self.screen_height // 2)
        self.sprite_back_default = sprite.Sprite(img_back_default, x=self.screen_width // 2, y=self.screen_height // 2)
        self.sprite_left_default = sprite.Sprite(img_left_default, x=self.screen_width // 2, y=self.screen_height // 2)
        self.sprite_right_default = sprite.Sprite(img_right_default, x=self.screen_width // 2, y=self.screen_height // 2)
    
    def set_screen_size(self, screen_width, screen_height) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.sprite_front_default.x = self.screen_width // 2
        self.sprite_front_default.y = self.screen_height // 2
        self.sprite_back_default.x = self.screen_width // 2
        self.sprite_back_default.y = self.screen_height // 2
        self.sprite_left_default.x = self.screen_width // 2
        self.sprite_left_default.y = self.screen_height // 2
        self.sprite_right_default.x = self.screen_width // 2
        self.sprite_right_default.y = self.screen_height // 2
