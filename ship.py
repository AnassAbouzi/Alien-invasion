import pygame
from pygame.sprite import Sprite

class Ship(Sprite) :
    """a class that manages the ship"""
    def __init__(self, ai_game) :
        """initialize the ship"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #load the ship image
        self.image = pygame.image.load(r"C:\\Users\\anass\\Desktop\\python\\alien_invasion\\images\\ship.bmp")
        self.rect = self.image.get_rect()

        #start each ship at the bottom middle of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        #movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self) :
        """Update the ship's position based on the mouvement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0 :
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self) :
        """draw the ship at it's current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self) :
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)