from pyglet import sprite,resource

class Minigame:
  def __init__(self,hud) -> None:
    self.screen_width,self.screen_height=hud.screen_width,hud.screen_height
    self.batch=hud.popupbatch
    self.popup_components=hud.popup_components
    self.corner1=self.screen_width/2-128,self.screen_height/2-64
    self.milkingmininit=False
  def set_screen_size(self, zoom) -> None:
    self.screen_width /= zoom
    self.screen_height /= zoom
    self.corner1=self.screen_width/2-128,self.screen_height/2-64
  def returnmilk(self,hud):
    print("mug full. put code to fill mug here later")
    self.milk=0
    hud.close_popup()
  def milkingmini(self,udder) -> None:
    self.milk=0
    self.milkingmininit=True
    if udder=="real":
      self.udder="real"
      udderimg=resource.image("assets/sprites/hud/minigame/udder.png",atlas=True)
    elif udder == "drain":
      self.udder="drain"
      udderimg=resource.image("assets/sprites/hud/minigame/curdincloth.png",atlas=True)

    udder=sprite.Sprite(udderimg,x=self.corner1[0],y=self.corner1[1],batch=self.batch)
    
    self.popup_components.append(udder)
  def getmousepos(self,x1,y1,intensity,hud):
    if self.milkingmininit and self.udder=="real":
      self.milk=self.milk+intensity
      if self.milk>100:
        self.returnmilk(hud)
    
 
  