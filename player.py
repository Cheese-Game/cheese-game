from pyglet.resource import image


class Player:
    SPEED = 16.0

    def __init__(self, sprite_path, screen_size) -> None:
        self.screen_width, self.screen_height = screen_size
        self.position = [0.0, 0.0]
        self.sprites = PlayerSprites(sprite_path)
        self.sprite = self.sprites.sprite_front_default
        self.inventory = []
     
    def set_screen_size(self, zoom) -> None:
        self.screen_width = self.screen_width / zoom
        self.screen_height = self.screen_height / zoom
    
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
        self.sprite.blit(self.screen_width / 2, self.screen_height / 2)

    def give(self, item, count, *args, **kwargs):
        for i in self.inventory:
            if i['item'] == item:
                i['count'] += count
                return
        properties = kwargs.get('properties', None)
        if properties is not None:
            self.inventory.append({"item": item, "count": count, "properties": properties})
        else:
            self.inventory.append({"item": item, "count": count})


class PlayerSprites:
    def __init__(self, sprite_path) -> None:
        self.sprite_path_front_default = sprite_path + 'front-default.png'
        self.sprite_path_back_default = sprite_path + 'back-default.png'
        self.sprite_path_left_default = sprite_path + 'left-default.png'
        self.sprite_path_right_default = sprite_path + 'right-default.png'

        self.sprite_front_default = image(self.sprite_path_front_default)
        self.sprite_back_default = image(self.sprite_path_back_default)
        self.sprite_left_default = image(self.sprite_path_left_default)
        self.sprite_right_default = image(self.sprite_path_right_default)
