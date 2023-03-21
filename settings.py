class Settings() :
    """a class to control all of alien invasion's settings"""

    def __init__(self) :
        """initialize game settings"""
        #Screen settings.
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230, 230, 230)

        #Ship settings.
        self.ship_limit = 3

        #Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (150, 60, 60)
        self.bullets_allowed = 3

        #Alien settings
        self.alien_drop_speed = 10.0
        

        #How much the game's speed increases on each lvl up
        self.speedup_scale = 1.1

        #How much the aliens point value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) :
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #fleet_direction of 1 means right; -1 means left.
        self.fleet_direction = 1

        #Scoring.
        self.alien_points = 50

    def increase_speed(self) :
        """Increase speed settings and alien point value."""
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)