from math import sqrt
from pyglet import resource, sprite, clock, graphics
from random import randint, random, shuffle, choice
from json import load
from os import fsdecode, fsencode, listdir
from pathlib import Path

from logger import log


class NPC_Manager:
    def __init__(self, screen_size, player, tilemap) -> None:
        self.screen_width, self.screen_height = screen_size
        self.player = player
        self.tilemap = tilemap

        self.npc_list = []
        self.batch = graphics.Batch()

        self.initialise_children()
        self.initialise_cows()
        self.initialise_npcs()

    def initialise_children(self) -> None:
        x_positions = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        y_positions = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        x_velocities = [-20, -25, -15, -10, -5, 5, 10, 15, 20, 25]
        y_velocities = [-25, -20, -15, -10, -5, 5, 10, 15, 20, 25]

        shuffle(x_positions)
        shuffle(y_positions)
        shuffle(x_velocities)
        shuffle(y_velocities)

        self.child_flock = []

        for i in range(10):
            self.child_flock.append(Child(x_positions[i], y_positions[i], 
                                    x_velocities[i], y_velocities[i],
                                    self.batch, (self.screen_width, self.screen_height)))

        for child in self.child_flock:
            self.npc_list.append(child)

    def initialise_cows(self) -> None:
        self.cow = Cow(3.0, 3.0, 1, (self.screen_width, self.screen_height), self.batch, self.tilemap)

        self.npc_list.append(self.cow)

    def initialise_npcs(self) -> None:
        directory = fsencode(f"assets/npc_info/{self.player.current_tilemap}/")

        npcs = []

        for file in listdir(directory):
            npcs.append(f"{self.player.current_tilemap}/{Path(fsdecode(file)).stem}")

        for npc in npcs:
            self.npc_list.append(NPC(npc, 1.0, (self.screen_width, self.screen_height), self.batch, self.tilemap))

    def set_screen_size(self, zoom) -> None:
        self.screen_width /= zoom
        self.screen_height /= zoom

        for npc in self.npc_list:
            npc.set_screen_size(zoom)

    def draw(self, player_pos) -> None:
        self.batch.draw()

        for npc in self.npc_list:
            npc.update(self.child_flock, player_pos)

    def set_tilemap(self, name) -> None:
        self.cow = None
        for npc in self.npc_list:
            npc.batch = None
            del npc
        self.npc_list = []
        self.batch = graphics.Batch()


class NPC:
    def __init__(self, id: str, speed: float, screen_size, batch, tilemap) -> None:
        self.id = id
        self.speed = speed
        self.screen_width, self.screen_height = screen_size
        self.batch = batch
        self.tilemap = tilemap

        with open(f"assets/npc_info/{self.id}.json") as file:
            self.npc_info = load(file)

        self.position = [*self.npc_info['locations'][0]]

        self.image = resource.image(f'assets/sprites/npc/{self.id}.png', atlas=True)
        self.sprite = sprite.Sprite(self.image, x=self.position[0], y=self.position[1], batch=self.batch)

        clock.schedule_once(self.random_movement, randint(1, 5))

    def random_movement(self, _) -> None:
        target_location = choice(self.npc_info['locations'])

        while target_location == self.position:
            target_location = choice(self.npc_info['locations'])

        start = AStarNode(tuple(self.position), 0, 0)
        goal = AStarNode(tuple(target_location), 0, 0)

        astar = AStar(self.tilemap.tilemap[1])
        path = astar.search(start, goal)

        path_positions = []
        for tile in path:
            path_positions.append(tile.pos)

        log(path_positions)

        clock.schedule_interval(self.move, 1/60, path_positions, target_location)

    def set_screen_size(self, zoom) -> None:
        self.screen_width /= zoom
        self.screen_height /= zoom

    def update(self, _, player_pos) -> None:
        x, y = player_pos

        self.sprite.x = self.position[0] * 16 + self.screen_width // 2 - x * 16
        self.sprite.y = self.position[1] * 16 + self.screen_height // 2 - y * 16

    def move(self, dt, path, target) -> None:
        if self.position == target:
            clock.unschedule(self.move)
            clock.schedule_once(self.random_movement, randint(5, 10))
            return

        if path[0] == self.position:
            path.pop(0)

        distance = self.speed * dt

        vector_to_next_tile = self.position[0] - path[0][0], self.position[1] - path[0][1]
        distance_to_next_tile = abs(vector_to_next_tile[0] or vector_to_next_tile[1])

        if distance_to_next_tile < distance:
            self.position[0] = path[0][0]
            self.position[1] = path[0][1]

            distance -= distance_to_next_tile

            if len(path) > 1:
                path.pop(0)

                vector_to_next_tile = self.position[0] - path[0][0], self.position[1] - path[0][1]
                distance_to_next_tile = abs(vector_to_next_tile[0] or vector_to_next_tile[1])
            else:
                clock.unschedule(self.move)
                clock.schedule_once(self.random_movement, randint(5, 10))
                return

        if vector_to_next_tile[0] > 0:
            self.position[0] -= distance
        elif vector_to_next_tile[0] < 0:
            self.position[0] += distance

        if vector_to_next_tile[1] > 0:
            self.position[1] -= distance
        elif vector_to_next_tile[1] < 0:
            self.position[1] += distance



