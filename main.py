import pyglet
import math

from pyglet.graphics.shader import _introspect_uniforms
from pyglet.window.key import C

import item
import cursor

from item import Item
from sound import Music_manager
from cheeses import Cheeses
from player import Player
from tiles import Tilemap
from logger import log
from npc import NPC_Manager, NPC
from hud import Hud
from minigame import Minigame
from lang import Lang

class Game:
    #draining fix. explained in the segment
    SIZE = 640, 480
    zoom = 1.0 
    totalzoom = 1.0
    milk = False
    colourexists=False
    drainrotation=0.0
    dragintensity = 0
    x1 = 0
    rectangle = pyglet.shapes.Rectangle(1,1,1,1,(0,0,0,0))
    y1 = 0
    minigameopen = False


    def __init__(self) -> None:
        pyglet.app.run()


lang = Lang("en-gb")

window = pyglet.window.Window(*Game.SIZE, vsync=False, caption=lang.get_string("name"))
window.view = window.view.scale((Game.zoom, Game.zoom, 1.0))
window.set_icon(pyglet.resource.image("assets/sprites/player/front-default.png"))
Game.zoom = 2.0

cursor.set_cursor(window, cursor.CROSSHAIR)

pyglet.options['debug_graphics_batch'] = True


@window.event
def on_draw():
    window.clear()
    pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D,
                              pyglet.gl.GL_TEXTURE_MAG_FILTER,
                              pyglet.gl.GL_NEAREST)

    tilemap.adjust_position(player.get_pos())

    tilemap.bg_batch.draw()
    player.draw()
    npcs.draw(player.get_pos())
    tilemap.fg_batch.draw()
    hud.hud_batch.draw()
    fps_display.draw()

    #log(hud.active_gui_batches)
    for elem in hud.active_gui_components:
        elem.draw()

    if minigame.instruction == "create-dialog":
        minigame.kneadmininit=False
        minigame.milkingmininit=False
        hud.create_dialog((Game.SIZE[0] / 2 - 128) * Game.totalzoom, (Game.SIZE[1] / 2 - 64) * Game.totalzoom, 256,128,player)
        minigame.minigameselector(hud,cheeses)
        Game.minigameopen=True
        minigame.instruction = ""

    if hud.dialog is not None and hasattr(minigame, "nailsprite"):
        if minigame.nailsprite is not None:
            minigame.nailsprite.draw()

    else:
        Game.minigameopen=False
        minigame.kneadmininit=False
        minigame.milkingmininit=False
        minigame.dialog_components.clear()
        minigame.kneadingcheese=None
        minigame.uddersprite=None
        minigame.kneadingbtn=None
        minigame.drainingbtn=None
        minigame.hotbtn=None
        minigame.finishbtn=None
        if hasattr(minigame,"nailsprite"):
            minigame.nailsprite=None
    minigame.secssincehot=minigame.secssincehot+1
    if minigame.secssincehot>90:
        minigame.hot=False


def zoom(recip: bool=False) -> None:
    z = 1 / Game.zoom if recip else Game.zoom

    player.set_screen_size(z)
    tilemap.set_screen_size(z)
    minigame.set_screen_size(z)
    hud.set_screen_size(z)
    npcs.set_screen_size(z)
    hud.close_dialog(player)
    hud.close_inventory()

    if hud.inventory_open:
        hud.close_inventory()
    if hud.dialog is not None:
        hud.close_dialog(player)

