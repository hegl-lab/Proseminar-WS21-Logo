#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, pathlib

import math
import drawSvg
from hyperbolic import euclid
from hyperbolic.poincare.shapes import Horocycle, Line, Ideal, Point


nb_geodesics, nb_horocycles = 2, 0
stroke_width = 0.015
hyp_width = True
draw_arrow = False
horo_angle = 0*math.pi


def draw_horocycle(horo, color='black', hyp=hyp_width):
    if hyp:
        d.draw(horo, hwidth=5*stroke_width, fill=color)  
    else:
        d.draw(horo, stroke_width=stroke_width, fill='none', stroke=color)  

def draw_geodesic(angle1, angle2, color='black', stroke_width=stroke_width, hyp=hyp_width):
    '''Draw the geodesic between ideal points given by their angles on the unit circle'''
    geodesic = Line.fromPoints(*Ideal.fromRadian(angle1), *Ideal.fromRadian(angle2))
    if hyp:
        d.draw(geodesic, hwidth=7*stroke_width, fill=color)
    else:
        d.draw(geodesic, stroke=color, stroke_width=stroke_width, fill='none')

def draw_line(z1, z2, color='black', stroke_width=stroke_width):
    line = euclid.shapes.Line(z1.real, z1.imag, z2.real, z2.imag)
    d.draw(line, stroke=color, stroke_width=stroke_width, fill='none')

d = drawSvg.Drawing(2.1, 2.1, origin='center')
d.draw(euclid.shapes.Circle(0, 0, 1), stroke='none', fill='none')

# d.draw(drawSvg.Rectangle(-1,-1,2,2, fill=color_background))

N = nb_geodesics + 1
#angles = [horo_angle + 2*math.pi*i/N for i in range(1,N)]
#for i in range(nb_geodesics):
draw_geodesic(0, 2/3*math.pi, color='black')
draw_geodesic(0, 2/3*math.pi, color='black', hyp=False, stroke_width=0.015)

draw_geodesic(-1/3*math.pi, 4/3*math.pi, color='black')
draw_geodesic(-1/3*math.pi, 4/3*math.pi, color='black', hyp=False, stroke_width=0.015)

M = nb_horocycles + 1
xList = [-1 + 2*i/M + 0.05 for i in range(1, M)]
horoList = [Horocycle.fromClosestPoint(Point(math.cos(math.pi + horo_angle)*x, math.sin(math.pi + horo_angle)*x), surroundOrigin=(x>0)) for x in xList]
for i in range(nb_horocycles):
    draw_horocycle(horoList[i], color='black')


if draw_arrow:
    a = 5*stroke_width
    z1 = -0.55-a -a*1j
    z2 = -0.55 + a
    z3 = -0.55-a + a*1j
    draw_line(z1, z2, stroke_width=1.5*stroke_width, color='black')
    draw_line(z2, z3, stroke_width=1.5*stroke_width, color='black')

draw_line(complex(math.cos(6*math.pi/7), math.sin(6*math.pi/7)), complex(math.cos(math.pi+math.pi/4), math.sin(math.pi+math.pi/4)), stroke_width=stroke_width)
#draw_line(complex(math.cos(2*(math.pi/3)), math.sin(2*(math.pi/3))), complex(math.cos(math.pi + 2*(math.pi/3)), math.sin(math.pi + 2*(math.pi/3))), stroke_width=stroke_width)
draw_line(complex(math.cos(5*math.pi/6), math.sin(5*math.pi/6)), complex(math.cos(math.pi + (5*math.pi/6)), math.sin(math.pi + (5*math.pi/6))), stroke_width=2*stroke_width)

d.draw(euclid.shapes.Circle(0, 0, 1), stroke='black', stroke_width=2*stroke_width, fill='none')

d.setRenderSize(w=279)
d.savePng('HEGL_horocycle_test.png')
d.saveSvg('HEGL_horocycle_test.svg')