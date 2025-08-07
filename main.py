import pyglet
import math

from pyglet.graphics.shader import _introspect_uniforms
from pyglet.window.key import C

import item

from cursor import Cursor_Class
from random import randint
from item import Item
from sound import Music_manager
from cheeses import Cheeses
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
    colourexists=False
    drainrotation=0.0
    rectangle_exists=False
    dragintensity = 0
    x1 = 0
    y1 = 0
    minigameopen = False
    cursor_created=False
    

    def __init__(self) -> None:
        pyglet.app.run()
    
    def moo(self)-> None:
        distance=math.sqrt((player.get_pos()[0]-npcs.cow.get_pos()[0])**2+(player.get_pos()[1]-npcs.cow.get_pos()[1])**2)
        music_manager.distance_sfx("moo",distance)
        pyglet.clock.schedule_once(Game.moo,randint(5,10))

        



lang = Lang("en-gb")

window = pyglet.window.Window(*Game.SIZE, vsync=False, caption=lang.get_string("name"))
window.view = window.view.scale((Game.zoom, Game.zoom, 1.0))
window.set_icon(pyglet.resource.image("assets/logo.png"))
Game.zoom = 2.0




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
    
    
    

    if hud.inventory_open:
        hud.inventory_batch.draw()

    if minigame.instruction == "create-popup":
        minigame.kneadmininit=False
        minigame.milkingmininit=False
        hud.create_popup(0, (Game.SIZE[0] / 2 - 128) * Game.totalzoom,(Game.SIZE[1] / 2 - 64) * Game.totalzoom, 256,128,player)
        minigame.minigameselector(hud,cheeses)
        Game.minigameopen=True
        minigame.instruction = ""
    if hud.popup is not None:
        hud.popup.draw()
        if hasattr(minigame,"nailsprite"):
            if minigame.nailsprite is not None:
                minigame.nailsprite.draw()

    else:
        Game.minigameopen=False
        minigame.kneadmininit=False
        minigame.milkingmininit=False
        minigame.popup_components.clear()
        minigame.kneadingcheese=None
        minigame.uddersprite=None
        minigame.kneadingbtn=None
        minigame.drainingbtn=None
        minigame.hotbtn=None
        minigame.finishbtn=None
        if hasattr(minigame,"nailsprite"):
            minigame.nailsprite=None
    if Game.totalzoom != 1 and Game.cursor_created:
        Cursor.sprite.draw()

def zoom(recip: bool=False) -> None:
    z = 1 / Game.zoom if recip else Game.zoom
    Game.SIZE=Game.SIZE[0]/z,Game.SIZE[1]/z
    #please don't fix anything again, raffers
    player.set_screen_size(z)
    tilemap.set_screen_size(z)
    minigame.set_screen_size(z)
    hud.set_screen_size(z)
    npcs.set_screen_size(z)
    hud.close_popup(player)
    hud.close_inventory()
    Cursor.change_size(1/z,window)
    Cursor.set_cursor(window, Cursor.CROSSHAIR)
    if hud.inventory_open:
        hud.close_inventory()
@window.event
def on_mouse_motion(x,y,dx,dy):
    if Game.totalzoom !=1:
        #the best idea i have is to entirely replace the mouse with a new system, but it could be performance intensive
        Cursor.create_cursor(x/Game.totalzoom,y/Game.totalzoom)
        Game.cursor_created=True
        #window.set_mouse_visible(False)
        #^ is to reactivate once pushbuttons are fix
        #pushbuttons are a serious issue... 
        #udder-rectangle broken x when zoomed out
    else:
        window.set_mouse_visible(True)
        Game.cursor_created=False
@window.event
def on_mouse_scroll(x,y,scroll_x,scroll_y):
    Cursor.create_cursor(x/Game.totalzoom,y/Game.totalzoom)
    x=x/Game.totalzoom
    y=y/Game.totalzoom
    if  minigame.kneadmininit and Game.minigameopen and minigame.hot:
        minigame.totalscroll=minigame.totalscroll+scroll_y*10
        if 1+minigame.totalscroll/300<minigame.lowest:
            minigame.lowest=1+minigame.totalscroll/300
        if 1+minigame.totalscroll/300>minigame.highest:
            minigame.highest=1+minigame.totalscroll/300
        if minigame.totalscroll>=-120 and minigame.totalscroll<400:
            minigame.kneadingcheese.update(scale_x=1+minigame.totalscroll/300, scale_y=(1/(1+minigame.totalscroll/300)),x=(Game.SIZE[0]/2-128*(1+minigame.totalscroll/300)),y=(Game.SIZE[1]/2-64/(1+minigame.totalscroll/300)))
            print(minigame.kneadingcheese.scale_x,minigame.kneadingcheese.x)
            print(Game.SIZE[0])
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
            
    elif not minigame.hot and minigame.kneadmininit: 

        minigame.kneadval=(minigame.highest-minigame.lowest)/1.7333
        minigame.kneadmininit=False



