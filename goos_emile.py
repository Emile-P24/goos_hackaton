import pygame
import pymunk.pygame_util
import pymunk



# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Création de l'espace physique
space = pymunk.Space()
g = (50*9.81)
space.gravity = (0, g)  # Gravité vers le bas

# Objet statique
b0 = space.static_body

# Création d'une boule de Goo
radius = 20
mass = 0.4
moment = pymunk.moment_for_circle(mass, 0, radius)
goo_body = pymunk.Body(mass, moment)
goo_body.position = (400, 100)
goo_shape = pymunk.Circle(goo_body, radius)
goo_shape.elasticity = 0.8
space.add(goo_body, goo_shape)

# Sol
segment1 = pymunk.Segment(space.static_body, (0, 800), (800, 600), 10)
segment2 = pymunk.Segment(space.static_body, (0, 0), (0, 600), 10)
segment3 = pymunk.Segment(space.static_body, (0, 0), (800, 0), 10)
segment4 = pymunk.Segment(space.static_body, (800,0), (800, 600), 10)
segment1.elasticity = 0.8
segment2.elasticity = 0.8
segment3.elasticity = 0.8
segment4.elasticity = 0.8
space.add(segment1,segment2,segment3,segment4)

# Plateforme
plateforme = pymunk.Segment(space.static_body, (20, 300), (200, 300), 50)
plateforme.elasticity = 0.8
space.add(plateforme)
"""
# Liaison ponctuelle
class PinJoint:
    def __init__(self, b, b2, a=(0, 0), a2=(0, 0)):
        joint = pymunk.Constraint.PinJoint(b, b2, a, a2)
        space.add(joint)

PinJoint(plateforme,goo_body,goo_body.position)

# Ressort de torsion
class RotarySpring:
    def __init__(self, b, b2, angle, stiffness):
        joint = pymunk.Constraint.RotarySpring(
            b, b2, angle, stiffness)
        space.add(joint)
"""
# joint = pymunk.constraints.PinJoint(b0, goo_body, (600, 100))
joint = pymunk.constraints.DampedSpring(b0, goo_body,(400,0),(0,0), 300, 50,0.01)
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
    pygame.draw.circle(screen, (0, 0, 0), (600,100), 5)
    # Dessin du sol
    pygame.draw.line(screen, (0,0,0), (0, 600), (800, 600), 10)
    pygame.draw.line(screen, (0,0,0), (0,0), (0,600), 10)
    pygame.draw.line(screen, (0,0,0), (0,0), (800,0), 10)
    pygame.draw.line(screen, (0,0,0), (800,0), (800, 600), 10)
    # Dessin de plateforme
    pygame.draw.line(screen, (0,50,0), (20, 300), (200, 300),50)

    # Affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
