import pygame
import pymunk
import numpy as np

# Paramètres de la simulation
GRAVITY = 9.81 / 20  # Gravité réduite
GOO_RADIUS = 10  # En pixels (1 cm = 1 pixels)
GOO_MASS = 0.4  # kg
SPRING_K = 100  # Raideur du ressort

class Goo:
    def __init__(self, space, x, y):
        self.body = pymunk.Body(mass=GOO_MASS, moment=pymunk.moment_for_circle(GOO_MASS, 0, GOO_RADIUS))
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, GOO_RADIUS)
        self.shape.elasticity = 0.5
        space.add(self.body, self.shape)
        self.links = []  # Liste des liens (constraints) avec d'autres Goos

    def add_link(self, space, other_goo):
        if other_goo not in self.links:
            rest_length = np.linalg.norm(np.array(self.body.position) - np.array(other_goo.body.position))
            constraint = pymunk.DampedSpring(self.body, other_goo.body, (0, 0), (0, 0), rest_length, SPRING_K, 0.1)
            space.add(constraint)
            self.links.append(other_goo)
            other_goo.links.append(self)

class Platform:
    def __init__(self, space, x, y, width, height):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.5
        space.add(self.body, self.shape)

def create_world():
    space = pymunk.Space()
    space.gravity = (0, GRAVITY * 100)
    
    platform_start = Platform(space, 100, 500, 200, 20)
    platform_end = Platform(space, 500, 200, 200, 20)
    
    goos = []
    first_goo = Goo(space, 150, 480)
    goos.append(first_goo)
    
    return space, [platform_start, platform_end], goos

def find_closest_link_target(goos, platforms, pos):
    closest_target = None
    min_distance = float('inf')
    
    for goo in goos:
        distance = np.linalg.norm(np.array(goo.body.position) - np.array(pos))
        if distance < min_distance and distance < 100:
            min_distance = distance
            closest_target = goo
    
    for platform in platforms:
        platform_pos = np.array(platform.body.position)
        distance = np.linalg.norm(platform_pos - np.array(pos))
        if distance < min_distance and distance < 100:
            min_distance = distance
            closest_target = platform
    
    return closest_target

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    space, platforms, goos = create_world()
    
    running = True
    mouse_pos = None
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        closest_target = find_closest_link_target(goos, platforms, mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                new_goo = Goo(space, *mouse_pos)
                goos.append(new_goo)
                if closest_target and isinstance(closest_target, Goo):
                    new_goo.add_link(space, closest_target)
                
        space.step(1/60.0)
        
        screen.fill((255, 255, 255))
        for platform in platforms:
            pygame.draw.rect(screen, (100, 100, 100), (*platform.body.position, 200, 20))
        for goo in goos:
            pygame.draw.circle(screen, (0, 0, 255), (int(goo.body.position.x), int(goo.body.position.y)), GOO_RADIUS)
            for link in goo.links:
                pygame.draw.line(screen, (0, 0, 0), (int(goo.body.position.x), int(goo.body.position.y)),
                                 (int(link.body.position.x), int(link.body.position.y)), 2)
        
        if closest_target:
            pygame.draw.line(screen, (150, 150, 150), mouse_pos, (int(closest_target.body.position.x), int(closest_target.body.position.y)), 1)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
