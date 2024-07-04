"""Class representing a trap in the game"""
import random
import pygame
from src.engine.tools import load_texture

class CTrap:
    """Class representing a trap in the game"""
    def __init__(self, x, y, animating):
        """constructor for CTrap

        Args:
            x (int): x pos
            y (int): y pos
            animating (bool): True if the trap should be animated
        """
        self.m_textures = [
            "textures/traps/spikes_down.png",
            "textures/traps/spikes_up.png"
        ]
        self.image = load_texture(self.m_textures[1])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.m_start_x = x
        self.m_start_y = y
        self.m_update_time = pygame.time.get_ticks()
        self.m_spikes_up = not animating
        self.m_animating = animating
        self.m_cooldown = 1500 + random.randint(500, 1000)
        self.m_attack_update_time = pygame.time.get_ticks()

    def render(self, screen)->None:
        """draws the trap onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        if self.m_animating:
            if self.m_spikes_up:
                self.image = load_texture(self.m_textures[1])
            else:
                self.image = load_texture(self.m_textures[0])
        screen.blit(self.image, self.rect)

    def animate(self)->None:
        """represents basic animation for the trap
        """
        if pygame.time.get_ticks() - self.m_update_time > self.m_cooldown:
            self.m_update_time = pygame.time.get_ticks()
            if self.m_spikes_up:
                self.m_spikes_up = False
            else:
                self.m_spikes_up = True
    def player_on_trap(self, player)->None:
        """checks if the player is on the trap, if yes, it deals dmg

        Args:
            player (CPlayer): CPlayer object
        """
        player_x = player.rect.center[0]
        player_y = player.rect.center[1]
        cooldown = 2000
        flag = player_x > self.rect.x and player_x < self.rect.x + self.rect.width and player_y > self.rect.y and player_y < self.rect.y + self.rect.height and self.m_spikes_up
        if flag and pygame.time.get_ticks() -  self.m_attack_update_time > cooldown:
            self.m_attack_update_time = pygame.time.get_ticks()
            player.get_damage(30)
            print(f"Player got damaged by trap: {player.m_hp}")

    def to_dict(self)->dict:
        """converts CTrap instance into json dict format

        Returns:
            dict: Returns json dict format for CTrap instance
        """
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "animating": self.m_animating,
            "start_x": self.m_start_x,
            "start_y": self.m_start_y
        }
    @classmethod
    def from_dict(cls, data):
        """converts json dict format into CTrap instance

        Args:
            data (dict): json dict format for CTrap

        Returns:
            CTrap: Returns CTrap instance from json dict format
        """
        new_trap = cls(data["x"], data["y"], data["animating"])
        new_trap.m_start_x = data["start_x"]
        new_trap.m_start_y = data["start_y"]
        return new_trap
