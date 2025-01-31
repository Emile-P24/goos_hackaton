import pygame
import pymunk

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Création de l'espace physique
space = pymunk.Space()
g = (50*9.81)
space.gravity = (0, g)  # Gravité vers le bas

# Création d'une boule de Goo
radius = 20
mass = 0.4
moment = pymunk.moment_for_circle(mass, 0, radius)
goo_body = pymunk.Body(mass, moment)
goo_body.position = (400, 100)
goo_shape = pymunk.Circle(goo_body, radius)
goo_shape.elasticity = 0.5
space.add(goo_body, goo_shape)

# Sol
segment = pymunk.Segment(space.static_body, (0, 500), (800, 500), 5)
segment.elasticity = 0.8
space.add(segment)

# Plateforme
plateforme = pymunk.Segment(space.static_body, (20, 300), (200, 300), 50)
plateforme.elasticity = 0.8
space.add(plateforme)

# Ressort de torsion
class RotarySpring:
    def __init__(self, b, b2, angle, stiffness):
        joint = pymunk.constraint.RotarySpring(
            b, b2, angle, stiffness)
        space.add(joint)
        
# Boucle du jeu
running = True
while running:
    screen.fill((200, 200, 255))  # Fond bleu ciel
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de la physique
    space.step(1/60.0)

    # Dessin de la boule
    pygame.draw.circle(screen, (0, 0, 0), (int(goo_body.position.x), int(goo_body.position.y)), radius)
    
    # Dessin du sol
    pygame.draw.line(screen, (0,0,0), (0, 500), (800, 500), 5)
    
    # Dessin de plateforme
    pygame.draw.line(screen, (0,50,0), (20, 300), (200, 300), 50)

    # Affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
