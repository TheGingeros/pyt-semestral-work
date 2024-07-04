"""Class representing Main menu of the game"""
import pygame

class CMainMenu:
    """Class representing Main menu of the game"""
    def __init__(self, screen):
        """constructor for CMainMenu

        Args:
            screen (pygame.surface): pygame.surface object
        """
        self.rect = pygame.Rect(0,0, screen.get_width(), screen.get_height())
        self.m_options = [
            "New Game",
            "Load Save",
            "Quit"
        ]
        self.m_active_option = 0
        self.m_key_update_time = pygame.time.get_ticks()
        self.m_active = True

    def render(self, screen)->int:
        """renders the main menu onto the screen

        Args:
            screen (pygame.surface): pygame.surface object

        Returns:
            int: Returns an index based on the user input, more in CMainMenu.handle_key_input()
        """
        # Menu background
        pygame.draw.rect(screen, (255,255,255), self.rect)
        self.render_options(screen)
        return self.handle_key_input()



    def handle_key_input(self)->int:
        """Handles key input from the user

        Returns:
            int: Returns 1 for New Game, 2 for Load Save, 3 for Quit or 0 for no user input
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RETURN]:
            active_action = self.m_options[self.m_active_option]
            if active_action == "New Game":
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
        """Renders the options in the main menu

        Args:
            screen (pygame.surface): pygame.surface object
        """
        font = pygame.font.SysFont('Arial', 30)
        x = screen.get_width()/2
        y = 300

        for option in self.m_options:
            option_text = font.render(option, True, (0,0,0))
            rect = option_text.get_rect()
            rect.x = x - rect.width/2
            rect.y = y
            y += 40
            if option == self.m_options[self.m_active_option]:
                pygame.draw.rect(screen, (0,100,200), rect)
            screen.blit(option_text, rect)
