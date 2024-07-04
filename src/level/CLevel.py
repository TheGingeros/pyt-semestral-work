"""Class representing level in the game"""
from src.movement.CColManager import ColManager
from src.enemy.CTrap import CTrap
from src.enemy.CEnemy import CEnemy
from src.level.CInteractiveItem import CInteractiveItem

class CLevel:
    """Class representing level in the game
    """
    def __init__(self, texture, name, player_start_x, player_start_y, player, index):
        """Constructor for CLevel

        Args:
            texture (string): texture name
            name (string): name of the level
            player_start_x (int): x pos for player to spawn
            player_start_y (int): y pos for player to spawn
            player (CPlayer): CPLayer object
            index (int): index number for the level
        """
        self.m_texture = texture
        self.m_name = name
        self.m_enemies = []
        self.m_interactive_items = []
        self.m_traps = []
        self.m_player_start_x = player_start_x
        self.m_player_start_y = player_start_y
        self.m_unlocked = False
        self.m_collision_manager = ColManager()
        self.m_player = player
        self.m_index = index

    def add_enemy(self, enemy)->None:
        """add enemy into the list of enemies

        Args:
            enemy (CEnemy): CEnemy object
        """
        self.m_enemies.append(enemy)

    def add_interactive(self, item)->None:
        """add interactive item into the list of items

        Args:
            item (CInteractiveItem): CInteractiveItem object
        """
        self.m_interactive_items.append(item)

    def add_collision(self, collision)->None:
        """add collison into the list of col manager

        Args:
            collision (CCollision): collision object
        """
        self.m_collision_manager.m_collisions.append(collision)

    def add_trap(self, trap)->None:
        """add trap into the list of traps

        Args:
            trap (CTrap): CTrap object
        """
        self.m_traps.append(trap)
    def render(self, screen)->None:
        """Renders everything from the CLevel onto the screen

        Args:
            screen (pygame.surface): pygame.surface object
        """
        # Render Enemies
        for enemy in self.m_enemies:
            if enemy.m_dead:
                self.m_enemies.remove(enemy)
            enemy.movement()
            enemy.attack_check()
            if enemy.player_in_vicinity(self.m_player):
                enemy.attack()
                if self.m_player.can_attack(enemy.rect, enemy.m_attack_radius):
                    self.m_player.m_closest_enemy = enemy
                    #print(self.m_player.m_closest_enemy.m_name)
                elif enemy == self.m_player.m_closest_enemy:
                    self.m_player.m_closest_enemy = None
            enemy.render(screen)

        # Render Interactive items
        for item in self.m_interactive_items:
            item.render(screen)

        for trap in self.m_traps:
            trap.player_on_trap(self.m_player)
            if trap.m_animating:
                trap.animate()
            trap.render(screen)

    def set_data(self, player)->None:
        """Sets needed data for the new level

        Args:
            player (CPlayer): player object
        """
        player.rect.center = (self.m_player_start_x, self.m_player_start_y)
        player.m_real_pos_x = self.m_player_start_x
        player.m_real_pos_y = self.m_player_start_y
        for enemy in self.m_enemies:
            enemy.rect.center = (enemy.m_start_x, enemy.m_start_y)
            enemy.m_center_x = enemy.rect.center[0]
            enemy.m_center_y = enemy.rect.center[1]
        for item in self.m_interactive_items:
            item.rect.x = item.m_start_x
            item.rect.y = item.m_start_y
        for trap in self.m_traps:
            trap.rect.x = trap.m_start_x
            trap.rect.y = trap.m_start_y
    def to_dict(self)->dict:
        """Converts CLevel into json dict format

        Returns:
            dict: json dict format for CLevel
        """
        return {
            "texture": self.m_texture,
            "name": self.m_name,
            "player_start_x": self.m_player_start_x,
            "player_start_y": self.m_player_start_y,
            "index": self.m_index,
            "enemies": [enemy.to_dict() for enemy in self.m_enemies],
            "items": [item.to_dict() for item in self.m_interactive_items],
            "traps": [trap.to_dict() for trap in self.m_traps],
            "unlocked": self.m_unlocked,
            "colmanager": self.m_collision_manager.to_dict(),
        }

    @classmethod
    def from_dict(cls, data, player):
        """Creates an instance of CLevel from json file

        Args:
            data (dict): json data
            player (CPlayer): CPlayer object

        Returns:
            CLevel: Returns an instance of CLevel from json file
        """
        new_level = cls(data["texture"], data["name"], data["player_start_x"], data["player_start_y"], player, data["index"])
        new_level.m_enemies = [CEnemy.from_dict(enemy, player) for enemy in data["enemies"]]
        new_level.m_interactive_items = [CInteractiveItem.from_dict(item) for item in data["items"]]
        new_level.m_traps = [CTrap.from_dict(trap) for trap in data["traps"]]
        new_level.m_unlocked = data["unlocked"]
        new_level.m_collision_manager = ColManager.from_dict(data["colmanager"])
        return new_level
