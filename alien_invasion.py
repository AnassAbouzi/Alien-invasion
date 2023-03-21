import sys
import pygame
from time import sleep


from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion() :
    """globale class that manages the game"""
    def __init__(self) :
        """initialize the game"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game statistics.
        self.stats = GameStats(self)

        #Create an instance for the scoreboard
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make play button
        self.play_button = Button(self, "Play")

        #Set background-color
        self.bg_color = self.settings.bg_color 
        

    

    def run_game(self) :
        """start the main loop of the game"""
        while True :
            self._check_events()

            if self.stats.game_active :
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self) :
        """listening for events"""
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                sys.exit()
            elif event.type == pygame.KEYDOWN :
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP :
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN :
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos) :
        """Starts a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active :
            #Reset game settings.
            self.settings.initialize_dynamic_settings()

            #Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #Remove any remaining aliens or bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            #Hide mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event) :
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT :
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT :
             self.ship.moving_left = True
        elif event.key == pygame.K_q :
            sys.exit()
        elif event.key == pygame.K_SPACE :
            self.fire_bullet()

    def _check_keyup_event(self, event) :
        """Responds to key releases."""
        if event.key == pygame.K_RIGHT :
                self.ship.moving_right = False
        elif event.key == pygame.K_LEFT :
                self.ship.moving_left =False
                
    def fire_bullet(self) :
        """Create a new bullet and add it to the bullets groupe."""
        if len(self.bullets) < self.settings.bullets_allowed :
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self) :
        """Update position of bullets and remove old ones"""
        #update bullets position
        self.bullets.update()
            
        #Get remove bullets after they disapear
        for bullet in self.bullets.copy() :
            if bullet.rect.bottom <= 0 :
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self) :
        """Respond to bullet-alien collisions"""
        #Check if any bullet hit an alien
        #if so remove both the alien and the bullet
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                    True, True)

        if collisions :
            for alien in collisions.values() :
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()

        #Check if fleet is destroyed
        if not self.aliens :
            #Remove all bullets and call another fleet
            self.bullets.empty()
            self._create_fleet() 
            self.settings.increase_speed()

            #Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self) :
        """Update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        #Look for ship-alien collisions 
        if pygame.sprite.spritecollideany(self.ship, self.aliens) :
            self._ship_hit()

        #Check for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _create_fleet(self) :
        """Create the fleet of aliens"""
        #Create an alien and calculate the number of aliens in a row.
        #Spacing between aliens is equal to the width of one alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width) 

        #Determine the number of rows of aliens we can fit in the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height) 
        
        #Create the full fleet of aliens.
        for row_number in range(number_rows) :
            for alien_number in range(number_aliens_x) :
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number) :
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (alien_number * alien_width * 2)
        alien.rect.x = alien.x
        alien.rect.y = alien_height + (row_number * alien_height * 2)
        self.aliens.add(alien)

    def _check_fleet_edges(self) :
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites() :
            if alien.check_edges() :
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) :
        """Drop the entire fleet and change the direction"""
        for alien in self.aliens.sprites() :
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self) :
        """Respond to ship-alien collision"""
        if self.stats.ships_left > 0 :
            #Decrement ships left and update soreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #remove any aliens or bullets left
            self.bullets.empty()
            self.aliens.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else :
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self) :
        """Check if any alien have reached the bottom of the screen"""
        self.screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites() :
            if alien.rect.bottom >= self.screen_rect.bottom :
                #Treat this case the same way we treated ship-alien collision
                self._ship_hit()
                break   

    def _update_screen(self) :
        """sets the initial window of the game and updates it"""
        #changing background-color
        self.screen.fill(self.bg_color)
        #render the ship
        self.ship.blitme()
        #draw each bullet in the bullets groupe.
        for bullet in self.bullets :
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Draw the score information
        self.sb.show_score()

        #Display the play button if the game is inactive
        if not self.stats.game_active :
            self.play_button.draw_button()

        #refresh window
        pygame.display.flip()

if __name__ == "__main__" :
    ai = AlienInvasion()
    ai.run_game()