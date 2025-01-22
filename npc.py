from math import sqrt, acos
from pyglet import resource
from random import randint


class Cow:
    MAX_SPEED = 30.0

    def __init__(self, x, y, vx, vy, screen_size) -> None:
        self.position = [x, y]
        self.velocity = [vx, vy]

        self.screen_width, self.screen_height = screen_size

        self.sprite = resource.image(f'assets/sprites/creature/cow{randint(1,2)}.png', atlas=True)

    def set_screen_size(self, zoom, player_pos) -> None:
        self.screen_width = self.screen_width / zoom
        self.screen_height = self.screen_height / zoom

    def get_pos(self) -> list:
        return self.position

    def draw(self, player_pos) -> None:
        x, y = player_pos

        self.sprite.blit(self.screen_width // 2 - x * 16 + self.position[0] * 16,
                         self.screen_height // 2 - y * 16 + self.position[1] * 16)

    def set_direction(self, direction) -> None:
        self.velocity = [acos(direction), acos(direction)]

    def move(self, dt) -> None:
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


class Child:
    MAX_SPEED = 40.0
    PERCEPTION_RADIUS = 100.0

    SOCIAL_ANXIETY_WEIGHT = 0.1
    PEER_PRESSURE_WEIGHT = 0.01
    ATTACHMENT_ISSUES_WEIGHT = 0.01

    def __init__(self, x, y, vx, vy, screen_size) -> None:
        self.position = [x, y]
        self.velocity = [vx, vy]

        self.screen_width, self.screen_height = screen_size

        self.sprite = resource.image('assets/sprites/player/front-default.png', atlas=True)
        
    def get_screen_size(self, zoom) -> None:
        self.screen_width = self.screen_width / zoom
        self.screen_height = self.screen_height / zoom

    def get_pos(self) -> list:
        return self.position

    def draw(self, player_pos) -> None:
        x, y = player_pos
        self.sprite.blit(self.screen_width // 2 - x * 16 + self.position[0],
             self.screen_height // 2 - y * 16 + self.position[1])

    def update(self, flock, player_pos) -> None:
        socialAnxiety = self.social_anxiety(flock)
        attachmentIssues = self.attachment_issues(flock)
        peerPressure = self.peer_pressure(flock)

        self.velocity[0] = (socialAnxiety[0] * Child.SOCIAL_ANXIETY_WEIGHT +
                            attachmentIssues[0] * Child.ATTACHMENT_ISSUES_WEIGHT +
                            peerPressure[0] * Child.PEER_PRESSURE_WEIGHT)

        self.velocity[1] = (socialAnxiety[1] * Child.SOCIAL_ANXIETY_WEIGHT +
                            attachmentIssues[1] * Child.ATTACHMENT_ISSUES_WEIGHT +
                            peerPressure[1] * Child.PEER_PRESSURE_WEIGHT)

        speed = sqrt(self.velocity[0]**2 + self.velocity[1]**2)

        if speed > Child.MAX_SPEED:
            self.velocity[0] = (self.velocity[0] / speed) * Child.MAX_SPEED
            self.velocity[1] = (self.velocity[1] / speed) * Child.MAX_SPEED

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        self.draw(player_pos)

    def social_anxiety(self, flock) -> list:
        steering = [0.0, 0.0]
        total = 0

        for child in flock:
            distance = sqrt((self.position[0] - child.position[0])**2 + (self.position[1] - child.position[1])**2)
            if 0 < distance < Child.PERCEPTION_RADIUS:
                steering[0] += child.velocity[0]
                steering[1] += child.velocity[1]
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            speed = sqrt(steering[0]**2 + steering[1]**2)

            try:
                steering[0] = steering[0] / speed * Child.MAX_SPEED
            except ZeroDivisionError:
                steering[0] = 0

            try:
                steering[1] = steering[1] / speed * Child.MAX_SPEED
            except ZeroDivisionError:
                steering[1] = 0

            steering[0] -= self.velocity[0]
            steering[1] -= self.velocity[1]

        return steering

    def attachment_issues(self, flock) -> list:
        steering = [0.0, 0.0]
        total = 0

        for child in flock:
            distance = sqrt((self.position[0] - child.position[0])**2 + (self.position[1] - child.position[1])**2)
            if 0 < distance < Child.PERCEPTION_RADIUS:
                steering[0] += child.position[0]
                steering[1] += child.position[1]
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            steering[0] -= self.position[0]
            steering[1] -= self.position[1]

            speed = sqrt(steering[0]**2 + steering[1]**2)

            try:
                steering[0] = steering[0] / speed * Child.MAX_SPEED
            except ZeroDivisionError:
                steering[0] = 0

            try:
                steering[1] = steering[1] / speed * Child.MAX_SPEED
            except ZeroDivisionError:
                steering[1] = 0

            steering[0] -= self.velocity[0]
            steering[1] -= self.velocity[1]

        return steering
    
    def peer_pressure(self, flock) -> list:
        steering = [0.0, 0.0]
        total = 0

        for child in flock:
            diff = [self.position[0] - child.position[0], self.position[1] - child.position[1]]
            distance = sqrt(diff[0]**2 + diff[1]**2)
            if 0 < distance < Child.PERCEPTION_RADIUS:
                steering[0] += diff[0] / distance
                steering[1] += diff[1] / distance
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            speed = sqrt(steering[0]**2 + steering[1]**2)

            try:
                steering[0] = steering[0] / speed * Child.MAX_SPEED
            except ZeroDivisionError:
                steering[0] = 0

            try:
                steering[1] = steering[1] / speed * Child.MAX_SPEED
            except ZeroDivisionError:
                steering[1] = 0

            steering[0] -= self.velocity[0]
            steering[1] -= self.velocity[1]

        return steering

    