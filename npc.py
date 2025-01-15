import math
import pyglet


class Child:
    MAX_SPEED = 50.0
    PERCEPTION_RADIUS = 40.0

    SOCIAL_ANXIETY_WEIGHT = 0.1
    PEER_PRESSURE_WEIGHT = 0.01
    ATTACHMENT_ISSUES_WEIGHT = 0.01

    def __init__(self, x, y, vx, vy, screen_size):
        self.position = [x, y]
        self.velocity = [vx, vy]

        self.screen_width, self.screen_height = screen_size

        self.sprite = pyglet.resource.image('assets/sprites/player/front-default.png')

    def get_pos(self):
        return self.position

    def draw(self, player_pos):
        x, y = player_pos
        self.sprite.blit(self.position[0] - x * 16,
                         self.position[1] - y * 16)

    def update(self, flock, player_pos):
        socialAnxiety = self.social_anxiety(flock)
        attachmentIssues = self.attachment_issues(flock)
        peerPressure = self.peer_pressure(flock)

        self.velocity[0] = (socialAnxiety[0] * Child.SOCIAL_ANXIETY_WEIGHT +
                            attachmentIssues[0] * Child.ATTACHMENT_ISSUES_WEIGHT +
                            peerPressure[0] * Child.PEER_PRESSURE_WEIGHT)

        self.velocity[1] = (socialAnxiety[1] * Child.SOCIAL_ANXIETY_WEIGHT +
                            attachmentIssues[1] * Child.ATTACHMENT_ISSUES_WEIGHT +
                            peerPressure[1] * Child.PEER_PRESSURE_WEIGHT)

        speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

        if speed > Child.MAX_SPEED:
            self.velocity[0] = (self.velocity[0] / speed) * Child.MAX_SPEED
            self.velocity[1] = (self.velocity[1] / speed) * Child.MAX_SPEED

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        self.draw(player_pos)

    def social_anxiety(self, flock):
        steering = [0.0, 0.0]
        total = 0

        for child in flock:
            distance = math.sqrt((self.position[0] - child.position[0])**2 + (self.position[1] - child.position[1])**2)
            if 0 < distance < Child.PERCEPTION_RADIUS:
                steering[0] += child.velocity[0]
                steering[1] += child.velocity[1]
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            speed = math.sqrt(steering[0]**2 + steering[1]**2)

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

    def attachment_issues(self, flock):
        steering = [0.0, 0.0]
        total = 0

        for child in flock:
            distance = math.sqrt((self.position[0] - child.position[0])**2 + (self.position[1] - child.position[1])**2)
            if 0 < distance < Child.PERCEPTION_RADIUS:
                steering[0] += child.position[0]
                steering[1] += child.position[1]
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            steering[0] -= self.position[0]
            steering[1] -= self.position[1]

            speed = math.sqrt(steering[0]**2 + steering[1]**2)

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

    def peer_pressure(self, flock):
        steering = [0.0, 0.0]
        total = 0

        for child in flock:
            diff = [self.position[0] - child.position[0], self.position[1] - child.position[1]]
            distance = math.sqrt(diff[0]**2 + diff[1]**2)
            if 0 < distance < Child.PERCEPTION_RADIUS:
                steering[0] += diff[0] / distance
                steering[1] += diff[1] / distance
                total += 1

        if total > 0:
            steering[0] /= total
            steering[1] /= total

            speed = math.sqrt(steering[0]**2 + steering[1]**2)

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

    