from sprites.groups import movable_group


class Camera:
    def __init__(self):
        self.dx = -2

    def apply(self):
        for obj in movable_group:
            obj.rect.x += self.dx
