"""
Author: Hiheat
Github: Hieat

a bar class to display values
made for pygame
made for my other project  '1vs1KI'
"""

class Bar(pygame.sprite.Sprite):
    
    def __init__(self, start, color, width=5, height=20):
        self.value = start
        self.color = color
        self.width = width
        self.height = height
        self.create_image()
        
    def create_image(self):
        if self.value <= 0:
            self.image = pygame.Surface((1, self.height))
        else:
            self.image = pygame.Surface((self.value*self.width, self.height))
            self.image.fill(self.color)
        
    def remove(self, value):
        self.value -= value
        
    def set(self, value):
        self.value = value
        
    def add(self, value):
        self.value += value
        
    def divide(self, value):
        self.value /= value
        
    def multiply(self, value):
        self.value *= value
        
    def update(self):
        self.create_image()
