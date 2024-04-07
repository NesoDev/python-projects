from pyray import *
from raylib import *
from resources.data_structures import KdBTree, Node
import time

colors = [LIGHTGRAY, GRAY, DARKGRAY, YELLOW, GOLD, ORANGE, PINK, RED, MAROON, GREEN, LIME, DARKGREEN, 
          SKYBLUE, BLUE, DARKBLUE, PURPLE, VIOLET, DARKPURPLE, BEIGE, BROWN, DARKBROWN, WHITE, BLACK,
          BLANK, MAGENTA, RAYWHITE]


class Corpe:
    def __init__(self, pos_x: float, pos_y: float, radius: float):
        self.x = pos_x
        self.y = pos_y
        self.x_0 = pos_x
        self.y_0 = pos_y
        self.radius = radius
        
    def restorePosition(self):
        self.x = self.x_0
        self.y = self.y_0


class Wall(Corpe):
    def __init__(self, pos_x_0: float, pos_y_0: float, pos_x: float, pos_y: float):
        length = max(abs(pos_x_0 - pos_x), abs(pos_y_0 - pos_y))
        super().__init__((pos_x_0 + pos_x) / 2, (pos_y_0 + pos_y) / 2, length / 2)
        self.pos_x_0 = pos_x_0
        self.pos_y_0 = pos_y_0
        self.pos_x = pos_x
        self.pos_y = pos_y


class Particle(Corpe):
    def __init__(self, pos_x: float, pos_y: float, v_x: float, v_y: float, radius: float, mass: float,):
        super().__init__(pos_x, pos_y, radius)
        self.v_x = v_x
        self.v_y = v_y
        self.mass = mass
        
    @staticmethod
    def setPosition(particle, x: float, y: float):
        particle.x_0 = particle.x
        particle.y_0 = particle.y
        particle.x = x
        particle.y = y

    def setVelocity(self, v_x: float, v_y: float):
        self.v_x = v_x
        self.v_y = v_y
    
    @staticmethod
    def updatePosition(particle, dt: float):
        # Método de Euler mejorado
        x_n = particle.x + particle.v_x * dt
        y_n = particle.y - particle.v_y * dt
        v_x_n = particle.v_x
        v_y_n = particle.v_y
        new_pos_x = particle.x + (particle.v_x + v_x_n) * 0.5 * dt
        new_pos_y = particle.y - (particle.v_y + v_y_n) * 0.5 * dt
        Particle.setPosition(particle, new_pos_x, new_pos_y)


def update_position_corpes(corpes: list, dt: float):
    for corpe in corpes:
        Particle.updatePosition(corpe, dt)
        
        
class KdBTreeCollision(KdBTree):
    def __init__(self, data: list, axis: str, space: int):
        super().__init__(data, axis, space)
    
    
    @staticmethod
    def searchCollisions(kdbtc):
        def checkCollision(p1, p2):
            distance = ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5
            return distance <= p1.radius + p2.radius

        def read(root: Node):
            if root.type == "Leaf":
                if len(root.data) > 1:
                    for i in range(len(root.data)):
                        for j in range(i + 1, len(root.data)):
                            p1 = root.data[i]
                            p2 = root.data[j]
                            if checkCollision(p1, p2):
                                #print(f"Collision detected between particles {i} and {j}")
                                p1.restorePosition()
                                p2.restorePosition()
                                p1.v_x *= -1
                                p1.v_y *= -1
                                p2.v_x *= -1
                                p2.v_y *= -1
            if root.branchLeft:
                read(root.branchLeft)
            if root.branchRight:
                read(root.branchRight)

        read(kdbtc.root)

        #print("---------------------------------------------------------------------------------------------------------------------")
        
def draw_corpes(corpes: list, kdbtc: KdBTreeCollision):
    for corpe in corpes:
        draw_circle_lines(int(corpe.x), int(corpe.y), corpe.radius, WHITE)
        
    def read(root: Node):
        if root.type == "Leaf":
            if len(root.data) == 2:
                corpes = root.data
                contrary_axis = "y" if root.axi == "x" else "x"
                if abs(getattr(corpes[0], contrary_axis) - getattr(corpes[1], contrary_axis)) <= corpes[0].radius + corpes[1].radius:
                    draw_line(int(corpes[0].x), int(corpes[0].y), int(corpes[1].x), int(corpes[1].y), YELLOW)
            
            #return
        if root.branchLeft:
            read(root.branchLeft)
        if root.branchRight:
            read(root.branchRight)

    root = kdbtc.root
    read(root)
    
    

def main():
    window_width = 1000
    window_height = 700
    window_title = "Particles System"
    window_color = BLACK
    
    init_window(window_width, window_height, window_title)
    
    target_fps = 60  # FPS objetivo
    target_dt = 1 / target_fps  # Duración objetivo entre fotogramas
    play = True
    
    #corpes = [
    #    Particle(pos_x=400, pos_y=200, v_x=20, v_y=-40, radius=10, mass=10),
    #    Particle(pos_x=600, pos_y=500, v_x=-20, v_y=40, radius=25, mass=5),
    #    Particle(pos_x=200, pos_y=200, v_x=20, v_y=0, radius=10, mass=3),
    #    Particle(pos_x=600, pos_y=200, v_x=-80, v_y=0, radius=30, mass=1),
    #    Particle(pos_x=400, pos_y=100, v_x=100, v_y=-40, radius=50, mass=4),
    #    Particle(pos_x=183, pos_y=105, v_x=80, v_y=10, radius=40, mass=8),
    #]
    
    corpes = []
    
    # Agregar 20 partículas que no se sobrepongan
    for _ in range(100):
        pos_x = get_random_value(50, window_width - 50)
        pos_y = get_random_value(50, window_height - 50)
        radius = get_random_value(5, 20)
        v_x = get_random_value(-200, 200)
        v_y = get_random_value(-200, 200)
        mass = radius  # La masa se ajusta al radio en esta implementación
        new_corpe = Particle(pos_x=pos_x, pos_y=pos_y, v_x=v_x, v_y=v_y, radius=radius, mass=mass)
        
        # Verificar si la nueva partícula no se superpone con las existentes
        overlap = False
        for existing_corpe in corpes:
            distance = ((existing_corpe.x - new_corpe.x) ** 2 + (existing_corpe.y - new_corpe.y) ** 2) ** 0.5
            if distance <= existing_corpe.radius + new_corpe.radius:
                overlap = True
                break
        
        if not overlap:
            corpes.append(new_corpe)
    
    while not window_should_close():
        
        begin_drawing()
        clear_background(window_color)
        
        if play:
            #for corpe in corpes:
                #print(f"Particle{corpe.x, corpe.y, corpe.radius, corpe.v_x, corpe.v_y, corpe.mass},")
            t0 = time.time()

            kdbtc = KdBTreeCollision(data=corpes, axis="y", space=0.5)
            KdBTreeCollision.searchCollisions(kdbtc)
            
            update_position_corpes(corpes, target_dt)

            t1 = time.time()
            elapsed_time = t1 - t0

            remaining_time = target_dt - elapsed_time

            if remaining_time > 0:
                time.sleep(remaining_time)

            dt = time.time() - t0
            
            
        if is_key_pressed(KEY_ENTER):
            #print(f"Tecla ENTER presionada")
            play = not play
            
        play_symbol = "|>" if play else "||"
        draw_text(play_symbol, 20, 20, 50, WHITE)
        
        draw_corpes(corpes, kdbtc)
        #kdbtc = None
        end_drawing()
        
    close_window()

main()

