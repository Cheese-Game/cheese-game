import pyglet


class Music_manager:

    def __init__(self, screen_size) -> None:
        self.screen_width, self.screen_height = screen_size
        self.player = pyglet.media.Player()

    def update_area(self, world, area) -> None:
        self.cancel_music()
        self.player = pyglet.media.Player()
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

    def looping_music(track, extrathing):
        print(extrathing)
        while True:
            yield track

    def play_sfx(self, sfx) -> None:
        effect = pyglet.media.load("assets/sfx/" + str(sfx) + ".mp3",
                                   streaming=False)
        effect.play()
