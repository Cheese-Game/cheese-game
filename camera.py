from logger import log


class Camera:
    def __init__(self, x: float, y: float, zoom: float) -> None:
        self.x = x
        self.y = y
        self.zoom = zoom

        log("Camera initialised")
