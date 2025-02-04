from pyglet import sprite,resource

class Minigame:
  def __init__(self,hud) -> None:
    self.screen_width,self.screen_height=hud.screen_width,hud.screen_height
    self.batch=hud.popupbatch
    self.popup_components=hud.popup_components
    self.corner1=self.screen_width/2-128,self.screen_height/2-64
    
  
  def milkingmini(self) -> None:
    udderimg=resource.image("assets/sprites/hud/minigame/udder.png",atlas=True)
    udder=sprite.Sprite(udderimg,x=self.corner1[0],y=self.corner1[1],batch=self.batch)
    self.popup_components.append(udder)
    