"""Class representing the map of the game"""
import pygame
from src.engine.tools import load_texture
from src.level.CLevel import CLevel

class CMap():
    """Class representing the map of the game"""
    def __init__(self, player, hud, data):
        """constructor for cmap

        Args:
            player (CPlayer): Player moving the the map
            hud (CHud): Hud of the game
            data (dict): json data for the cmap
        """
        self.m_player = player
        self.m_hud = hud
        self.image = load_texture('textures/base_camp.png')
        self.rect = self.image.get_rect()
        self.rect.x = data["x"]
        self.rect.y = data["y"]
        self.collision_up = False
        self.collision_down = False
        self.collision_left = False
        self.collision_right = False

        self.m_levels = [CLevel.from_dict(level, self.m_player) for level in data["levels"]]
        x = 1
        for item in self.m_levels[0].m_interactive_items:
            item.m_data = self.m_levels[x]
            x+=1
        self.m_levels[1].m_interactive_items[0].m_data = self.m_levels[0]
        self.m_levels[2].m_interactive_items[0].m_data = self.m_levels[0]
        self.m_levels[3].m_interactive_items[0].m_data = self.m_levels[0]
        self.m_levels[4].m_interactive_items[0].m_data = self.m_levels[0]
        self.m_levels[5].m_interactive_items[0].m_data = self.m_levels[0]

        self.m_hud.m_active_level = self.m_levels[0]
        self.m_levels[1].m_unlocked = True
        self.m_hud.m_interactive_items = self.m_hud.m_active_level.m_interactive_items
        # self.m_player.m_real_pos_x = self.m_hud.m_active_level.m_player_start_x
        # self.m_player.m_real_pos_y = self.m_hud.m_active_level.m_player_start_y
        # self.m_player.rect.center = (self.m_hud.m_active_level.m_player_start_x, self.m_hud.m_active_level.m_player_start_y)

    def movement(self)->None:
        """Represents basic movement on the map for both player and other objects placed in the scene
        """
        if self.m_hud.m_active_level.m_index == 0:
            self.m_levels[0].m_unlocked = False
            if not self.m_hud.m_active_level_index >= len(self.m_levels):
                self.m_levels[self.m_hud.m_active_level_index].m_unlocked = True
        #print(self.m_hud.m_active_level)
        # Collisions checks
        self.check_for_outer_collision()
        # Player checks
        self.m_player.check_attack_cooldown()
        # Key input checks
        self.handle_key_input()

        # if len(self.m_hud.m_active_level.m_enemies) == 0:
        #     self.m_levels[]

    def check_for_outer_collision(self)->None:
        """Checks for collision
        """
        border_width = 12
        col_flag =  self.m_hud.m_active_level.m_collision_manager.check_for_collisions(self.m_player)
        if self.m_player.m_real_pos_y <= 0 + border_width + self.m_player.rect.height/2 or col_flag == 1:
            self.collision_up = True
        else:
            self.collision_up = False
        if self.m_player.m_real_pos_y >= self.rect.height - border_width - self.m_player.rect.height/2 or col_flag == 0:
            self.collision_down = True
        else:
            self.collision_down = False
        if self.m_player.m_real_pos_x <= 0 + border_width + self.m_player.rect.width/2 or col_flag == 3:
            self.collision_left = True
        else:
            self.collision_left = False
        if self.m_player.m_real_pos_x >= self.rect.width - border_width - self.m_player.rect.width/2 or col_flag == 2:
            self.collision_right = True
        else:
            self.collision_right = False

    def move_items_up(self)->None:
        """Moves all items up if player goes down
        """
        for item in self.m_hud.m_active_level.m_interactive_items:
            item.rect.y += self.m_player.m_speed

        for enemy in self.m_hud.m_active_level.m_enemies:
            enemy.rect.y += self.m_player.m_speed
            enemy.m_destination[1] += self.m_player.m_speed
            enemy.m_center_y += self.m_player.m_speed
            for projectile in enemy.m_projectiles:
                projectile.rect.y += self.m_player.m_speed

        for trap in self.m_hud.m_active_level.m_traps:
            trap.rect.y += self.m_player.m_speed
    def move_items_down(self):
        """Moves all items down if player goes up
        """
        for item in self.m_hud.m_active_level.m_interactive_items:
            item.rect.y -= self.m_player.m_speed

        for enemy in self.m_hud.m_active_level.m_enemies:
            enemy.rect.y -= self.m_player.m_speed
            enemy.m_destination[1] -= self.m_player.m_speed
            enemy.m_center_y -= self.m_player.m_speed
            for projectile in enemy.m_projectiles:
                projectile.rect.y -= self.m_player.m_speed
        for trap in self.m_hud.m_active_level.m_traps:
            trap.rect.y -= self.m_player.m_speed
    def move_items_left(self):
        """Moves all items left if player goes right
        """
        for item in self.m_hud.m_active_level.m_interactive_items:
            item.rect.x += self.m_player.m_speed

        for enemy in self.m_hud.m_active_level.m_enemies:
            enemy.rect.x += self.m_player.m_speed
            enemy.m_destination[0] += self.m_player.m_speed
            enemy.m_center_x += self.m_player.m_speed
            for projectile in enemy.m_projectiles:
                projectile.rect.x += self.m_player.m_speed
        for trap in self.m_hud.m_active_level.m_traps:
            trap.rect.x += self.m_player.m_speed
    def move_items_right(self):
        """Moves all items right if player goes left
        """
        for item in self.m_hud.m_active_level.m_interactive_items:
            item.rect.x -= self.m_player.m_speed

        for enemy in self.m_hud.m_active_level.m_enemies:
            enemy.rect.x -= self.m_player.m_speed
            enemy.m_destination[0] -= self.m_player.m_speed
            enemy.m_center_x -= self.m_player.m_speed
            for projectile in enemy.m_projectiles:
                projectile.rect.x -= self.m_player.m_speed
        for trap in self.m_hud.m_active_level.m_traps:
            trap.rect.x -= self.m_player.m_speed
    def handle_key_input(self):
        """handles user input
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w] and not self.collision_up:
            if self.m_player.is_on_up_edge():
                self.rect.y += self.m_player.m_speed
                self.move_items_up()
                self.m_player.m_movement.moving_up(False)
            else:
                self.m_player.m_movement.moving_up(True)
        elif pressed_keys[pygame.K_s] and not self.collision_down:
            if self.m_player.is_on_down_edge():
                self.rect.y -= self.m_player.m_speed
                self.move_items_down()
                self.m_player.m_movement.moving_down(False)
            else:
                self.m_player.m_movement.moving_down(True)
        elif pressed_keys[pygame.K_a] and not self.collision_left:
            if self.m_player.is_on_left_edge():
                self.rect.x += self.m_player.m_speed
                self.move_items_left()
                self.m_player.m_movement.moving_left(False)
            else:
                self.m_player.m_movement.moving_left(True)
        elif pressed_keys[pygame.K_d] and not self.collision_right:
            if self.m_player.is_on_right_edge():
                self.rect.x -= self.m_player.m_speed
                self.move_items_right()
                self.m_player.m_movement.moving_right(False)
            else:
                self.m_player.m_movement.moving_right(True)
        if pressed_keys[pygame.K_q] and not self.m_player.m_attacking:
            self.m_player.attack()
        if(
        pressed_keys[pygame.K_w] == False and
        pressed_keys[pygame.K_s] == False and
        pressed_keys[pygame.K_a] == False and
        pressed_keys[pygame.K_d] == False and
        not self.m_player.m_attacking):
            self.m_player.image = self.m_player.m_standing_textures[self.m_player.m_movement.m_last_direction]
    def render(self, screen)->None:
        """Renders everything onto the scren

        Args:
            screen (pygame.surface): pygame.surface object
        """
        self.image = load_texture(self.m_hud.m_active_level.m_texture)
        if self.m_hud.m_new_rect:
            self.rect.x = 0
            self.rect.y = 0
            self.rect = self.image.get_rect()
            self.m_hud.m_new_rect = False
        screen.blit(self.image, self.rect)
        self.m_hud.m_active_level.render(screen)

    def to_dict(self)->dict:
        """Convets CMap into json dict format

        Returns:
            dict: Returns json dict format representing CMap instance
        """
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "levels": [level.to_dict() for level in self.m_levels]
        }
