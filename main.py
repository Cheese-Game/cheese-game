import pyglet
import math

import item
import cursor

from player import Player
from tiles import Tilemap
from logger import log
from npc import NPC_Manager
from hud import Hud
from minigame import Minigame
from lang import Lang

class Game:
    SIZE = 640, 480
    zoom = 1.0
    totalzoom = 1.0
    milk = False
    dragintensity = 0
    x1 = 0
    rectangle=pyglet.shapes.Rectangle(1,1,1,1,(0,0,0,0))
    y1 = 0
    minigameopen = False

    def __init__(self) -> None:
        pyglet.app.run()

        log("Game running")

lang = Lang("en-gb")

window = pyglet.window.Window(*Game.SIZE, vsync=False, caption=lang.get_string("name"))
window.view = window.view.scale((Game.zoom, Game.zoom, 1.0))
window.set_icon(
    pyglet.resource.image("assets/sprites/player/front-default.png"))
Game.zoom = 2.0

cursor.set_cursor(window, cursor.CROSSHAIR)


@window.event
def on_draw():
    tilemap.adjust_position(player.get_pos())
    window.clear()
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D,
                              pyglet.gl.GL_TEXTURE_MAG_FILTER,
                              pyglet.gl.GL_NEAREST)

    tilemap.batch.draw()
    player.draw()
    tilemap.above_batch.draw()
    npcs.draw(player.get_pos())
    hud.hud_batch.draw()
    fps_display.draw()

    if hud.inventory_open:
        hud.inventory_batch.draw()

    if hud.popup is not None:
        hud.popup.draw()
    else:
        Game.minigameopen=False

    


def zoom(recip=False) -> None:
    z = 1 / Game.zoom if recip else Game.zoom
    player.set_screen_size(z)
    tilemap.set_screen_size(z)
    minigame.set_screen_size(z)
    hud.set_screen_size(z)
    npcs.set_screen_size(z)
    hud.close_popup()
    hud.close_inventory()

    if hud.inventory_open:
        hud.close_inventory()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT and Game.minigameopen:
        if Game.milk:
            colour=(255, 163, 177)
        else:
            colour=(255,255,1)
        minigame.fetch_colour(x,y)
        if Game.dragintensity == 0:
            Game.x1, Game.y1 = x, y

        Game.rectangle.opacity=0
        Game.dragintensity = Game.dragintensity + 1
        if y-Game.y1<0:
            if (math.sqrt((x-Game.x1)**2+(y-Game.y1)**2)) >= 100:
                Game.rectangle = pyglet.shapes.Rectangle(Game.x1, Game.y1, (8.4), (-100), color=colour, batch=hud.getpopupbatch()[0])
            else:
                Game.rectangle = pyglet.shapes.Rectangle(Game.x1, Game.y1, (12/(math.sqrt((x-Game.x1)**2+(y-Game.y1)**2))**0.096689), (-(math.sqrt((x-Game.x1)**2+(y-Game.y1)**2))), color=colour, batch=hud.getpopupbatch()[0])
            Game.rectangle.rotation=math.degrees(math.atan((x-Game.x1)/(y-Game.y1)))
            
            hud.getpopupbatch()[1].append(Game.rectangle)


@window.event
def on_mouse_release(x, y, button, modifiers):
    if Game.dragintensity != 0:
        Game.rectangle.opacity=0
        minigame.getmousepos(Game.x1, Game.y1, Game.dragintensity,hud)
        
        Game.dragintensity = 0
        


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
    elif (symbol == pyglet.window.key.PLUS or
          (symbol == pyglet.window.key.EQUAL and modifiers
           and pyglet.window.key.MOD_SHIFT)) and Game.totalzoom < 3.0:
        window.view = window.view.scale((Game.zoom, Game.zoom, Game.zoom))
        Game.totalzoom *= Game.zoom
        zoom()
    elif symbol == pyglet.window.key.MINUS and Game.totalzoom > 0.101:
        window.view = window.view.scale(
            (1 / Game.zoom, 1 / Game.zoom, Game.zoom))
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
        if tilemap.filename == "assets/tiles/cheese_room/cheese_room.tmx":
            tilemap.load_new_tilemap(f"assets/tiles/{player.current_area}/{player.current_area}.tmx")
            player.current_tilemap = player.current_area
        else:
            tilemap.load_new_tilemap("assets/tiles/cheese_room/cheese_room.tmx")
            player.current_tilemap = "cheese_room"
        npcs.set_tilemap(player.current_tilemap)
    elif symbol == pyglet.window.key.E:
        if hud.inventory_open:
            hud.close_inventory()
        else:
            hud.open_inventory()
    elif symbol == pyglet.window.key.F:
        Game.milk=False
        hud.create_popup(0, (Game.SIZE[0] / 2 - 128) * Game.totalzoom,
             (Game.SIZE[1] / 2 - 64) * Game.totalzoom, 256,
             128)
        minigame.milkingmini("drain")
        Game.minigameopen=True
    elif symbol == pyglet.window.key.M:
        playerpos = player.get_pos()
        cowpos = npcs.cow.get_pos()

        if playerpos==cowpos or (playerpos[0]<cowpos[0]+32 and playerpos[0]>cowpos[0]-32 and playerpos[1]<cowpos[1]+32 and playerpos[1]>cowpos[1]-32):
            if Game.milk:
                hud.close_popup()
            else:
                hud.create_popup(0, (Game.SIZE[0] / 2 - 128) * Game.totalzoom,
                             (Game.SIZE[1] / 2 - 64) * Game.totalzoom, 256,
                             128)
                minigame.milkingmini("real")

                cursor.set_cursor(window, cursor.HAND)
                Game.minigameopen=True
            

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

tilemap = Tilemap('assets/tiles/europe/europe.tmx', Game.SIZE)

player = Player('assets/sprites/player/', Game.SIZE, tilemap)
player.give(item.MUG, 1)
player.set_held_item(0)
player.set_screen_size(1)

hud = Hud(Game.SIZE, player, window)
minigame = Minigame(hud)

npcs = NPC_Manager(Game.SIZE, player, tilemap)

held_movement_keys = []

game = Game()
