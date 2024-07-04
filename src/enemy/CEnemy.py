"""
Class representing the enemies in the game
"""
import random
import pygame
from src.enemy.CProjectile import CProjectile
from src.engine.tools import inside_circle

class CEnemy:
    """Class representing the enemies in the game"""
    def __init__(self, pos_x, pos_y, hp, dmg, attack_cooldown, texture_subname, player, radius, speed, reach_x, reach_y):
        """Constructor for CEnemy

        Args:
            pos_x (int): x pos
            pos_y (int): y pos
            hp (int): health points
            dmg (int): damage
            attack_cooldown (int): cooldown for attack, in ms
            texture_subname (string): name
            player (CPlayer): CPlayer object
            radius (int): radius for attack
            speed (int): speed
            reach_x (int): max x reach for enemy movement
            reach_y (int): max y reach for enemy movement
        """
        self.rect = pygame.Rect(pos_x, pos_y, 60,60)
        self.rect.center = (pos_x+reach_x/2, pos_y+reach_y/2)
        self.m_hp = hp
        self.m_max_hp = hp
        self.m_damage = dmg
        self.m_attack_cooldown = attack_cooldown
        self.m_start_attack_cooldown = 1000
        self.m_attack_start = False
        self.m_name = texture_subname
        self.m_attack_update_time = pygame.time.get_ticks()
        self.m_start_attack_update_time = pygame.time.get_ticks()
        self.m_attack_animation_update_time = pygame.time.get_ticks()
        self.m_player = player
        self.m_animating = False
        self.m_shooting = False
        self.m_dead = False
        self.m_attack_radius = radius
        self.m_speed = speed
        self.m_moving = False
        self.m_movement_update_time = pygame.time.get_ticks()
        self.m_move_update_time = pygame.time.get_ticks()
        self.m_center_x = self.rect.center[0]
        self.m_center_y = self.rect.center[1]
        self.m_destination = [0,0]
        self.m_reach_x = reach_x
        self.m_reach_y = reach_y
        self.m_start_x = pos_x+reach_x/2
        self.m_start_y = pos_y+reach_y/2
        self.m_attack_modes = [
            "melee",
            "ranged"
        ]
        self.m_projectiles = []
        self.m_attack_mode = ""
    def render(self, screen)-> None:
        """Function to render CEnemy

        Args:
            screen (pygame.surface): pygame surface object
        """
        pygame.draw.rect(screen,(0,255,0), self.rect)
        self.draw_health_bar(screen)
        if self.m_animating:
            pygame.draw.circle(screen, (255,0,0), (self.rect.center[0], self.rect.center[1]), 30)
        if self.m_shooting:
            self.m_projectiles.append(CProjectile(self.rect.center[0], self.rect.center[1], 4, self.m_damage))
            self.m_projectiles.append(CProjectile(self.rect.center[0], self.rect.center[1], 4, self.m_damage))
            self.m_projectiles.append(CProjectile(self.rect.center[0], self.rect.center[1], 4, self.m_damage))
            self.m_projectiles.append(CProjectile(self.rect.center[0], self.rect.center[1], 4, self.m_damage))
            self.m_shooting = False
        else:
            pygame.draw.circle(screen, (255,0,0), (self.rect.center[0], self.rect.center[1]), 30, 1)

        for projectile in self.m_projectiles:
            if self.m_player.in_vicinity(projectile.rect, 20):
                self.m_player.get_damage(projectile.m_dmg)
                self.m_projectiles.remove(projectile)
            if projectile.reached_distance():
                self.m_projectiles.remove(projectile)
            else:
                #print(projectile.m_direction)
                projectile.move()
                projectile.render(screen)
        # Draw interaction radius of Enemy
        pygame.draw.circle(screen, (0,255,0), (self.rect.center[0], self.rect.center[1]), 100, 1)

    def player_in_vicinity(self, player)->bool:
        """Function to check if player object is inside our attack radius

        Args:
            player (CPlayer): CPlayer object

        Returns:
            bool: True if player is inside attack radius
        """
        return inside_circle(self.rect, player.rect, 100)

    def attack(self)->None:
        """Function that represents start of attack
        """
        if pygame.time.get_ticks() - self.m_attack_update_time > self.m_attack_cooldown:
            self.m_attack_mode = self.m_attack_modes[random.randint(0,1)]
            print(self.m_attack_mode)
            if self.m_attack_mode == "ranged":
                self.m_shooting = True
            self.m_attack_update_time = pygame.time.get_ticks()
            self.m_attack_start = True
            self.m_start_attack_update_time = pygame.time.get_ticks()

    def attack_check(self)-> None:
        """Checks if its time to attack
        """
        animation_cooldown = 750
        if not self.m_shooting and not self.m_animating and self.m_attack_start and pygame.time.get_ticks() - self.m_start_attack_update_time > self.m_start_attack_cooldown:
            self.m_attack_animation_update_time = pygame.time.get_ticks()
            if self.m_attack_mode == "melee":
                self.m_animating = True
            if self.player_in_vicinity(self.m_player) and self.m_attack_mode == "melee":
                self.m_player.get_damage(self.m_damage)
        if self.m_animating and pygame.time.get_ticks() - self.m_attack_animation_update_time > animation_cooldown:
            #print("Animation done")
            self.m_attack_animation_update_time = pygame.time.get_ticks()
            self.m_animating = False
            self.m_shooting = False
            self.m_attack_start = False

    def get_damaged(self,dmg)->None:
        """Function to deal damage to enemy

        Args:
            dmg (int): damage that should be dealt to enemy
        """
        self.m_hp -= dmg
        #print(f"{self.m_hp/self.m_max_hp}")
        if self.m_hp <= 0:
            self.m_dead = True

    def generate_random_destination(self)->None:
        """Generates random destination for the enemy to reach
        """
        x = random.randint(self.m_center_x - self.m_reach_x//2, self.m_center_x + self.m_reach_x//2 - self.rect.width)
        y = random.randint(self.m_center_y - self.m_reach_y//2, self.m_center_y + self.m_reach_y//2 - self.rect.height)
        self.m_destination[0] = x
        self.m_destination[1] = y
        #print(f"Destination - X:{self.m_destination[0]} Y:{self.m_destination[1]}")
    def reach_destination(self)->None:
        """Moves the enemy in the generated destination
        """
        move_x = self.m_speed
        move_y = self.m_speed
        if self.m_destination[0] < self.m_center_x:
            move_x *= -1
        if self.m_destination[1] < self.m_center_y:
            move_y *= -1

        move_cooldown = 25
        if pygame.time.get_ticks() - self.m_move_update_time > move_cooldown:
            #print(f"{self.m_name} - X:{self.rect.x} Y:")
            if (move_x < 0 and self.rect.x >= self.m_destination[0]) or (move_x > 0 and self.rect.x <= self.m_destination[0]):
                self.rect.x += move_x
            elif (move_y < 0 and self.rect.y >= self.m_destination[1]) or (move_y > 0 and self.rect.y <= self.m_destination[1]):
                self.rect.y += move_y
            else:
                #print(f"{self.m_name} has reach its destination")
                self.m_moving = False
            self.m_move_update_time = pygame.time.get_ticks()
    def movement(self)->None:
        """Represents the movement for enemy
        """
        if self.m_moving:
            self.reach_destination()
        #move_distance = 150
        movement_cooldown = random.randint(1500, 3000)
        if not self.m_moving and pygame.time.get_ticks() - self.m_movement_update_time > movement_cooldown:
            self.generate_random_destination()
            self.m_moving = True
            self.m_movement_update_time = pygame.time.get_ticks()

    def draw_health_bar(self, screen)->None:
        """Draws the health bar of enemy onto the screen

        Args:
            screen (pygame.surface): pygame surface object
        """
        back_rect = pygame.Rect(self.rect.x-2, self.rect.y-27, 64, 14)
        rect = pygame.Rect(self.rect.x, self.rect.y-25, 60, 10)
        scale = self.m_hp/self.m_max_hp
        rect.scale_by_ip(scale, 1)
        rect.x = self.rect.x
        pygame.draw.rect(screen,(0,0,0), back_rect)
        pygame.draw.rect(screen,(255,0,0), rect)

    def to_dict(self)->dict:
        """Function to convert CEnemy into json dict

        Returns:
            dict: represents CEnemy as json dict
        """
        return {
            "x": self.rect.center[0],
            "y": self.rect.center[1],
            "hp": self.m_hp,
            "dmg": self.m_damage,
            "attack_cooldown": self.m_attack_cooldown,
            "texture_subname": self.m_name,
            "radius": self.m_attack_radius,
            "speed": self.m_speed,
            "reach_x": self.m_reach_x,
            "reach_y": self.m_reach_y,
            "start_x": self.m_start_x,
            "start_y": self.m_start_y,
            "projectiles": [projectile.to_dict() for projectile in self.m_projectiles]
        }

    @classmethod
    def from_dict(cls, data, player):
        """Function to create instance of CEnemy from json dict

        Args:
            data (dict): json data for CEnemy
            player (CPlayer): CPlayer object

        Returns:
            CEnemy: Returns new instance of CEnemy
        """
        new_enemy = cls(0,0, data["hp"], data["dmg"], data["attack_cooldown"], data["texture_subname"], player, data["radius"], data["speed"], data["reach_x"], data["reach_y"])
        new_enemy.rect.center = (data["x"], data["y"])
        new_enemy.m_start_x = data["start_x"]
        new_enemy.m_start_y = data["start_y"]
        new_enemy.m_projectiles = [CProjectile.from_dict(projectile) for projectile in data["projectiles"]]
        return new_enemy