class Cow:
    def __init__(self, x, y, speed: float, screen_size, batch, tilemap) -> None:
        self.position = [x, y]
        self.speed = speed
        self.screen_width, self.screen_height = screen_size
        self.batch = batch
        self.tilemap = tilemap

        self.image = resource.image(f'assets/sprites/creature/cow{randint(1,2)}.png', atlas=True)

        self.sprite = sprite.Sprite(self.image, x=self.position[0], y=self.position[1], batch=self.batch)

        clock.schedule_once(self.random_movement, randint(1, 5))

    def random_movement(self, _) -> None:
        clock.schedule_interval_for_duration(self.move, 1/60, randint(1, 5), direction=randint(0, 3))

        clock.schedule_once(self.random_movement, randint(5, 15))

    def set_screen_size(self, zoom) -> None:
        self.screen_width /= zoom
        self.screen_height /= zoom

    def get_pos(self) -> list:
        return self.position

    def update(self, _, player_pos) -> None:
        x, y = player_pos

        self.sprite.x = self.position[0] * 16 + self.screen_width // 2 - x * 16
        self.sprite.y = self.position[1] * 16 + self.screen_height // 2 - y * 16

    def move(self, dt, direction) -> None:
        if not self.tilemap.test_collisions(self.position, direction):
            match direction:
                case 0:
                    self.position[0] += self.speed * dt
                case 1:
                    self.position[0] -= self.speed * dt
                case 2:
                    self.position[1] -= self.speed * dt
                case 3:
                    self.position[1] += self.speed * dt



class Child:
    MAX_SPEED = 40.0
    PERCEPTION_RADIUS = 100.0

    SOCIAL_ANXIETY_WEIGHT = 0.1
    PEER_PRESSURE_WEIGHT = 0.01
    ATTACHMENT_ISSUES_WEIGHT = 0.01

    def __init__(self, x, y, vx, vy, batch, screen_size) -> None:
        self.position = [x, y]
        self.velocity = [vx, vy]

        self.screen_width, self.screen_height = screen_size

        self.image = resource.image('assets/sprites/player/front-default.png', atlas=True)
        self.sprite = sprite.Sprite(self.image, x=self.position[0], y=self.position[1], batch=batch)

    def set_screen_size(self, zoom) -> None:
        self.screen_width /= zoom
        self.screen_height /= zoom

    def get_pos(self) -> list:
        return self.position

    def adjust_position(self, player_pos) -> None:
        x, y = player_pos

        self.sprite.x = self.screen_width // 2 - x * 16 + self.position[0]
        self.sprite.y = self.screen_height // 2 - y * 16 + self.position[1]

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

        self.adjust_position(player_pos)

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



class AStar:
    def __init__(self, map_grid):
        self.open = []
        self.closed = []
        self.map_grid = map_grid

    def search(self, start_node, goal_node):
        self.open.append(start_node)

        while self.open:
            self.open.sort()
            current_node = self.open[0]
            self.open.clear()

            self.closed.append(current_node)

            if current_node.pos == goal_node.pos:
                return self.reconstruct_path(current_node, start_node)

            neighbours = self.get_neighbours(current_node)

            for neighbour in neighbours:
                if neighbour in self.closed:
                    continue

                g_cost = current_node.g_cost + 1
                h_cost = self.heuristic(neighbour, goal_node)
                f_cost = g_cost + h_cost

                if neighbour in self.open:
                    if neighbour.f_cost > f_cost:
                        self.update_node(neighbour, g_cost, h_cost, current_node)
                else:
                    self.update_node(neighbour, g_cost, h_cost, current_node)
                    self.open.append(neighbour)

        return None

    def get_neighbours(self, node):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        neighbours = []

        for dir in dirs:
            neighbour_pos = (int(node.pos[0] + dir[0]), int(node.pos[1] + dir[1]))
            log(neighbour_pos)

            if (0 <= neighbour_pos[0] < self.map_grid.shape[0] and 0 <= neighbour_pos[1] < self.map_grid.shape[1]):
                if self.map_grid[neighbour_pos] == 0:
                    neighbours.append(AStarNode(neighbour_pos, 0, 0))

        return neighbours

    def heuristic(self, node, goal):
        d = (node.pos[0] - goal.pos[0]) ** 2 + (node.pos[1] - goal.pos[1]) ** 2
        return d

    def reconstruct_path(self, goal_node, start_node):
        path = [goal_node]
        current = goal_node

        while current.parent != start_node:
            path.append(current.parent)
            current = current.parent

        return path[::-1]

    def update_node(self, node, g_cost, h_cost, current_node):
        node.g_cost = g_cost
        node.h_cost = h_cost
        node.f_cost = g_cost + h_cost
        node.parent = current_node

class AStarNode:
    def __init__(self, pos: tuple, g_cost: float, h_cost: float):
        self.pos = pos
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = self.g_cost + self.h_cost

        self.parent = None

    def output_info(self):
        log(f"Node: {self.pos}, g_cost: {self.g_cost}, h_cost: {self.h_cost}, f_cost: {self.f_cost}, parent: {self.parent.pos if self.parent else None}")

    def __lt__(self, other):
        return self.f_cost < other.f_cost