import numpy as np
import math
import pygame
import pymunk

#création de l'espace 
space = pymunk.Space()


class Goo:
    def __init__(self, position):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.mass = 0.4  #en kg
        self.radius = 0.01  #en m
        self.links = []  #connexions (Goos ou plateformes)
        self.rest_lengths = {}  #Longueurs au repos des ressorts
        self.k = 100  #raideur du ressort J/m²

    def attach(self, other):
        if other not in self.links:
            self.links.append(other)
            distance = np.linalg.norm(self.position - other.position)
            self.rest_lengths[other] = distance

    def compute_force(self):
        total_force = np.array([0.0, 0.0])
        gravity = np.array([0, -9.81 / 20]) * self.mass  # Gravité réduite
        total_force += gravity

        for other in self.links:
            displacement = self.position - other.position
            distance = np.linalg.norm(displacement)
            rest_length = self.rest_lengths[other]
            force_magnitude = self.k * (distance - rest_length)
            force_direction = displacement / distance if distance != 0 else np.array([0, 0])
            total_force += force_magnitude * force_direction

        return total_force
    
    def update(self, dt):
        force = self.compute_force()
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

    def add_to_space(self, space):
        space.add(self.body, self.shape)

    def draw(self, screen):
        """Affiche la Goo et ses liens"""
        # Convertir la position en pixels
        x, y = int(self.position[0]), int(600 - self.position[1])

        # Dessiner les liens (ressorts)
        for other in self.links:
            # Assure-toi que `other.position` est bien un tableau avec deux valeurs
            ox, oy = int(other.position[0]), int(600 - other.position[1])
            
            # Vérifie que les coordonnées sont valides avant de dessiner
            if isinstance(x, int) and isinstance(y, int) and isinstance(ox, int) and isinstance(oy, int):
                pygame.draw.line(screen, (50, 50, 50), (x, y), (ox, oy), 2)  # Ligne grise

        # Dessiner la Goo
        pygame.draw.circle(screen, (0, 0, 0), (x, y), int(self.radius))

class Platform:
    def __init__(self, points):
        self.points = [np.array(p, dtype=float) for p in points]  # Liste de points définissant la forme
    
    def closest_point(self, goo):
        min_dist = float('inf')
        closest = None
        for p in self.points:
            dist = np.linalg.norm(goo.position - p)
            if dist < min_dist:
                min_dist = dist
                closest = p
        return closest
    
    def draw(self, screen):
        """Dessine la plateforme comme une ligne"""
        for i in range(len(self.points) - 1):
            # Conversion des coordonnées en pixels
            x1, y1 = int(self.points[i][0]), int(600 - self.points[i][1])
            x2, y2 = int(self.points[i+1][0]), int(600 - self.points[i+1][1])
            
            # Utiliser pygame.draw.line pour dessiner une ligne
            pygame.draw.line(screen, (100, 100, 100), (x1, y1), (x2, y2), 5)


def add_goo(goos, new_position, platforms):
    new_goo = Goo(new_position)
    
    # Attacher aux Goos existants
    for goo in goos:
        if np.linalg.norm(new_goo.position - goo.position) <= 0.2:
            new_goo.attach(goo)
            goo.attach(new_goo)
    
    # Attacher aux plateformes
    for platform in platforms:
        closest_point = platform.closest_point(new_goo)
        if np.linalg.norm(new_goo.position - closest_point) <= 0.1:
            new_goo.attach(Goo(closest_point))  # Création d'un point fixe fictif
    
    # Un Goo doit avoir au moins un lien pour être valide
    if new_goo.links:
        goos.append(new_goo)

def simulate(goos, dt=0.01, steps=1000):
    for _ in range(steps):
        for goo in goos:
            goo.update(dt)

# +
# --- Initialisation de Pygame ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Création de la scène ---
platforms = [Platform([(0, 0), (5, 0)]), Platform([(10, 0), (15, 0)])]
goos = [Goo((2, 1)), Goo((3, 1)), Goo((4, 2))]

# Attacher les Goos entre eux
goos[0].attach(goos[1])
goos[1].attach(goos[2])

# --- Boucle du jeu ---
running = True
while running:
    screen.fill((200, 200, 255))  # Fond bleu ciel

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de la simulation
    simulate(goos, dt=0.01, steps=1)

    # Affichage des plateformes
    for platform in platforms:
        platform.draw(screen)

    # Affichage des Goos
    for goo in goos:
        goo.draw(screen)

    # Rafraîchir l'écran
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()

# -





c
