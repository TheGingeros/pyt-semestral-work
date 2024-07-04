"""Class representing menu that is shown after the player dies"""
import pygame

class CDeadMenu:
    """Class representing menu that is shown after the player dies
    """
    def __init__(self, screen):
        """Constructor for CDeadMenu

        Args:
            screen (pygame.surface): pygame surface object
        """
        self.rect = pygame.Rect(0,0, screen.get_width(), screen.get_height())
        self.m_options = [
            "Play Again",
            "Load Save",
            "Quit"
        ]
        self.m_active_option = 0
        self.m_key_update_time = pygame.time.get_ticks()

    def render(self, screen)->int:
        """Function for rendering CDeadMenu

        Args:
            screen (pygame.surface): pygame surface object

        Returns:
            int: Returns index that returs CDeadMenu.handle_key_input()
        """
        # Menu background
        pygame.draw.rect(screen, (255,255,255), self.rect)
        self.render_options(screen)
        return self.handle_key_input()



    def handle_key_input(self)->int:
        """Function for handling input from user

        Returns:
            int: Returns 1 for Play Again, 2 for Load Save, 3 for Quit and 0 if user haven't pressed anything
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RETURN]:
            active_action = self.m_options[self.m_active_option]
            if active_action == "Play Again":
                return 1
            if active_action == "Load Save":
                return 2
            if active_action == "Quit":
                return 3
        if pressed_keys[pygame.K_UP]:
            if self.m_active_option != 0 and pygame.time.get_ticks() - self.m_key_update_time > 100:
                self.m_key_update_time = pygame.time.get_ticks()
                self.m_active_option -= 1
        if pressed_keys[pygame.K_DOWN]:
            if self.m_active_option != len(self.m_options)-1 and pygame.time.get_ticks() - self.m_key_update_time > 100:
                self.m_key_update_time = pygame.time.get_ticks()
                self.m_active_option += 1
        return 0

    def render_options(self, screen)->None:
        """Function for rendering options that the user can interact

        Args:
            screen (pygame.surface): pygame surface object
        """
        font = pygame.font.SysFont('Arial', 30)
        font1 = pygame.font.SysFont('Arial', 60)
        x = screen.get_width()/2
        y = 300
        text = "You Died!"
        text_render = font1.render(text, True, (0,0,0))
        text_render_rect = text_render.get_rect()
        text_render_rect.x = x - text_render_rect.width/2
        text_render_rect.y = 100
        screen.blit(text_render, text_render_rect)

        for option in self.m_options:
            option_text = font.render(option, True, (0,0,0))
            rect = option_text.get_rect()
            rect.x = x - rect.width/2
            rect.y = y
            y += 40
            if option == self.m_options[self.m_active_option]:
                pygame.draw.rect(screen, (0,100,200), rect)
            screen.blit(option_text, rect)
