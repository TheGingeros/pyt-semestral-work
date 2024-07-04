"""Class representing HUD on the screen"""
import pygame
from src.level.CInteractiveItem import CInteractiveItem
from src.level.CLevel import CLevel
from src.menu.CDeadMenu import CDeadMenu
class CHud:
    """Class representing HUD on the screen
    """
    def __init__(self, screen, player):
        """Constructor for CHud

        Args:
            screen (pygame.surface): pygame.surface object
            player (CPlayer): CPlayer object
        """
        self.m_player = player
        self.m_interactive_items = []
        self.m_active_level = None
        self.m_active_level_index = 1
        self.m_new_rect = False
        self.m_dead_menu = CDeadMenu(screen)
    def render(self, screen)->None:
        """Renders HUD onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        self.render_player_coords(screen)
        self.render_current_location(screen)
        self.handle_interactions(screen)
        self.render_player_info(screen)
        #self.render_hud(screen)
    def render_player_coords(self, screen)->None:
        """Renders player coordinations onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        x = int(self.m_player.m_real_pos_x)
        y = int(self.m_player.m_real_pos_y)
        coords = f"X: {x} Y: {y}"
        font = pygame.font.SysFont('Arial', 30)
        coords_text = font.render(coords, True, (0,0,0))
        coords_text_rect = coords_text.get_rect()
        coords_text_rect.x = screen.get_width()/2 - coords_text_rect.width/2
        coords_text_rect.y = 0
        screen.blit(coords_text, coords_text_rect)
    def handle_interactions(self, screen)->None:
        """Function for handling interactions of items with the player

        Args:
            screen (pygame.surface): pygame.surface object
        """
        for item in self.m_interactive_items:
            if not self.m_active_level.m_index == 0 and len(self.m_active_level.m_enemies) == 0:
                item.m_data.m_unlocked = True
            if self.m_player.in_vicinity(item.rect, item.m_radius):
                #print("Inside Circle")
                self.render_action_label(item, screen)
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_f] and item.m_data.m_unlocked:
                    #print("Action - Enter Level")
                    self.m_active_level = item.m_data
                    if self.m_active_level.m_index == 0:
                        self.m_active_level_index += 1
                        print(self.m_active_level_index)
                    self.m_new_rect = True
                    self.m_interactive_items = self.m_active_level.m_interactive_items
                    self.m_active_level.set_data(self.m_player)
    def render_action_label(self, item, screen)->None:
        """Renders action label onto the screen

        Args:
            item (CLevel): renders the level action label onto the screen
            screen (pygame.surface): pygame.surface object
        """
        edited_label = f"[F] {item.m_action_name}"
        if isinstance(item.m_data, CLevel):
            if not item.m_data.m_unlocked:
                edited_label = "There are still some enemies left to be dealth with!"
                if item.m_data.m_name != "Base":
                    edited_label = "This level is not yet unlocked"
        font = pygame.font.SysFont('Arial', 30)
        render_label = font.render(edited_label, True, (0,0,0))
        render_label_rect = render_label.get_rect().copy()
        render_label_rect.x = screen.get_width()/2 - render_label_rect.width/2
        render_label_rect.y = screen.get_height() - render_label_rect.height - 60

        #print(f"X:{render_label_rect.x} Y: {render_label_rect.y}")

        screen.blit(render_label, render_label_rect)

    def render_current_location(self, screen)->None:
        """Renders the current location of the player onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        current_location = f"Current location: {self.m_active_level.m_name}"
        font = pygame.font.SysFont('Arial', 30)
        render_label = font.render(current_location, True, (0,0,0))
        render_label_rect = render_label.get_rect()
        render_label_rect.x = 17
        render_label_rect.y = 17
        screen.blit(render_label, render_label_rect)

    def render_player_info(self, screen)->None:
        """Renders player hp, dmg and speed onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        player_info = f"HP: {self.m_player.m_hp}/100    Damage: {self.m_player.m_damage}    Speed: {self.m_player.m_speed}"
        font = pygame.font.SysFont('Arial', 30)
        render_info = font.render(player_info, True, (0,0,0))
        render_info_rect = render_info.get_rect()
        render_info_rect.x = render_info_rect.x = screen.get_width()/2 - render_info_rect.width/2
        render_info_rect.y = screen.get_height() - render_info_rect.height - 20
        padding = 10
        background_rect = pygame.Rect(render_info_rect.x - padding, render_info_rect.y - padding, render_info_rect.width + padding*1.5,  render_info_rect.height + padding*1.5)
        pygame.draw.rect(screen, (0,100,200), background_rect)
        screen.blit(render_info, render_info_rect)
