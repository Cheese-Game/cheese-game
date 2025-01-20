import pyglet

from random import shuffle

import item

from player import Player
from tiles import Tilemap
from logger import log
from npc import Child, Cow
from hud import Hud


class Game:
    SIZE = 640, 480
    zoom = 1.0
    totalzoom = 1.0

    def __init__(self) -> None:
        pyglet.app.run()


pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

window = pyglet.window.Window(*Game.SIZE, vsync=False)
window.view = window.view.scale((Game.zoom, Game.zoom, 1.0))
Game.zoom = 2.0


@window.event
def on_draw():

    tilemap.adjust_position(player.get_pos())
    window.clear()
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

    tilemap.batch.draw()
    player.draw()
    cow.draw(player.get_pos()) 
    hud.hud_batch.draw()
    fps_display.draw()

    if hud.inventory_open:
        hud.inventory_batch.draw()

    # for child in child_flock:
    #      child.update(child_flock, player.get_pos())


@window.event
def on_key_press(symbol, _) -> None:
    if symbol == pyglet.window.key.W:
        pyglet.clock.schedule_interval(player.move_up, 1 / 60.0)
    elif symbol == pyglet.window.key.A:
        pyglet.clock.schedule_interval(player.move_left, 1 / 60.0)
    elif symbol == pyglet.window.key.S:
        pyglet.clock.schedule_interval(player.move_down, 1 / 60.0)
    elif symbol == pyglet.window.key.D:
        pyglet.clock.schedule_interval(player.move_right, 1 / 60.0)
    elif symbol == pyglet.window.key.PLUS and Game.zoom < 3.0:
        window.view = window.view.scale((Game.zoom, Game.zoom, Game.zoom))
        Game.totalzoom = Game.totalzoom * Game.zoom
        player.set_screen_size(Game.zoom)
        tilemap.set_screen_size(Game.zoom)
        hud.set_screen_size(Game.zoom)
        cow.set_screen_size(Game.zoom,player.get_pos())
        if hud.inventory_open:
            hud.close_inventory()
    elif symbol == pyglet.window.key.MINUS and Game.zoom > 0.101:
        window.view = window.view.scale((1/Game.zoom, 1/Game.zoom, Game.zoom))
        Game.totalzoom = Game.totalzoom / Game.zoom
        player.set_screen_size(1/Game.zoom)
        tilemap.set_screen_size(1/Game.zoom)
        hud.set_screen_size(Game.zoom)
        cow.set_screen_size(1/Game.zoom,player.get_pos())
        if hud.inventory_open:
            hud.close_inventory()
    elif symbol == pyglet.window.key.EQUAL:
        Game.zoom = 1.0 / Game.totalzoom
        window.view = window.view.scale((Game.zoom, Game.zoom, Game.zoom))
        player.set_screen_size(Game.zoom)
        tilemap.set_screen_size(Game.zoom)
        hud.set_screen_size(Game.zoom)
        cow.set_screen_size(Game.zoom,player.get_pos())
        if hud.inventory_open:
            hud.close_inventory()
        Game.zoom = 2.0
        Game.totalzoom = 1.0
    elif symbol == pyglet.window.key.B:
        pyglet.app.exit()
    elif symbol == pyglet.window.key.C:
        print(cow.get_pos())
    elif symbol == pyglet.window.key.E:
        if hud.inventory_open:
            hud.close_inventory()
        else:
            hud.open_inventory()


@window.event
def on_key_release(symbol, _) -> None:
    if symbol == pyglet.window.key.W:
        pyglet.clock.unschedule(player.move_up)
    elif symbol == pyglet.window.key.A:
        pyglet.clock.unschedule(player.move_left)
    elif symbol == pyglet.window.key.S:
        pyglet.clock.unschedule(player.move_down)
    elif symbol == pyglet.window.key.D:
        pyglet.clock.unschedule(player.move_right)


fps_display = pyglet.window.FPSDisplay(window=window)

tilemap = Tilemap('assets/tilemap/area1.tmx', Game.SIZE)

player = Player('assets/sprites/player/', Game.SIZE)

cow = Cow(400.0, 300.0, 10, 10, Game.SIZE)

hud = Hud(Game.SIZE, player)

child_flock = []

x_positions = [110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
y_positions = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
x_velocities = [-25, -20, -15, -10, -5, 5, 10, 15, 20, 25]
y_velocities = [-25, -20, -15, -10, -5, 5, 10, 15, 20, 25]

shuffle(x_positions)
shuffle(y_positions)
shuffle(x_velocities)
shuffle(y_velocities)

for i in range(10):
    child_flock.append(
        Child(x_positions[i], y_positions[i], 
              x_velocities[i], y_velocities[i],
              Game.SIZE))

held_movement_keys = []

player.give(item.MUG, 1)

game = Game()
