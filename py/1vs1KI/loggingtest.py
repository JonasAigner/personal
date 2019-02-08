import logging
import pygame
import os
import time

logging.basicConfig(filename="log.log", level=logging.INFO)


def Logger1():
	logger = logging.getLogger("Logger_1")
	logger.setLevel(logging.DEBUG)
	logger.debug("in der Funktion")
	
#Logger1()


#clickable GUI

# mit os.system("echo") kann man Befehle in der Windows Command Shell ausführen (echo war nur ein Beispiel)


pygame.init()
#pygame.font

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 500))

# pick a font you have and set its size
myfont = pygame.font.Font("freesansbold.ttf", 30)
# apply it to text on a label
label = myfont.render("Python and Pygame are Fun!", 1, (255, 255, 255))
# put the label object on the screen at point x=100, y=100
screen.blit(label, (100, -50))





