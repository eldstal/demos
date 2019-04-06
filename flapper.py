#!/usr/bin/env python3

import math
import random

import pyglet
from pyglet.gl import *

import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pyglet_util



def tick(dt):
  space.step(dt)

#
# "Engine"
#

space = pymunk.Space()
space.iterations = 20
space.gravity = 0,0
window = pyglet.window.Window()

@window.event
def on_draw():
  window.clear()
  options = pymunk.pyglet_util.DrawOptions()
  space.debug_draw(options)

# 60FPS animations
pyglet.clock.schedule_interval(tick, 1/60)


earth = pymunk.Body(9000000, pymunk.inf)
earth.body_type = pymunk.Body.STATIC
earth.position = (window.width/2, window.height/2)
space.add(earth)





#
# Demo
#

class Ball(pymunk.Body):
  def __init__(self, x, y, r, mass=1):
    moment = pymunk.moment_for_circle(mass, 0, r, (0, 0))
    pymunk.Body.__init__(self, mass, moment)

    self.position = (x, y)
    self.shape = pymunk.Circle(self, r)
    self.body_type = pymunk.Body.DYNAMIC

    self.shape.friction = 1
    self.shape.elasticity = 0.4

  def is_out(self):
    if self.position[0] < -10: return True
    if self.position[0] > window.width + 10: return True
    if self.position[1] < -10: return True
    if self.position[1] > window.height + 10: return True
    return False

class Box(pymunk.Body):
  def __init__(self, x, y, width, height, angle=0):
    mass = 10
    moment = pymunk.moment_for_box(mass, (width,height))
    pymunk.Body.__init__(self, mass, moment)

    self.position = (x, y)
    self.angle = angle
    self.shape = pymunk.Poly.create_box(self, size=(width,height), radius=0.01)
    self.body_type = pymunk.Body.DYNAMIC

    self.shape.friction = 1
    self.shape.elasticity = 0.95

balls = []
def cleanup_balls():
  global balls

  for b in balls:
    if b.is_out():
      space.remove(b, b.shape)

  balls = [ b for b in balls if not b.is_out() ]

def spawn_ball(dt):
  global balls

  cleanup_balls()
  if (len(balls) > 100):
    return

  # Balls all at a random part of the screen
  scale = random.uniform(0.4,1)
  r = scale * 20
  x = random.uniform(0, window.width)
  y = random.uniform(0, window.height)
  b = Ball(x, y, r, mass=scale)


  balls += [ b ]
  space.add(b, b.shape)

# Ball spawner, 5 balls per second seems allright
pyglet.clock.schedule_interval(spawn_ball, 1/5)

# A board in the middle of the screen
flapper = Box(window.width/2, window.height/2, 300, 10)
space.add(flapper, flapper.shape)

# Let the board spin freely
ax = pymunk.constraint.PinJoint(flapper, earth)
ax.error_bias = 0
motor = pymunk.constraint.SimpleMotor(flapper, earth, rate=2*math.pi)
motor.max_force = 80000

space.add(ax, motor)


pyglet.app.run()
