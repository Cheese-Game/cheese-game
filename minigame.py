from collections.abc import Mapping
from pyglet import sprite, resource, gui,clock
import time

from logger import log

class Minigame:

    def __init__(self, hud) -> None:
        #how does my own code work? I know, but my memory fails so mayhaps actually leave comments
        # i fucking hate python it is a bullshit language that only follows fucking vibes over whether it should work
        self.hot = False
        self.kneadval = 0.0
        self.dragintensity = 0
        self.totaldrag = 0
        #to do: look at 2do list, you dumbass. if you have no clue what i'm talking about, make colision actually work!!
        self.games_used = []
        self.screen_width, self.screen_height = hud.screen_width, hud.screen_height
        self.secssincehot = 0.0
        self.instruction = ""
        self.kneadmininit = False
        self.batch = hud.dialog_batch
        self.dialog_components = hud.dialog_components
        self.corner1 = self.screen_width / 2 - 128, self.screen_height / 2 - 64
        self.milkingmininit = False
        
    def update(self,dt):
        if self.secssincehot>=30:
            self.hot=False
        else:
            self.secssincehot=self.secssincehot +1
            #this is just a shit counter. must fix
       
    def fetch_colour(self, x, y):
        x = int(x - self.corner1[0])
        y = int(y - self.corner1[1])
        imagedata = self.udderimg.get_image_data()
        #b'\xff\xa3\xff' is udder-pink.
        if (imagedata.get_region(x, y, 1, 1).get_data("RGBA",
                                                      (3))) == b'\x00\x00\x00':
            # by fetching the colour of the png, you can filter out the transparent parts of the png
            see = False
        else:
            see = True
        return see

    def set_screen_size(self, zoom) -> None:
        self.screen_width /= zoom
        self.screen_height /= zoom
        self.corner1 = self.screen_width / 2 - 128, self.screen_height / 2 - 64
    def returnmilk(self, hud, player):
        print("mug full. put code to fill mug here later")
        self.milk = 0
        hud.close_dialog(player)

    def milkingmini(self, udder) -> None:
        self.milk = 0
        self.milkingmininit = True
        if udder == "real":
            self.udder = "real"
            self.udderimg = resource.image(
                "assets/sprites/hud/minigame/udder.png", atlas=True)
        #the udder var is about whether the udder is an udder or curds in a cloth
        elif udder == "drain":
            self.udder = "drain"
            self.games_used.append("drain")
            self.udderimg = resource.image(
                "assets/sprites/hud/minigame/curdincloth.png", atlas=True)

            self.nailimg = resource.image(
                "assets/sprites/hud/minigame/nail.png", atlas=True)
            self.udderimg.anchor_x = 128
            self.nailsprite = sprite.Sprite(self.nailimg,
                                            x=self.corner1[0],
                                            y=self.corner1[1] + 124)
        
        if udder == "drain":
            self.uddersprite = sprite.Sprite(self.udderimg,
                                         x=self.corner1[0] + 128,
                                         y=self.corner1[1] + 128,
                                         batch=self.batch)
            self.uddersprite.update(scale_y=-1)
        else:
            self.uddersprite = sprite.Sprite(self.udderimg,
                                         x=self.corner1[0],
                                         y=self.corner1[1],
                                         batch=self.batch)
        self.dialog_components.append(self.uddersprite)

    def getmousepos(self, x1, y1, intensity, hud):
        if self.milkingmininit and self.udder == "real":
            self.milk = self.milk + intensity
            if self.milk > 100:
                self.milk = 0

                self.returnmilk(hud, hud.player)

    def kneadminigame(self, hud) -> None:
        self.kneadmininit = True
        self.totalscroll = 0
        self.highest = 1.0
        self.lowest = 1.0
        self.games_used.append("knead")

        kneadingcheeseicon = resource.image(
            "assets/sprites/hud/minigame/kneadable.png", atlas=True)
        self.kneadingcheese = sprite.Sprite(
            kneadingcheeseicon,
            x=self.corner1[0],
            y=self.corner1[1],
            batch=self.batch,
        )

        self.dialog_components.append(self.kneadingcheese)

    def minigameselector(self, hud, item) -> None:
        if self.hot:
            kneadingbtnicon = resource.image("assets/sprites/item/1.png")
            self.kneadingbtn = gui.PushButton(x=self.corner1[0] + 32,
                                              y=self.corner1[1],
                                              pressed=kneadingbtnicon,
                                              unpressed=kneadingbtnicon,
                                              batch=self.batch)
            hud.window.push_handlers(self.kneadingbtn)

        finishbtnicon = resource.image(
            "assets/sprites/hud/minigame/finishicon.png")
        self.finishbtn = gui.PushButton(x=self.corner1[0],
                                        y=self.corner1[1] + 16,
                                        pressed=finishbtnicon,
                                        unpressed=finishbtnicon,
                                        batch=self.batch)
        backbtnicon = resource.image("assets/sprites/hud/minigame/backbtn.png")
        self.backbtn = gui.PushButton(x=self.corner1[0],
                                      y=self.corner1[1] + 112,
                                      pressed=finishbtnicon,
                                      unpressed=backbtnicon,
                                      batch=self.batch)
        hud.window.push_handlers(self.backbtn)
        hud.window.push_handlers(self.finishbtn)
        drainingbtnicon = resource.image(
            "assets/sprites/hud/minigame/drainingicon.png")
        self.drainingbtn = gui.PushButton(x=self.corner1[0] + 16,
                                          y=self.corner1[1] + 16,
                                          pressed=drainingbtnicon,
                                          unpressed=drainingbtnicon,
                                          batch=self.batch)
        hud.window.push_handlers(self.drainingbtn)
        hotbtnicon = resource.image(
            "assets/sprites/hud/minigame/microwaveicon.png")
        self.hotbtn = gui.PushButton(x=self.corner1[0] + 16,
                                     y=self.corner1[1],
                                     pressed=hotbtnicon,
                                     unpressed=hotbtnicon,
                                     batch=self.batch)
        hud.window.push_handlers(self.hotbtn)
        #buttons.

        def killself(self, hud):
            # this purges the old screen of all of the cheese menu buttons. might replace the menu with navigation of the cheese room (hows it in there?)
            if self.hot:
                self.dialog_components.remove(self.kneadingbtn)
                self.kneadingbtn = None

            self.dialog_components.remove(self.hotbtn)
            self.dialog_components.remove(self.finishbtn)
            self.hotbtn = None
            self.dialog_components.remove(self.drainingbtn)
            self.drainingbtn = None
            self.finishbtn = None

        def on_press_backbtn(_):
            hud.dialog = None
            self.dialog_components.clear()
            self.instruction = "create-dialog"
            self.kneadingcheese = None
            self.nailsprite = None
            self.uddersprite = None

        def on_presskneadbtn(_):
            killself(self, hud)
            self.kneadminigame(hud)

        def on_presshotbtn(_):
            killself(self, hud)
            self.hot = True
            self.minigameselector(hud, item)
            clock.schedule_interval(self.update, 1)
            self.secssincehot = 0.0

        def on_pressdrainbtn(_):
            killself(self, hud)
            self.milkingmini("drain")

        def on_pressfinishbtn(_):
            killself(self, hud)
            print(item.find_cheese(self))

        if self.hot:
            self.kneadingbtn.set_handler('on_press', on_presskneadbtn)
            self.dialog_components.append(self.kneadingbtn)
        self.finishbtn.set_handler('on_press', on_pressfinishbtn)
        self.backbtn.set_handler('on_press', on_press_backbtn)
        self.drainingbtn.set_handler('on_press', on_pressdrainbtn)
        self.hotbtn.set_handler('on_press', on_presshotbtn)
        self.dialog_components.append(self.backbtn)
        self.dialog_components.append(self.drainingbtn)
        self.dialog_components.append(self.hotbtn)
        self.dialog_components.append(self.finishbtn)