@window.event        
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    Cursor.create_cursor(x/Game.totalzoom,y/Game.totalzoom)
    x=x/Game.totalzoom
    y=y/Game.totalzoom
    dx=dx/Game.totalzoom
    dy=dy/Game.totalzoom
    if buttons & pyglet.window.mouse.LEFT and minigame.milkingmininit:
        if Game.milk:
            colour=(255, 163, 177)
        else:
            colour=(255,255,1)
        if Game.dragintensity == 0:
            Game.x1, Game.y1 = x, y
            Game.colourexists=minigame.fetch_colour(x, y)
        if Game.colourexists:
            Game.dragintensity = Game.dragintensity + 1
            if minigame.udder=="real" and Game.rectangle_exists:
                    Game.rectangle.opacity=0
            if y-Game.y1<0 and Game.milk:
                if (((x-Game.x1)**2+(y-Game.y1)**2)**0.5) >= 100:
                    Game.rectangle = pyglet.shapes.Rectangle(Game.x1, Game.y1, (8.4), (-100), color=colour, batch=hud.getpopupbatch()[0])

                else:
                    Game.rectangle = pyglet.shapes.Rectangle(Game.x1, Game.y1, (12/(((x-Game.x1)**2+(y-Game.y1)**2)**0.5)**0.096689), -(((x-Game.x1)**2+(y-Game.y1)**2)**0.5), color=colour, batch=hud.getpopupbatch()[0])

                Game.rectangle.rotation=math.degrees(math.atan((x-Game.x1)/(y-Game.y1)))
                Game.rectangle_exists=True
                

                hud.getpopupbatch()[1].append(Game.rectangle)
                minigame.uddersprite.update(scale_x=1,scale_y=1, x=(Game.SIZE[0]/2-128),y=(Game.SIZE[1]/2-64))
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
                    Game.drainrotation=(math.degrees(math.acos((asq+bsq-csq)/2/asq**0.5/bsq**0.5)))
                else:
                    Game.drainrotation=0.0
                if x>pivot[0]:
                    Game.drainrotation=-Game.drainrotation
                minigame.uddersprite.update(scale_x=scalex, scale_y=-scaley,x=(Game.SIZE[0]/2),y=(Game.SIZE[1]/2+64), rotation=Game.drainrotation)
@window.event
def on_mouse_release(x, y, button, modifiers):
    Cursor.create_cursor(x/Game.totalzoom,y/Game.totalzoom)
    x=x/Game.totalzoom
    y=y/Game.totalzoom
    if Game.dragintensity != 0:
        if Game.rectangle_exists:
            Game.rectangle.opacity=0
            Game.rectangle_exists=False

        Game.drainrotation=0.0
        minigame.getmousepos(Game.x1, Game.y1, Game.dragintensity,hud)
        if not Game.milk:
            minigame.uddersprite.update(scale_x=1, scale_y=-1,x=((Game.SIZE[0]/2)),y=(Game.SIZE[1]/2+64),rotation=Game.drainrotation)
        else:
            minigame.uddersprite.update(scale_x=1,scale_y=1, x=(Game.SIZE[0]/2-128),y=(Game.SIZE[1]/2-64))
        minigame.totaldrag=minigame.totaldrag+Game.dragintensity
        Game.dragintensity = 0
        if minigame.milk ==0:
            Cursor.set_cursor(window, Cursor.CROSSHAIR)



