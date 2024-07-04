"""Class for representing the game application object"""
import json
import os
import pygame
from src.game.CPlayer import CPlayer
from src.game.CMap import CMap
from src.menu.CHud import CHud
from src.menu.CMainMenu import CMainMenu

class CApp:
    """Class for representing the game application object"""
    def __init__(self, width, height):
        """constructor for CApp

        Args:
            width (int): width for the screen
            height (int): height for the screen
        """
        pygame.init()
        self.m_width = width
        self.m_height = height
        self.m_screen = pygame.display.set_mode((self.m_width, self.m_height))
        self.m_clock = pygame.time.Clock()
        self.m_running = False
        self.m_background = ()
        with open("config/save/player_data.json","r") as player_file:
            player_data = json.load(player_file)
        self.m_player = CPlayer(player_data)
        self.m_player.m_hp = player_data["hp"]
        self.m_player.m_damage = player_data["dmg"]
        self.m_player.m_speed = player_data["speed"]
        self.m_hud = CHud(self.m_screen, self.m_player)
        with open("config/save/map_data.json","r") as map_file:
            map_data = json.load(map_file)
        self.m_map = CMap(self.m_player, self.m_hud, map_data)

        # Things to render - MUST BE IN RIGHT ORDER
        self.m_render_list = [
            self.m_map,
            self.m_player,
            self.m_hud
        ]
        self.m_main_menu = CMainMenu(self.m_screen)

    def launch(self)->None:
        """Starts the application
        """
        if self.m_running:
            print("App is already running!")
            return

        pygame.display.set_caption('School Adventures of Mr. Fiala')

        # Setup background
        self.m_background = pygame.Surface(self.m_screen.get_size())
        self.m_background = self.m_background.convert()
        self.m_background.fill((255, 255, 255))
        self.m_screen.blit(self.m_background, (0,0))

        # Start the game loop
        self.m_running = True
        self.run()

    def run(self)->None:
        """Runs the application
        """
        if not self.m_running:
            print("App is not running.")

        while self.m_running:
            self.m_clock.tick(30)
            #print(pygame.display.get_caption())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.m_running = False
            if self.m_main_menu.m_active:
                action = self.m_main_menu.render(self.m_screen)
                if action == 1:
                    self.new_game()
                    self.m_main_menu.m_active = False
                if action == 2:
                    self.load_game()
                    self.m_main_menu.m_active = False
                if action == 3:
                    self.m_running = False
            elif self.m_player.m_dead:
                action = self.m_hud.m_dead_menu.render(self.m_screen)
                if action == 1:
                    self.new_game()
                if action == 2:
                    self.load_game()
                if action == 3:
                    self.m_running = False
            else:
                self.m_map.movement()
                self.render()

            self.refresh()

        self.save()
        pygame.quit()

    def refresh(self)->None:
        """Refreshes the screen
        """
        pygame.display.update()

    def render(self)->None:
        """renders everything from the app onto the screen
        """
        self.m_screen.blit(self.m_background, (0,0))
        for item in self.m_render_list:
            item.render(self.m_screen)

    def save(self)->None:
        """saves player and map data into json format
        """
        player_data = self.m_player.to_dict()
        with open('config/save/player_data.json', 'w') as player_file:
            json.dump(player_data, player_file)
        map_data = self.m_map.to_dict()
        with open('config/save/map_data.json', 'w') as map_file:
            json.dump(map_data, map_file)

    def new_game(self)->None:
        """sets up new game
        """
        with open("config/new_player_data.json","r") as player_file:
            player_data = json.load(player_file)
        self.m_player = CPlayer(player_data)
        self.m_hud = CHud(self.m_screen, self.m_player)
        with open("config/new_map_data.json","r") as map_file:
            map_data = json.load(map_file)
        self.m_map = CMap(self.m_player, self.m_hud, map_data)
        self.m_render_list = [
            self.m_map,
            self.m_player,
            self.m_hud
        ]
    def load_game(self)->None:
        """loads new game from saved json files
        """
        load_path = "config/save/map_data.json"
        if os.path.exists(load_path):
            print("Load Game")
            with open("config/save/player_data.json","r") as player_file:
                player_data = json.load(player_file)
            self.m_player = CPlayer(player_data)
            self.m_hud = CHud(self.m_screen, self.m_player)
            with open("config/save/map_data.json","r") as map_file:
                map_data = json.load(map_file)
            self.m_map = CMap(self.m_player, self.m_hud, map_data)
            self.m_render_list = [
                self.m_map,
                self.m_player,
                self.m_hud
            ]
        else:
            self.new_game()