@window.event
def on_mouse_scroll(x,y,scroll_x,scroll_y):
    if  minigame.kneadmininit and Game.minigameopen and minigame.hot:
        minigame.totalscroll=minigame.totalscroll+scroll_y*10
        if 1+minigame.totalscroll/300<minigame.lowest:
            minigame.lowest=1+minigame.totalscroll/300
        if 1+minigame.totalscroll/300>minigame.highest:
            minigame.highest=1+minigame.totalscroll/300
        if minigame.totalscroll>=-120 and minigame.totalscroll<400:
            minigame.kneadingcheese.update(scale_x=1+minigame.totalscroll/300, scale_y=(1/(1+minigame.totalscroll/300)),x=(Game.SIZE[0]/2-128*(1+minigame.totalscroll/300))*Game.totalzoom,y=(Game.SIZE[1]/2-64/(1+minigame.totalscroll/300))*Game.totalzoom)
        elif minigame.totalscroll>400:
            minigame.kneadingcheese.image=pyglet.resource.image("assets/sprites/hud/minigame/curdincloth.png",atlas=True)
            print("cheese was broken :(")
            minigame.totalscroll=0
            minigame.kneadmininit=False
            minigame.highest=1.1
            minigame.kneadval=(minigame.highest-minigame.lowest)/1.7333

            minigame.kneadingcheese.update(scale_x=1,scale_y=1,x=minigame.corner1[0],y=minigame.corner1[1])
        elif minigame.totalscroll< -120 and minigame.hot:
            minigame.totalscroll=-115
            if minigame.secssincehot>8.5:
                minigame.hot=False
    elif not minigame.hot and minigame.kneadmininit: 

        minigame.kneadval=(minigame.highest-minigame.lowest)/1.7333
        minigame.kneadmininit=False



@window.event        
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT and minigame.milkingmininit:
        if Game.milk:
            colour=(255, 163, 177)
        else:
            colour=(255,255,1)
        if Game.dragintensity == 0:
            Game.x1, Game.y1 = x, y
            Game.colourexists=minigame.fetch_colour(x, y)
        if Game.colourexists:
            Game.rectangle.opacity=0
            Game.dragintensity = Game.dragintensity + 1

            if y-Game.y1<0 and Game.milk:
                if (((x-Game.x1)**2+(y-Game.y1)**2)**0.5) >= 100:
                    Game.rectangle = pyglet.shapes.Rectangle(Game.x1, Game.y1, (8.4), (-100), color=colour, batch=hud.get_dialog_batch()[0])

                else:
                    Game.rectangle = pyglet.shapes.Rectangle(Game.x1, Game.y1, (12/(((x-Game.x1)**2+(y-Game.y1)**2)**0.5)**0.096689), -(((x-Game.x1)**2+(y-Game.y1)**2)**0.5), color=colour, batch=hud.get_dialog_batch()[0])

                Game.rectangle.rotation=math.degrees(math.atan((x-Game.x1)/(y-Game.y1)))


                hud.get_dialog_batch()[1].append(Game.rectangle)
            elif not Game.milk :
                pivot=[Game.SIZE[0]/2,Game.SIZE[1]/2+64]
                if ((pivot[0]-x)**2+(pivot[1]-y)**2)**0.5/((pivot[0]-Game.x1)**2+(pivot[1]-Game.y1)**2)**0.5 == 1.5 and y-Game.y1<0:
                    scaley=1.5
                    scalex=1/scaley


                else:
                    scaley=((pivot[0]-x)**2+(pivot[1]-y)**2)**0.5/((pivot[0]-Game.x1)**2+(pivot[1]-Game.y1)**2)**0.5
                    scalex=1/scaley

                if scalex>=(1.5):
                    scaley=(2/3)
                    scalex=1/scaley
                placeholder=(pivot[0]-Game.x1)**2+(pivot[1]-Game.y1)**2
                placeholder=placeholder**0.5


                asq=placeholder**2
                bsq=(placeholder*scaley)**2
                csq=(((Game.x1-x)**2+(Game.y1-y)**2))
                if float(csq)>0.0 and float(bsq)>0.0 and float(asq)>0.0 and -1<((asq+bsq-csq)/2/asq**0.5/bsq**0.5)<1:
                    print(math.degrees(math.acos((asq+bsq-csq)/2/asq**0.5/bsq**0.5)))
                    Game.drainrotation=(math.degrees(math.acos((asq+bsq-csq)/2/asq**0.5/bsq**0.5)))
                else:
                    Game.drainrotation=0.0
                if x>pivot[0]:
                    Game.drainrotation=-Game.drainrotation





                minigame.uddersprite.update(scale_x=scalex, scale_y=-scaley,x=(Game.SIZE[0]/2)*Game.totalzoom,y=(Game.SIZE[1]/2+64)*Game.totalzoom, rotation=Game.drainrotation)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        # get nearest interactable thing
        nearest_npc = None
        for npc in npcs.npc_list:
            if isinstance(npc, NPC): # checks if is human npc
                dist_to_npc = ((npc.get_pos()[0] - player.get_pos()[0]) ** 2 + (npc.get_pos()[1] - player.get_pos()[1]) ** 2) ** 0.5
                if (nearest_npc is None or dist_to_npc < nearest_npc[1]) and dist_to_npc < 2:
                    nearest_npc = (npc, dist_to_npc)
        if nearest_npc is not None:
            nearest_npc[0].interact(hud, player)
        else:
            log("No interactable NPCs nearby")

