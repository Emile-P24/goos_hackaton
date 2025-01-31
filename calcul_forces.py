import numpy as np
import math
import pygame
import pymunk


class Goo:
    def __init__(self, position):
        self.position = np.array(position, dtype=float)
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