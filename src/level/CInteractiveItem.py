"""Class representing interactive items on the screen"""
import pygame
from src.engine.tools import load_texture

class CInteractiveItem(pygame.sprite.Sprite):
    """Class representing interactive items on the screen

    Args:
        pygame (pygame.sprite.Sprite): Sprite object from pygame module
    """
    def __init__(self, x, y, action_name,radius, texture, data):
        """Constructor for CInteractiveItem

        Args:
            x (int): x pos
            y (int): y pos
            action_name (name): name
            radius (int): radius of interaction
            texture (int): texture name
            data (CLevel): Level that will be entered
        """
        pygame.sprite.Sprite.__init__(self)
        self.m_action_name = action_name
        self.m_radius = radius
        self.m_data = data

        # Set texture for interactive
        self.image = load_texture(texture)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.m_start_x = x
        self.m_start_y = y
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
    def render(self, screen)->None:
        """Renders the CInteractive item onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        #pygame.draw.rect(screen, (255,0,0), self.rect, 2)
        if not self.m_data.m_unlocked:
            self.image = load_texture("textures/interactives/locked_level.png")
        else:
            self.image = load_texture("textures/interactives/level.png")
        sprite = pygame.sprite.RenderPlain(self)
        sprite.update()
        sprite.draw(screen)
        #pygame.draw.circle(screen, (255,0,0), (self.rect.center), self.m_radius, 2)
        self.draw_data_name(screen)

    def draw_data_name(self,screen)->None:
        """Draws the levels name onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        text = self.m_data.m_name
        font = pygame.font.SysFont('Arial', 35)
        render_text = font.render(text, True, (0,0,0))
        render_text_rect = render_text.get_rect()
        render_text_rect.center = self.rect.center
        screen.blit(render_text, render_text_rect)

    def to_dict(self)->dict:
        """Converts CInteractiveItem object into json dict

        Returns:
            dict: json dict format
        """
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "action_name": self.m_action_name,
            "radius": self.m_radius,
            "start_x": self.m_start_x,
            "start_y": self.m_start_y
        }

    @classmethod
    def from_dict(cls, data):
        """Creates new instance of CInteractiveItem from json dict

        Args:
            data (dict): json dict representing CInteractiveItem

        Returns:
            CInteractiveItem: Returns new instance of CInteractiveItem from json dict
        """
        new_item = cls(data["x"], data["y"], data["action_name"], data["radius"], "textures/interactives/locked_level.png", None)
        new_item.m_start_x = data["start_x"]
        new_item.m_start_y = data["start_y"]
        return new_item
