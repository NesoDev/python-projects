from ..Resources.data_structures import KdBTree


class Corpe:
    def __init__(self, pos_x: float, pos_y: float, radius: float):
        self.x = pos_x
        self.y = pos_y
        self.x_0 = pos_x
        self.y_0 = pos_y
        self.radius = radius


class Wall(Corpe):
    def __init__(self, pos_x_0: float, pos_y_0: float, pos_x: float, pos_y: float):
        length = max(abs(pos_x_0 - pos_x), abs(pos_y_0 - pos_y))
        super.__init__((pos_x_0 + pos_x) / 2, (pos_y_0 + pos_y) / 2, length / 2)
        self.pos_x_0 = pos_x_0
        self.pos_y_0 = pos_y_0
        self.pos_x = pos_x
        self.pos_y = pos_y


class Particle(Corpe):
    def __init__(
        self,
        pos_x: float,
        pos_y: float,
        v_x: float,
        v_y: float,
        radius: float,
        mass: float,
    ):
        super().__init__(pos_x, pos_y, radius)
        self.v_x = v_x
        self.v_y = v_y
        self.mass = mass

    def setPosition(self, x: float, y: float):
        self.x_0 = self.x
        self.y_0 = self.y
        self.x = x
        self.y = y

    def setVelocity(self, v_x: float, v_y: float):
        self.v_x = v_x
        self.v_y = v_y


corpes = [
    Particle(pos_x=7, pos_y=2, v_x=1, v_y=2, radius=4, mass=10),
    Particle(pos_x=24, pos_y=4, v_x=1, v_y=-3, radius=2, mass=5),
    Particle(pos_x=4, pos_y=10, v_x=1, v_y=4, radius=-1, mass=3),
    Particle(pos_x=18, pos_y=10, v_x=1, v_y=0, radius=-3, mass=1),
    Particle(pos_x=20, pos_y=12, v_x=10, v_y=-4, radius=0, mass=4),
    Particle(pos_x=13, pos_y=15, v_x=8, v_y=1, radius=-1, mass=8),
]

kdbt = KdBTree(data=corpes, axis="y", space=0.5)
