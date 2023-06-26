import random
import pygame
import numpy as np

from scipy.integrate import odeint

class Lorenz:
    def __init__(self):
        self.xMin, self.xMax = -30.0,30.0
        self.yMin, self.yMax = -30.0, 30.0
        self.zMin, self.zMax = 0.0,50.0
        self.X, self.Y, self.Z = 0.1, 0.0, 0.0
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        #dt = 0.00009999
        self.dt = 0.00009999
        self.a, self.b,self.c = 10, 28, 8/3
        self.pixelColor = (255,0,0)

        self.initX, self.initY, self.initZ = self.X, self.Y, self.Z
        self.states = None
        self.count = 0
        self.numFrames = 0


    def step(self):
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * self.a * (self.Y - self.X))
        self.Y = self.Y + (self.dt * (self.X *(self.b-self.Z) - self.Y))
        self.Z = self.Z + (self.dt * (self.X * self.Y - self.c * self.Z))

    def F(self, inputX, tempT, a, b, c):
        tx, ty, tz = inputX
        dXdt = [a * (ty-tx), tx * (b-tz), tx*ty - c*tz]
        return dXdt

    def solve(self):
        state0 = [self.initX, self.initY, self.initZ]
        tempT = np.arange(0.0,80.0, self.dt)
        self.states = odeint(self.F, state0, tempT, args = (self.a, self.b, self.c))
        self.numFrames = self.states.shape

    def step3(self):
        if self.count < self.numFrames[0]:
            self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
            self.X = self.states[self.count, 0]
            self.Y = self.states[self.count, 1]
            self.Z = self.states[self.count, 2]
            self.count +=1


    def draw(self, displaySurface):
        width, height = displaySurface.get_size()
        oldPos = self.ConvertToScreen(self.oX, self.oY, self.xMin, self.xMax, self.yMin, self.yMax, width, height)
        newPos = self.ConvertToScreen(self.X, self.Y, self.xMin, self.xMax, self.yMin, self.yMax, width, height)

        newRect = pygame.draw.line(displaySurface, self.pixelColor, oldPos, newPos, width=2)

        return newRect
    def ConvertToScreen(self, x, y, xMin, xMax, yMin, yMax, width, height):
        newX = width * ((x-xMin) / (xMax - xMin))
        newY = height * ((y-yMin) / (yMax - yMin))
        return round(newX, 0), round(newY, 0)

class Application:
    def __init__(self):
        self.isRunning = True
        self.displaySurface = None
        self.fpsClock = None
        self.attractors = []
        self.size = self.width, self.height = 1920, 1080
        self.count = 0
        self.outputCount = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Lorenz Attractor")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.isRunning = True
        self.fpsClock = pygame.time.Clock()

        color = []
        color.append((19,49,111))
        color.append((201,0,64))
        #color.append((255,255, 255))

        for i in range(len(color)):
            self.attractors.append(Lorenz())

            #self.attractors[i].X = random.uniform(0.01, 0.101)
            self.attractors[i].initX = random.uniform(0.1, 0.101)

            self.attractors[i].pixelColor = color[i]

            self.attractors[i].solve()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        for x in self.attractors:
            x.step3()

    def on_render(self):
        for x in self.attractors:
            newRect = x.draw(self.displaySurface)
            pygame.display.update(newRect)

    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

            self.fpsClock.tick()
            self.count += 1

        pygame.quit()

if __name__ == '__main__':
     t = Application()
     t.on_execute()
