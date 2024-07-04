"""Class representing a projectile shot by the CEnemy"""
import random
import pygame

class CProjectile:
    """Class representing a projectile shot by the CEnemy"""
    def __init__(self, x, y, speed, dmg):
        """constructor for CProjectile

        Args:
            x (int): x pos
            y (int): y pos
            speed (int): speed
            dmg (int): damage
        """
        rect = pygame.Rect(x, y, 10, 10)
        self.rect = rect
        self.rect.center = (x, y)
        self.m_speed = speed
        self.m_dmg = dmg
        self.m_distance = 300
        self.m_distance_done = 0
        self.m_direction = self.calculate_direction()

    def reached_distance(self)->bool:
        """Cheks if projectile reached its destination

        Returns:
            bool: True if projectile reached its distance
        """
        return self.m_distance_done >= self.m_distance

    def calculate_direction(self)->int:
        """calculates the direction for the projectile using random module

        Returns:
            int: Retuns 0 for up movement, 1 for down movement, 2 for left and 3 for right
        """
        x = random.randint(0,3)
        #print(f"X: {x}")
        if x == 0:
            return "up"
        if x == 1:
            return "down"
        if x == 2:
            return "left"
        if x == 3:
            return "right"
        return 4

    def move(self)->None:
        """Moves the projectile in its direction by its speed
        """
        self.m_distance_done += 1
        if self.m_direction == "up":
            self.rect.y -= self.m_speed
        if self.m_direction == "down":
            self.rect.y += self.m_speed
        if self.m_direction == "left":
            self.rect.x -= self.m_speed
        if self.m_direction == "right":
            self.rect.x += self.m_speed

    def render(self, screen)->None:
        """draws the projectile onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        pygame.draw.rect(screen, (255,0,0), self.rect)

    def to_dict(self)->dict:
        """converts CProjectile instance into json dict format

        Returns:
            dict: Returns json dict format for CProjectile instance
        """
        return {
            "x": self.rect.center[0],
            "y": self.rect.center[1],
            "speed": self.m_speed,
            "dmg": self.m_dmg,
            "distance_done": self.m_distance_done,
            "direction": self.m_direction
        }
    @classmethod
    def from_dict(cls, data):
        """Creates an instance of CProjectile from json dict format

        Args:
            data (dict): json dict format for CProjectile

        Returns:
            CProjectile: Returns an instance of CProjectile from json dict format
        """
        new_projectile = cls(data["x"], data["y"], data["speed"], data["dmg"])
        new_projectile.m_distance_done = data["distance_done"]
        new_projectile.m_direction = data["direction"]
        return new_projectile
