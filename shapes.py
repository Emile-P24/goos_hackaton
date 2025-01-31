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

    def draw(self, screen):
        # Dessiner le Goo (un cercle)
        position = self.body.position
        pygame.draw.circle(screen, (0, 255, 0), (int(position[0]), int(position[1])), int(self.shape.radius))

# Classe mère pour les plateformes
class Platform:
    def __init__(self, space, color):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shapes = []  # Liste pour stocker les formes associées à cette plateforme
        self.color = color
        space.add(self.body)

    def draw(self, screen):
        for shape in self.shapes:
            if isinstance(shape, pymunk.Segment):
                # Dessiner un segment
                pygame.draw.line(screen, self.color, 
                                 self.body.local_to_world(shape.a), 
                                 self.body.local_to_world(shape.b), 5)
            elif isinstance(shape, pymunk.Circle):
                # Dessiner un cercle (en utilisant la position du body pour le centre)
                position = self.body.position  # Le centre du cercle est la position du corps
                pygame.draw.circle(screen, self.color, (int(position[0]), int(position[1])), int(shape.radius))
            elif isinstance(shape, pymunk.Poly):
                # Dessiner un polygone
                vertices = [self.body.local_to_world(vertex) for vertex in shape.get_vertices()]
                pygame.draw.polygon(screen, self.color, vertices)

# Sous-classe : Plateforme en ligne (Segment)
class LinePlatform(Platform):
    def __init__(self, x1, y1, x2, y2, space, color):
        super().__init__(space, color)
        shape = pymunk.Segment(self.body, (x1, y1), (x2, y2), 5)
        shape.elasticity = 1.0
        space.add(shape)
        self.shapes.append(shape)

# Sous-classe : Plateforme hexagonale (Poly)
class HexagonPlatform(Platform):
    def __init__(self, x, y, size, space, color):
        super().__init__(space, color)

        # Générer les 6 points d'un hexagone régulier autour du centre (x, y)
        points = [(size * np.cos(theta), size * np.sin(theta)) for theta in np.linspace(0, 2 * np.pi, 6, endpoint=False)]
        
        # Création de la forme hexagonale
        shape = pymunk.Poly(self.body, points)
        self.body.position = (x, y)

        # Propriétés physiques
        shape.elasticity = 1.0
        shape.friction = 1.0

        # Ajouter la forme à l'espace
        space.add(shape)
        self.shapes.append(shape)

# Sous-classe : Plateforme circulaire (disque)
class CirclePlatform(Platform):
    def __init__(self, x, y, radius, space, color):
        super().__init__(space, color)
        shape = pymunk.Circle(self.body, radius)
        self.body.position = (x, y)
        shape.elasticity = 1.0
        space.add(shape)
        self.shapes.append(shape)

def connect_goos(goo1, goo2, space):
    rest_length = np.linalg.norm(goo1.position - goo2.position)  # Distance initiale
    stiffness = 100  # Raideur du ressort
    damping = 0.5  # Amortissement du ressort
    
    spring = pymunk.DampedSpring(goo1.body, goo2.body, (0, 0), (0, 0), rest_length, stiffness, damping)
    space.add(spring)
    return spring

def add_goo(goos, new_position, space):
    new_goo = Goo(new_position, space)
    
    # Attacher aux Goos existants
    for goo in goos:
        if np.linalg.norm(new_goo.position - goo.position) <= 200:  # Distance max de connexion
            connect_goos(new_goo, goo, space)
    
    goos.append(new_goo)

# Fonction pour dessiner les ressorts
def draw_springs(goos, screen):
    for i in range(len(goos)):
        for j in range(i + 1, len(goos)):
            goo1, goo2 = goos[i], goos[j]
            # Dessiner une ligne entre les deux goos
            pygame.draw.line(screen, (0, 0, 0), 
                             (int(goo1.body.position[0]), int(goo1.body.position[1])), 
                             (int(goo2.body.position[0]), int(goo2.body.position[1])), 2)

# Initialisation Pygame et Pymunk
WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 50 * 9.81)

# Création de différentes plateformes
platforms = [
    LinePlatform(100, 500, 300, 500, space, (255, 105, 180)),  # Ligne horizontale
    HexagonPlatform(400, 300, 50, space, (255, 165, 0)),  # Orange
    CirclePlatform(650, 300, 50, space, (238, 130, 238)),  # Violet
]

contours = [
    LinePlatform(0, 0, 0, 600, space, (0, 0, 0)),        # Bord gauche
    LinePlatform(0, 600, 800, 600, space, (0, 0, 0)),    # Sol
    LinePlatform(800, 600, 800, 0, space, (0, 0, 0)),    # Bord droit
    LinePlatform(0, 0, 800, 0, space, (0, 0, 0))         # Plafond
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
    
    # Dessiner les plateformes avec leurs couleurs
    for platform in platforms:
        platform.draw(screen)

    # Dessiner tous les Goos
    for goo in goos:
        goo.draw(screen)
    
    # Dessiner les ressorts
    draw_springs(goos, screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()