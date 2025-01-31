import numpy as np
import pygame
import pymunk
import pymunk.pygame_util

class Goo:
    def __init__(self, position, space):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.mass = 0.4  # kg
        self.radius = 10  # Pixels (10 cm = 10 pixels)
        
        # Création du corps Pymunk
        self.body = pymunk.Body(self.mass, pymunk.moment_for_circle(self.mass, 0, self.radius))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.5
        
        
        # Ajouter au moteur physique
        space.add(self.body, self.shape)

class Platform:
    def __init__(self, x1, y1, x2, y2, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (x1, y1), (x2, y2), 5)
        self.shape.elasticity = 1.0
        
        space.add(self.body, self.shape)

def connect_goos(goo1, goo2, space):
    rest_length = np.linalg.norm(goo1.position - goo2.position)  # Distance initiale
    stiffness = 100  # Raideur du ressort
    damping = 0.5  # Amortissement du ressort
    
    spring = pymunk.DampedSpring(goo1.body, goo2.body, (0, 0), (0, 0), rest_length, stiffness, damping)
    space.add(spring)
    return spring



def add_goo(goos, new_position, space):
    new_goo = Goo(new_position, space)
    
    if len(goos) > 0:
        min1= np.linalg.norm(new_goo.position - goos[0].position)
        min2= np.linalg.norm(new_goo.position - goos[0].position)
        
        goomin1 = goos[0]
        goomin2 = goos[0]
        # Attacher aux Goos existants
        for goo in goos:
        
            if np.linalg.norm(new_goo.position - goo.position) <= max(min1,min2):  # Distance max de connexion
                if max(min1,min2) == min1:
                    min1 = np.linalg.norm(new_goo.position - goo.position)
                    goomin1 = goo
                else:
                    min2 = np.linalg.norm(new_goo.position - goo.position)
                    goomin2 = goo
                
        if np.linalg.norm(new_goo.position - goomin1.position) <= 300:   
            connect_goos(new_goo, goomin1, space)
        if np.linalg.norm(new_goo.position - goomin2.position) <= 300:   
            connect_goos(new_goo, goomin2, space)
    
    goos.append(new_goo)
    
    

# Initialisation Pygame et Pymunk
WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 50*9.81)

# Dessinateur Pymunk
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Création des plateformes
platforms = [
    Platform(100, 500, 300, 500, space),  # Plateforme de départ
    Platform(500, 400, 700, 400, space)   # Plateforme d’arrivée
]

contours = [
    Platform(0, 0, 0, 600, space),
    Platform(0, 600, 800, 600, space),
    Platform(800, 600, 800, 0, space),
    Platform(0,0, 800, 0, space)
]
# Liste des Goos
goos = []

# Boucle principale
running = True
while running:
    screen.fill((255, 255, 255))  # Fond blanc

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            add_goo(goos, (x, y), space)

    # Mise à jour physique
    space.step(1 / FPS)

    # Dessiner la scène
    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