@window.event
def on_key_press(symbol, modifiers) -> None:
    #normalisation? why would anyone do this
    if symbol == pyglet.window.key.W:
        pyglet.clock.schedule_interval(player.move_up, 1 / 60.0,music_manager)
    elif symbol == pyglet.window.key.A:
        pyglet.clock.schedule_interval(player.move_left, 1 / 60.0,music_manager)
    elif symbol == pyglet.window.key.S:
        pyglet.clock.schedule_interval(player.move_down, 1 / 60.0,music_manager)
    elif symbol == pyglet.window.key.D:
        pyglet.clock.schedule_interval(player.move_right, 1 / 60.0,music_manager)
    elif (symbol == pyglet.window.key.PLUS or
          (symbol == pyglet.window.key.EQUAL and modifiers
           and pyglet.window.key.MOD_SHIFT)):
        window.view = window.view.scale((Game.zoom, Game.zoom, 1))
        Game.totalzoom = Game.totalzoom * Game.zoom
        zoom()
    elif symbol == pyglet.window.key.MINUS and Game.totalzoom > 0.5:
        window.view = window.view.scale(
            (1 / Game.zoom, 1 / Game.zoom, 1))
        Game.totalzoom /= Game.zoom
        zoom(recip=True)
    elif symbol == pyglet.window.key.EQUAL:
        Game.zoom = 1.0 / Game.totalzoom 
        #raffers completely fucked this up. i fixed it. next time, please stop modifying things without testing that the features actually work.
        window.view = window.view.scale((Game.zoom, Game.zoom, 1))
        z = Game.zoom
        Game.SIZE=640,480
        player.set_screen_size(z)
        tilemap.set_screen_size(z)
        minigame.set_screen_size(z)
        hud.set_screen_size(z)
        npcs.set_screen_size(z)
        hud.close_popup(player)
        hud.close_inventory()
        Cursor.change_size(1/z,window)
        Cursor.set_cursor(window, Cursor.CROSSHAIR)
        if hud.inventory_open:
            hud.close_inventory()
        Game.zoom = 2.0
        Game.totalzoom = 1.0
    elif symbol == pyglet.window.key.B:
        pyglet.app.exit()
    elif symbol == pyglet.window.key.C:
        if tilemap.filename == "assets/tiles/cheese_room/cheese_room.tmx":
            tilemap.load_new_tilemap(f"assets/tiles/{player.current_area}/{player.current_area}.tmx")
            player.current_tilemap = player.current_area
            # I love that this button turns cheese game into empty room simulator 2025
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
             128,player)
        minigame.minigameselector(hud,cheeses)
        Game.minigameopen=True
    elif symbol ==pyglet.window.key.Q:
        music_manager.get_playing()
    elif symbol == pyglet.window.key.M:
        playerpos = player.get_pos()
        cowpos = npcs.cow.get_pos()  
        
        if (playerpos[0]<=cowpos[0]+2 and playerpos[0]>=cowpos[0]-2 and playerpos[1]<=cowpos[1]+2 and playerpos[1]>=cowpos[1]-2):
            if Game.milk:

                hud.close_popup(player)
            else:
                hud.create_popup(0, (Game.SIZE[0] / 2 - 128) * Game.totalzoom,
                             (Game.SIZE[1] / 2 - 64) * Game.totalzoom, 256,
                             128,player)
                minigame.milkingmini("real")

                Cursor.set_cursor(window, Cursor.HAND)
                Game.minigameopen=True


            Game.milk = not Game.milk


@window.event
def on_key_release(symbol, _) -> None:
    if symbol == pyglet.window.key.W:
        pyglet.clock.unschedule(player.move_up)
        music_manager.cancel_sfx()
    elif symbol == pyglet.window.key.A:
        pyglet.clock.unschedule(player.move_left)
        music_manager.cancel_sfx()
    elif symbol == pyglet.window.key.S:
        pyglet.clock.unschedule(player.move_down)
        music_manager.cancel_sfx()
    elif symbol == pyglet.window.key.D:
        pyglet.clock.unschedule(player.move_right)
        music_manager.cancel_sfx()


fps_display = pyglet.window.FPSDisplay(window=window)


tilemap = Tilemap('assets/tiles/europe/europe.tmx', Game.SIZE)

player = Player('assets/sprites/player/', Game.SIZE, tilemap)
player.give(item.MUG, 1)
player.set_held_item(0)
player.set_screen_size(1)
Cursor = Cursor_Class(1)
Cursor.set_cursor(window, Cursor.CROSSHAIR)
hud = Hud(Game.SIZE, player, window)
minigame = Minigame(hud)
music_manager = Music_manager(Game.SIZE)
cheeses=Cheeses()
music_manager.update_area("europe","europe")

npcs = NPC_Manager(Game.SIZE, player, tilemap)
pyglet.clock.schedule_once(Game.moo,randint(5,10))
#this should be for each cow...

game = Game()
