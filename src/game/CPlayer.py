"""Class representing the player in the game"""
import pygame
from src.engine.tools import load_texture, inside_circle, distance_of_two_points
from src.movement.CMovement import CMovement

class CPlayer():
    """Class representing the player in the game"""
    def __init__(self, data):
        """constructor for CPlayer

        Args:
            data (dict): json dict with data for cplayer instance
        """
        self.m_standing_textures = [
            (load_texture('textures/char/char_standing_up.png')),
            (load_texture('textures/char/char_standing_down.png')),
            (load_texture('textures/char/char_standing_left.png')),
            (load_texture('textures/char/char_standing_right.png'))
        ]
        self.m_moving_textures = [
            # Variant UP - INDEX 0
            ((
            load_texture('textures/char/char_moving_up_a.png'),
            load_texture('textures/char/char_moving_up_b.png'))),
            # Variant DOWN - INDEX 1
            ((
            load_texture('textures/char/char_moving_down_a.png'),
            pygame.image.load('textures/char/char_moving_down_b.png'))),
            # Variant Left - INDEX 2
            ((
            load_texture('textures/char/char_moving_left_a.png'),
            load_texture('textures/char/char_moving_left_b.png'))),
            # Variant Right - INDEX 3
            ((
            load_texture('textures/char/char_moving_right_a.png'),
            load_texture('textures/char/char_moving_right_b.png')))
        ]
        self.m_melee_attack_textures = [
            load_texture('textures/char/char_attack_melee_up.png'),
            load_texture('textures/char/char_attack_melee_down.png'),
            load_texture('textures/char/char_attack_melee_left.png'),
            load_texture('textures/char/char_attack_melee_right.png')
        ]
        self.image = load_texture('textures/char/char_standing_up.png')
        self.rect = self.image.get_rect()
        self.rect.x = data["x"]
        self.rect.y = data["y"]
        self.m_real_pos_x = data["x"]
        self.m_real_pos_y = data["y"]
        self.m_speed = data["speed"]
        self.m_movement = CMovement(self)
        self.m_attack_update_time = pygame.time.get_ticks()
        self.m_attacking = False
        self.m_closest_enemy = None
        self.m_attack_radius = 20
        # Stats
        self.m_damage = data["dmg"]
        self.m_hp = data["hp"]
        self.m_max_hp = self.m_hp
        self.m_dead = False

    def is_on_left_edge(self)->bool:
        """checks if the player is on the left edge of screen

        Returns:
            bool: Returns true if player pos x is lower than 149
        """
        return self.rect.x <= 149
    def is_on_right_edge(self)->bool:
        """checks if the player is on the right edge of screen

        Returns:
            bool: Returns true if player pos x is higher than 1031
        """
        return self.rect.x >= 1031
    def is_on_up_edge(self)->bool:
        """checks if the player is on the top edge of screen

        Returns:
            bool: Returns true if player pos y is lower than 160
        """
        return self.rect.y <= 160
    def is_on_down_edge(self)->bool:
        """checks if the player is on the bottom edge of screen

        Returns:
            bool: Returns true if player pos y is higher than 460
        """
        return self.rect.y >= 460
    def in_vicinity(self, item_rect, radius)->bool:
        """Check if player is in close range to an item with given radius

        Args:
            item_rect (pygame.Rect): pygame.Rect object of the other item
            radius (int): radius for the vicinity

        Returns:
            bool: Returns True if player is in the radius vicinity of the other object
        """
        return inside_circle(self.rect, item_rect, radius)
    def can_attack(self, item_rect, radius)->bool:
        """Checks if player can attack given item

        Args:
            item_rect (pygame.Rect): pygame.Rect object of the other item
            radius (int): radius for the item

        Returns:
            bool: Returs true if player can attack
        """
        distance = distance_of_two_points(self.rect, item_rect)
        return distance <= self.m_attack_radius + radius
    def render(self, screen)->None:
        """Draws player onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        # Draw Attack Radius of Player
        #pygame.draw.circle(screen, (255,0,0), (self.rect.x+self.rect.width/2, self.rect.y+self.rect.height/2), self.m_attack_radius, 1)
        # Draw Player
        screen.blit(self.image, self.rect)

    def attack(self)->None:
        """Represents attack of the player"""

        if not self.m_attacking:
            self.image = self.m_melee_attack_textures[self.m_movement.m_last_direction]
            self.m_attacking = True
            print(f"{self.m_closest_enemy}")
            if self.m_closest_enemy:
                if self.m_closest_enemy.m_dead:
                    self.m_closest_enemy = None
                else:
                    self.m_closest_enemy.get_damaged(self.m_damage)
                    print(f"Player attacked {self.m_closest_enemy.m_name}")
                    print(f"Enemy hp: {self.m_closest_enemy.m_hp}")

    def check_attack_cooldown(self)->None:
        """Sets cooldown for player's attack"""
        attack_cooldown = 1000
        pressed_keys = pygame.key.get_pressed()
        if pygame.time.get_ticks() - self.m_attack_update_time > attack_cooldown and self.m_attacking:
            self.m_attack_update_time = pygame.time.get_ticks()
            if not pressed_keys[pygame.K_q]:
                self.m_attacking = False
            self.image = self.m_standing_textures[self.m_movement.m_last_direction]

    def get_damage(self, dmg)->None:
        """deals damage to the player

        Args:
            dmg (int): damage that is to be dealt to the player
        """
        self.m_hp -= dmg
        if self.m_hp <= 0:
            self.m_dead = True

    def to_dict(self)->dict:
        """converts Cplayer into json dict format

        Returns:
            dict: Returns json dict format for the CPlayer
        """
        data = {
            "x": self.rect.x,
            "y": self.rect.y,
            "hp": self.m_hp,
            "dmg": self.m_damage,
            "speed": self.m_speed
        }
        return data
