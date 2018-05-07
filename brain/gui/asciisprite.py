""" Inspirated and partly taken from the game Gorillas.py by Al Sweigart.
Visit him (and learn programming games) at:

        http://inventwithpython.com

"""
# From :http://www.pygame.org/project/1808/3164

import pygame
from pygame.locals import SRCALPHA
pygame.init()

class Image:
    def __init__(self, ascii, colours={'X': (255, 255, 255)}, scale=1):
        self.ascii      = ascii
        self.scale      = scale
        self.colours    = {}
        for colour in colours:
            self.colours[colour] = colours[colour]
        self.update()

    def update(self):
        ''' Update everything. '''
        self.update_ascii()
        self.update_colours()

    def update_ascii(self):
        ''' Call this after You changed self.ascii. '''
        self.asciilist  = self.ascii.split('\n')[1:-1]
        self.width      = max([len(x) for x in self.asciilist])
        self.height     = len(self.asciilist)
        self.surface    = pygame.Surface((self.width, self.height), SRCALPHA, 32)
        try: self.surface.fill(self.colours['bg'])
        except KeyError: self.surface.fill((0,0,0,0))
        self.update_colours()

    def update_colours(self):
        ''' Call this after You changed self.colours. '''
        for colour in self.colours:
            self.update_colour(colour)

    def update_colour(self, colour):
        ''' Update a single colour. Used internally. '''
        if colour in self.colours:
            for y in range(self.height):
                for x in range(len(self.asciilist[y])): # modified by Léon
                    if self.asciilist[y][x] == colour:
                        self.surface.set_at((x, y), self.colours[colour])

    def set_colour(self, key, value):
        ''' Set the colour of any byte in self.colours.'''
        self.colours[key] = value
        self.update_colour(key)

    def set_colours(self, colours):
        for i in colours:
            self.colours[i] = colours[i]
        self.update_colours()

    def set_ascii(self, ascii):
        self.ascii = ascii
        self.update_ascii()

    def get_surface(self):
        return self.surface

class Animation:
    ''' self.frames are the indexes in self.timeline of self.images,
        which are the Image(object)s. '''
    def __init__(self, asciis, timeline=[0], colours={'X': (255, 255, 255, 255)}):
        self.frames     = {}
        self.timeline   = timeline
        for i, img in enumerate(asciis):
            self.frames[i] = Image(img, colours)
        self.curframe   = 0
        self.update_curframe()
        self.update_frames()

    def update_curframe(self):
        ''' Update current shown Image. '''
        self.curimage = self.frames[self.timeline[self.curframe]]
        self.surface = self.curimage.get_surface()

    def update_frames(self):
        for i in self.frames:
            self.frames[i].update()

    def set_colours(self, colours):
        for i in self.frames:
            self.frames[i].set_colours(colours)

    def set_colour(self, key, value):
        for i in self.frames:
            self.frames[i].set_colour(key, value)

    def swap(self, amount = 1):
        if self.curframe + amount > len(self.timeline) -1:
            self.curframe = 0
        else:
            self.curframe += amount
        self.update_curframe()

    def get_image(self):
        frames = []
        for i in self.timeline:
            frames.append(self.frames[i])
        return frames

    def get_frames(self):
        images = []
        for i in self.timeline:
            images.append(self.frames[i].surface)
        return images

    def get_asciis(self):
        asciis = {}
        for i in self.frames:
            asciis[i] = self.frames[i].ascii
        return asciis

    def get_surface(self):
        return self.surface


from . import asciisprite_data as data

class Face:
    def __init__(self):
        self.surface = pygame.Surface((16, 14), SRCALPHA, 32)

        self.eye = Animation(data.eye, data.blink, data.palette)
        self.nose = Image(data.nose, data.palette)
        self.mouth = Image(data.mouth, data.palette)
        self.frm_duration = 0

    def update(self, slowness=1):
        if self.frm_duration <= 0:
            self.frm_duration = slowness
            self.surface.fill((0,0,0,0))
            self.eye.swap()
            self.surface.blit(self.eye.get_surface(),  (0    , 0))
            self.surface.blit(self.eye.get_surface(),  (5 + 6, 0))
            self.surface.blit(self.nose.get_surface(), (5 + 3, 4))
            self.surface.blit(self.mouth.get_surface(),(5    , 10))
        self.frm_duration -= 1

    def get_surface(self, scale=1):
        size = self.surface.get_width()*scale, self.surface.get_height()*scale
        return pygame.transform.scale(self.surface, size)
