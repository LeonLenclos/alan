#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from gui import pygame_textinput, asciisprite
from alan import Alan

pygame.init()

alan = Alan(settings_files=['logic_all', 'base', 'interface_gui'])

# Foreground and background colors
fg_color = (255,255,255)
bg_color = (0,0,0)

# Create TextInput-object
textinput = pygame_textinput.TextInput(
    font_family="monospace",
    font_size=48,
    text_color=fg_color,
    cursor_color=fg_color,
    antialias=False
)

# Create Face
face = asciisprite.Face()

width, height = 600, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

while True:
    screen.fill(bg_color)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Update

    if textinput.update(events):
        text = textinput.get_text()
        textinput.clear_text()
        alan.get_response(text)

    while textinput.get_surface().get_width() > width:
        textinput.set_font_size(textinput.font_size - 1)
        print(textinput.font_size)
        textinput.update(events)

    face.update(10)

    # Blit
    screen.blit(textinput.get_surface(), (10, 10))
    screen.blit(face.get_surface(5), (10,50))

    pygame.display.update()
    clock.tick(30)
