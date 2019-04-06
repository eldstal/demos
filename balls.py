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
space.gravity = 0,-500
window = pyglet.window.Window()

@window.event
def on_draw():
  window.clear()
  options = pymunk.pyglet_util.DrawOptions()
  space.debug_draw(options)

# 60FPS animations
pyglet.clock.schedule_interval(tick, 1/60)







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
    return self.position[1] < -10

class Box(pymunk.Body):
  def __init__(self, x, y, width, height, angle=0):
    pymunk.Body.__init__(self)

    self.position = (x, y)
    self.angle = angle
    self.shape = pymunk.Poly.create_box(self, size=(width,height), radius=0.01)
    self.body_type = pymunk.Body.STATIC

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

  # Balls all spawn in the same place
  scale = random.uniform(0.1,1)
  r = scale * 20
  b = Ball(window.width/2, window.height-100, r, mass=scale)

  # A slightly random upward kick
  direction = Vec2d(random.uniform(-1,1), 1)
  b.apply_impulse_at_world_point(scale * 300 * direction, b.position)

  balls += [ b ]
  space.add(b, b.shape)

# Ball spawner, 5 balls per second seems allright
pyglet.clock.schedule_interval(spawn_ball, 1/5)

ramp_l = Box(100,              100, 400, 10, angle=-math.pi/8)
ramp_r = Box(window.width-100, 100, 400, 10, angle=math.pi/8)
space.add(ramp_l, ramp_l.shape)
space.add(ramp_r, ramp_r.shape)


pyglet.app.run()
