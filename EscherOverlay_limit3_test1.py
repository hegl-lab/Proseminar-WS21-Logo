#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np

import drawSvg as draw
from drawSvg import Drawing
from hyperbolic import euclid, util
from hyperbolic.poincare.shapes import *
from hyperbolic.poincare import Transform
from hyperbolic.poincare.util import radialEuclidToPoincare, radialPoincareToEuclid, \
                                     poincareToEuclidFactor, triangleSideForAngles
import hyperbolic.tiles as htiles

stroke_width = 0.010

def draw_line(z1, z2, fill='grey', stroke_width=stroke_width):
    line = euclid.shapes.Line(z1.real, z1.imag, z2.real, z2.imag)
    d.draw(line, stroke='grey', stroke_width=stroke_width, fill='none')

def drawTiles(drawing, tiles):
    for tile in tiles:
        d.draw(tile, hwidth=0.02, fill='white')

p1 = 4
p2 = 3
q = 3
rotate = 0

theta1, theta2 = math.pi*2/p1, math.pi*2/p2
phiSum = math.pi*2/q
r1 = triangleSideForAngles(theta1/2, phiSum/2, theta2/2)
r2 = triangleSideForAngles(theta2/2, phiSum/2, theta1/2)

tGen1 = htiles.TileGen.makeRegular(p1, hr=r1, skip=1)
tGen2 = htiles.TileGen.makeRegular(p2, hr=r2, skip=1)

tLayout = htiles.TileLayout()
tLayout.addGenerator(tGen1, (1,)*p1)
tLayout.addGenerator(tGen2, (0,)*p2, htiles.TileDecoratorNull())
startTile = tLayout.defaultStartTile(rotateDeg=rotate)

t1 = startTile
t2 = tLayout.placeTile(t1.sides[-1])
t3 = tLayout.placeTile(t2.sides[-1])
pointBase = t3.vertices[-1]
points = [Transform.rotation(deg=i*360/p1).applyToPoint(pointBase)
          for i in range(p1)]
vertices = startTile.vertices
edges = []
for i, point in enumerate(points):
    v1 = vertices[i]
    v2 = vertices[(i+1)%p1]
    edge = Hypercycle.fromPoints(*v1, *v2, *point, segment=True, excludeMid=True)
    edges.append(edge)
decoratePoly = Polygon(edges=edges, vertices=vertices)
decorator1 = htiles.TileDecoratorPolygons(decoratePoly)
tLayout.setDecorator(decorator1, 0)

startTile = tLayout.defaultStartTile(rotateDeg=rotate)
tiles = tLayout.tilePlane(startTile, depth=6)

d = Drawing(2, 2, origin='center')
#d.draw(euclid.shapes.Circle(0, 0, 1), fill='silver')
for tile in tiles:
    d.draw(tile, hwidth=0.02, fill='black')
tiles[0].decorator = None

d.draw(euclid.shapes.Circle(0, 0, 1), stroke='black', stroke_width=stroke_width, fill='none')

d.setRenderSize(w=400)
d.saveSvg('escherOverlay_limit3_test1.svg')
d.savePng('escherOverlay_limit3_test1.png')