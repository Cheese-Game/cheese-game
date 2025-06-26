import pyglet


class Music_manager:

    def __init__(self, screen_size) -> None:
        self.screen_width, self.screen_height = screen_size
        self.player = pyglet.media.Player()
        self.sfx_player=None
        self.master_volume=1
        


    def update_area(self, world, area) -> None:
        self.cancel_music()
        self.player = pyglet.media.Player()
        self.player.volume=0.05*self.master_volume
        print("assets/music/" + str(world) + "/" + str(area) + ".mp3")
        track = pyglet.media.load("assets/music/" + str(world) + "/" +
                                  str(area) + ".mp3",
                                  streaming=False)
        self.player.queue(track)
        self.player.loop = True
        self.player.play()

    def cancel_music(self) -> None:
        self.player.pause()
        self.player = None

    def get_playing(self) -> None:
        print("status:" + str(self.player))
    def cancel_sfx(self) -> None:
        self.sfx_player = None
    def play_sfx(self, sfx,vol) -> None:
        effect=pyglet.media.load("assets/sfx/" + str(sfx) + ".mp3")
        if self.sfx_player==None:
            self.sfx_player=pyglet.media.Player()
            self.sfx_player.volume=vol*self.master_volume
            self.sfx_player.queue(effect)
            self.sfx_player.play()
        else:
            self.sfx_player.queue(effect)
    def distance_sfx(self,sfx,distance) -> None:
        self.dsfx_player=pyglet.media.Player()
        self.dsfx_player.volume=0.8/float(distance)*self.master_volume
        effect=pyglet.media.load("assets/sfx/" + str(sfx) + ".mp3")
        self.dsfx_player.queue(effect)
        self.dsfx_player.play()
        
        
        
