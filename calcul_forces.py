import numpy as np
import math
import pygame
import pymunk


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
    
def simulate(goos, dt=0.01, steps=1000):
    for _ in range(steps):
        for goo in goos:
            goo.update(dt)

# Exemple d'utilisation
platform1 = Platform([(0, 0), (5, 0)])
platform2 = Platform([(10, 0), (15, 0)])

goo1 = Goo((2, 1))
goo2 = Goo((3, 1))
goo3 = Goo((4, 2))

goo1.attach(goo2)
goo2.attach(goo3)

goos = [goo1, goo2, goo3]

simulate(goos)

# Affichage des positions finales
for goo in goos:
    print(f"Position d'équilibre du Goo: {goo.position}")