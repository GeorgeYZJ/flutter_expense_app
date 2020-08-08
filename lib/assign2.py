import pygame
from random import randint, uniform, choice
import math

vector = pygame.math.Vector2
gravity = vector(0, 0.25)
WIDTH = HEIGHT = 800

class Particle:
    def __init__(self, x, y, firework, color):
        self.firework = firework
        self.pos = vector(x, y)
        self.origin = vector(x, y)

        self.radius = 30
        self.remove = False
        self.ex_radius = randint(10, 16)
        self.life = 0
        self.acc = vector(0, 0)

        if self.firework:
            self.vel = vector(0, -randint(15, 18))
            self.size = 3
            self.color = color 
        else:
            self.vel = vector(uniform(-1, 1), uniform(-1, 1))
            self.vel.x *= randint(10, 14)
            self.vel.y *= randint(10, 14)
            self.size = randint(1, 3)
            self.color = choice(color)

    def _apply_force(self, force):
        self.acc += force
    
    def move(self):
        if not self.firework:
            self.vel.x *= 0.8
            self.vel.y *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.life == 0 and not self.firework:
            distance = math.sqrt((self.pos.x - self.origin.x) ** 2 + (self.pos.y - self.origin.y) ** 2)
            if distance > self.ex_radius:
                self.remove = True

        self._decay()
        self.life += 1

    def show(self, win):
        pygame.draw.circle(win, (self.color[0], self.color[1], self.color[2], 0), (int(self.pos.x), int(self.pos.y)), self.size)

    def _decay(self):
        if 50 > self.life > 10:
            rand = randint(0, 30)
            if rand == 0:
                self.remove = True
        elif self.life > 50:
            rand = randint(0, 5)
            if rand == 0:
                self.remove = True


class Firework:
    def __init__(self):
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.colors = ((randint(0, 255), randint(0, 255), randint(0, 255)), (randint(0, 255), randint(0, 255), randint(0, 255)), (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.firework = Particle(randint(0, WIDTH), HEIGHT, True, self.color)
        self.exploded = False
        self.particles = []

        self.min_max_particles = vector(75, 200)

    def update(self, win):
        if not self.exploded:
            self.firework._apply_force(gravity)
            self.firework.move()
            self.show(win)

            if  self.firework.vel.y >= 0:
                self.exploded = True
                self.explode()
        else:
            for particle in self.particles:
                particle._apply_force(gravity)
                particle.move()
                particle.show(win)

    def explode(self):
        amount = randint(self.min_max_particles.x, self.min_max_particles.y)
        for i in range(amount):
            self.particles.append(Particle(self.firework.pos.x, self.firework.pos.y, False, self.colors))

    def show(self, win):
        pygame.draw.circle(win, self.color, (int(self.firework.pos.x), int(self.firework.pos.y)), self.firework.size)

    def remove(self):
        if self.exploded:
            for particle in self.particles:
                if particle.remove is True:
                    self.particles.remove(particle)
            
            if len(self.particles) == 0:
                return True
            else:
                return False

def update(win, fireworks):
    for fw in fireworks:
        fw.update(win)
        if fw.exploded is True and fw.particles[0].life == 0:
            pass
        if fw.remove():
            fireworks.remove(fw)
    pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption("Fireworks with PyGame")
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    fireworks = [Firework() for i in range(1)]
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        win.fill((20, 20, 30))

        if randint(0, 20) == 1:
            fireworks.append(Firework())

        update(win, fireworks)
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()