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
    milk = False

    def __init__(self) -> None:
        pyglet.app.run()
        log("Game running")


window = pyglet.window.Window(*Game.SIZE, vsync=False)
window.view = window.view.scale((Game.zoom, Game.zoom, 1.0))
window.set_caption("Cheese Game")
window.set_icon(pyglet.resource.image("assets/sprites/player/front-default.png"))
Game.zoom = 2.0
window.set_mouse_cursor(window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR))
#set_handle()


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
    
    if hud.popup is not None:
        hud.popup.draw()

    for child in child_flock:
          child.update(child_flock, player.get_pos())
    child_batch.draw()

def zoom(recip=False) -> None:
    log("zoom")
    if recip:
        player.set_screen_size(1/Game.zoom)
        tilemap.set_screen_size(1/Game.zoom)
        hud.set_screen_size(1/Game.zoom)
        cow.set_screen_size(1/Game.zoom)
    else:
        player.set_screen_size(Game.zoom)
        tilemap.set_screen_size(Game.zoom)
        hud.set_screen_size(Game.zoom)
        cow.set_screen_size(Game.zoom)

    if hud.inventory_open:
        hud.close_inventory()


@window.event
def on_key_press(symbol, modifiers) -> None:
    if symbol == pyglet.window.key.W:
        pyglet.clock.schedule_interval(player.move_up, 1 / 60.0)
    elif symbol == pyglet.window.key.A:
        pyglet.clock.schedule_interval(player.move_left, 1 / 60.0)
    elif symbol == pyglet.window.key.S:
        pyglet.clock.schedule_interval(player.move_down, 1 / 60.0)
    elif symbol == pyglet.window.key.D:
        pyglet.clock.schedule_interval(player.move_right, 1 / 60.0)
    elif (symbol == pyglet.window.key.PLUS or (symbol == pyglet.window.key.EQUAL and modifiers and pyglet.window.key.MOD_SHIFT)) and Game.zoom < 3.0:
        window.view = window.view.scale((Game.zoom, Game.zoom, Game.zoom))
        Game.totalzoom *= Game.zoom
        zoom()
    elif symbol == pyglet.window.key.MINUS and Game.zoom > 0.101:
        window.view = window.view.scale((1/Game.zoom, 1/Game.zoom, Game.zoom))
        Game.totalzoom /= Game.zoom
        zoom(True)
    elif symbol == pyglet.window.key.EQUAL:
        Game.zoom = 1.0 / Game.totalzoom
        window.view = window.view.scale((Game.zoom, Game.zoom, Game.zoom))
        zoom()
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
    elif symbol == pyglet.window.key.M:
        playerpos = player.get_pos()
        cowpos = cow.get_pos()

        if playerpos[0] > cowpos[0]+2 or playerpos[0] < cowpos[0]-2 or playerpos[1] > cowpos[1]+2 or playerpos[1] < cowpos[1]-2:
            hud.close_popup()
            return
        
        if Game.milk:
            hud.close_popup()
        else:
            hud.create_popup(0, (Game.SIZE[0]/2-128), (Game.SIZE[1]/2-64), 256, 128)
            hud.milkingmini()
            window.set_mouse_cursor(window.get_system_mouse_cursor(window.CURSOR_HAND))
        Game.milk = not Game.milk
        

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

player = Player('assets/sprites/player/', Game.SIZE, tilemap)
player.give(item.MUG, 1)
player.set_held_item(0)
player.set_screen_size(1)

cow = Cow(3.0, 3.0, 10, 10, Game.SIZE)

hud = Hud(Game.SIZE, player,window)

child_flock = []

x_positions = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y_positions = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
x_velocities = [-20, -5, -15, -10, -5, 5, 10, 15, 20, 5]
y_velocities = [-25, -20, -15, -10, -5, 5, 10, 15, 20, 25]

shuffle(x_positions)
shuffle(y_positions)
shuffle(x_velocities)
shuffle(y_velocities)

child_batch = pyglet.graphics.Batch()

for i in range(10):
    child_flock.append(
        Child(x_positions[i], y_positions[i], 
              x_velocities[i], y_velocities[i],
              child_batch, Game.SIZE))

held_movement_keys = []

game = Game()
