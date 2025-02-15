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
        self.shape.friction = 0.5
        
        # Ajouter au moteur physique
        space.add(self.body, self.shape)

class Platform:
    def __init__(self, x1, y1, x2, y2, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (x1, y1), (x2, y2), 5)
        self.shape.elasticity = 1.0
        self.shape.friction = 0.5
        space.add(self.body, self.shape)

def connect_goos(goo1, goo2, space):
    rest_length = np.linalg.norm(goo1.body.position - goo2.body.position)  # Distance initiale
    stiffness = 300  # Raideur du ressort
    damping = 10  # Amortissement du ressort
    
    spring = pymunk.DampedSpring(goo1.body, goo2.body, (0, 0), (0, 0), rest_length, stiffness, damping)
    space.add(spring)
    return spring



def add_goo(goos, new_position, space):
    new_goo = Goo(new_position, space)
    
    if len(goos) > 0:
        goomin1, goomin2 = None, None
        min1, min2 = float('inf'), float('inf')

        
        for goo in goos:
            distance = np.linalg.norm(new_goo.position - goo.body.position)

            if distance < min1:
                min2, goomin2 = min1, goomin1  
                min1, goomin1 = distance, goo
            elif distance < min2:
                min2, goomin2 = distance, goo

        
        if goomin1 and min1 <= 200:
            connect_goos(new_goo, goomin1, space)
        if goomin2 and min2 <= 200:
            connect_goos(new_goo, goomin2, space)
    
    goos.append(new_goo)

import numpy as np

def find_two_closest_targets(goos, platforms, pos):
    closest1, closest2 = None, None
    min1, min2 = float('inf'), float('inf')

   
    for goo in goos:
        distance = np.linalg.norm(np.array(goo.body.position) - np.array(pos))

        if distance < min1 and distance < 200:
            min2, closest2 = min1, closest1 
            min1, closest1 = distance, goo
        elif distance < min2 and distance < 200:
            min2, closest2 = distance, goo


    for platform in platforms:
        platform_pos = np.array(platform.body.position)
        distance = np.linalg.norm(platform_pos - np.array(pos))

        if distance < min1 and distance < 200:
            min2, closest2 = min1, closest1  
            min1, closest1 = distance, platform
        elif distance < min2 and distance < 200:
            min2, closest2 = distance, platform

    return closest1, closest2
  

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
    Platform(50, 550, 300, 550, space),  # Plateforme de départ
    Platform(500, 200, 750, 200, space),   # Plateforme d’arrivée
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
    screen.fill((200, 255, 255))  # Fond blanc
    mouse_pos = pygame.mouse.get_pos()
    closest_targets = find_two_closest_targets(goos, platforms, mouse_pos)
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if len(goos) ==0:
                add_goo(goos, (x, y), space)
            elif closest_targets[0] or closest_targets[1]:
                add_goo(goos, (x, y), space)
            

    # Mise à jour physique
    space.step(1 / FPS)
    
    if closest_targets[0] and closest_targets[1]:
        pygame.draw.line(screen, (150, 150, 150), mouse_pos, (int(closest_targets[0].body.position.x), int(closest_targets[0].body.position.y)), 1)
        pygame.draw.line(screen, (150, 150, 150), mouse_pos, (int(closest_targets[1].body.position.x), int(closest_targets[1].body.position.y)), 1)
        
    # Dessiner la scène
    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