@window.event
def on_mouse_release(x, y, button, modifiers):
    if Game.dragintensity != 0:
        Game.rectangle.opacity=0
        Game.drainrotation=0.0
        minigame.getmousepos(Game.x1, Game.y1, Game.dragintensity,hud)
        minigame.uddersprite.update(scale_x=1, scale_y=-1,x=((Game.SIZE[0]/2)*Game.totalzoom),y=(Game.SIZE[1]/2+64) *Game.totalzoom,rotation=Game.drainrotation)
        minigame.totaldrag=minigame.totaldrag+Game.dragintensity
        Game.dragintensity = 0



@window.event
def on_key_press(symbol, modifiers) -> None:
    #normalisation? why would anyone do this
    if symbol == pyglet.window.key.W:
        pyglet.clock.schedule_interval(player.move_up, 1 / 60.0, music_manager)
    elif symbol == pyglet.window.key.A:
        pyglet.clock.schedule_interval(player.move_left, 1 / 60.0, music_manager)
    elif symbol == pyglet.window.key.S:
        pyglet.clock.schedule_interval(player.move_down, 1 / 60.0, music_manager)
    elif symbol == pyglet.window.key.D:
        pyglet.clock.schedule_interval(player.move_right, 1 / 60.0, music_manager)
    elif (symbol == pyglet.window.key.PLUS or
          (symbol == pyglet.window.key.EQUAL and modifiers
           and pyglet.window.key.MOD_SHIFT)) and Game.totalzoom < 3.0:
        window.view = window.view.scale((Game.zoom, Game.zoom, 1))
        Game.totalzoom = Game.totalzoom * Game.zoom
        zoom()
    elif symbol == pyglet.window.key.MINUS and Game.totalzoom > 0.101:
        window.view = window.view.scale(
            (1 / Game.zoom, 1 / Game.zoom, 1))
        Game.totalzoom /= Game.zoom
        zoom(recip=True)
    elif symbol == pyglet.window.key.EQUAL:
        Game.zoom = 1.0 / Game.totalzoom 
        #reverses the zoom completely
        log(Game.zoom)
        window.view = window.view.scale((Game.zoom, Game.zoom, 1))
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
        hud.create_dialog((Game.SIZE[0] / 2 - 128) * Game.totalzoom,
             (Game.SIZE[1] / 2 - 64) * Game.totalzoom, 256,
             128,player)
        minigame.minigameselector(hud,cheeses)
        Game.minigameopen=True

    elif symbol == pyglet.window.key.M:
        playerpos = player.get_pos()
        cowpos = npcs.cow.get_pos()

        if (playerpos[0]<=cowpos[0]+2 and playerpos[0]>=cowpos[0]-2 and playerpos[1]<=cowpos[1]+2 and playerpos[1]>=cowpos[1]-2):
            if Game.milk:

                hud.close_dialog(player)
            else:
                hud.create_dialog((Game.SIZE[0] / 2 - 128) * Game.totalzoom,
                             (Game.SIZE[1] / 2 - 64) * Game.totalzoom, 256,
                             128,player)
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
music_manager = Music_manager(Game.SIZE)
cheeses=Cheeses()
music_manager.update_area("europe","Europe")

npcs = NPC_Manager(Game.SIZE, player, tilemap)

game = Game()
