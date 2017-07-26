"""
    font.py -- Displays FPS in OpenGL using TrueType fonts.

    Copyright (c) 2002. Nelson Rush. All rights reserved.

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

from OpenGL.GL import *
from OpenGL.GLU import *

from pygame.locals import *
from pygame.display import *
from pygame.event import *
from pygame.key import *
from pygame.mouse import *
from pygame.font import *
from pygame.image import *
from pygame.time import *
from pygame import *
import sys

class Engine:
    def __init__(self,w,h):
        init()
        display.init()
        display.set_mode([w,h], DOUBLEBUF|OPENGL|HWPALETTE|HWSURFACE)
        self.initgl()
        self.resize(w,h)
        mouse.set_visible(0)
        self.w = w
        self.h = h
        font.init()
        if not font.get_init():
            print 'Could not render font.'
            sys.exit(0)
        self.font = font.Font('font.ttf',18)
        self.char = []
        for c in range(256):
            self.char.append(self.CreateCharacter(chr(c)))
        self.char = tuple(self.char)
        self.lw = self.char[ord('0')][1]
        self.lh = self.char[ord('0')][2]
        self.angle = 0.0
        self.frames = self.t = self.t_start = self.fps = 0
    def initgl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glShadeModel(GL_SMOOTH)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    def resize(self,w,h):
        if h == 0: h = 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w) / float(h), 0.5, 150.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def CreateCharacter(self, s):
        try:
            letter_render = self.font.render(s, 1, (255,255,255), (0,0,0))
            letter = image.tostring(letter_render, 'RGBA', 1)
            letter_w, letter_h = letter_render.get_size()
        except:
            letter = None
            letter_w = 0
            letter_h = 0
        return (letter, letter_w, letter_h)
    def textView(self):
        glViewport(0,0,self.w,self.h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.w - 1.0, 0.0, self.h - 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def Print(self,s,x,y):
        s = str(s)
        i = 0
        lx = 0
        length = len(s)
        self.textView()
        glPushMatrix()
        while i < length:
            glRasterPos2i(x + lx, y)
            ch = self.char[ ord( s[i] ) ]
            glDrawPixels(ch[1], ch[2], GL_RGBA, GL_UNSIGNED_BYTE, ch[0])
            lx += ch[1]
            i += 1
        glPopMatrix()
    def DrawFPS(self, x, y):
        self.t = time.get_ticks()
        self.frames += 1
        if self.t - self.t_start > 1000:
            self.fps = self.frames * 1000 / (self.t - self.t_start)
            self.t_start = self.t
            self.frames = 0
        self.Print(self.fps, x, y)
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.resize(self.w,self.h)
        glTranslatef(0.0, 0.0, -6.0)
        glPushMatrix()
        glRotatef(self.angle, 0.0, 1.0, 0.0)
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glVertex3f(1.0, -1.0, 0.0)
        glEnd()
        glPopMatrix()

        self.DrawFPS(self.w - (self.lw * 3), self.h - self.lh)

        self.angle += 1.0
    def run(self):
        while 1:
            e = event.poll()
            k = key.get_pressed()
            if e.type == KEYDOWN and e.key == K_ESCAPE: break
            self.draw()
            display.flip()

if __name__ == '__main__':
    engine = Engine(640,480)
    engine.run()
    font.quit()
    display.quit()
