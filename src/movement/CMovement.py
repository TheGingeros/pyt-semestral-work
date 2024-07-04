"""Class representing the default movement in the game"""

class CMovement:
    """Class representing the default movement in the game"""
    def __init__(self, player):
        """constructor for CMovement

        Args:
            player (CPlayer): player with the movement
        """
        self.m_tick_count = 0
        self.m_moving_index = 0
        self.m_moving_up = False
        self.m_moving_down = False
        self.m_moving_left = False
        self.m_moving_right = False
        self.m_last_direction = 0
        self.m_player = player

    def moving_up(self, move_player)->None:
        """Represents movement of player up

        Args:
            move_player (bool): True if the player should be animated
        """
        self.m_last_direction = 0
        if self.m_moving_up:
            self.animated_movement(0)
        else:
            self.m_player.image = self.m_player.m_standing_textures[0]
            self.flags_up()
        if move_player:
            self.m_player.rect.y -= self.m_player.m_speed

        self.m_player.m_real_pos_y -= self.m_player.m_speed

    def moving_down(self, move_player)->None:
        """Represents movement of player down

        Args:
            move_player (bool): True if the player should be animated
        """
        self.m_last_direction = 1
        if self.m_moving_down:
            self.animated_movement(1)
        else:
            self.m_player.image = self.m_player.m_standing_textures[1]
            self.flags_down()
        if move_player:
            self.m_player.rect.y += self.m_player.m_speed

        self.m_player.m_real_pos_y += self.m_player.m_speed

    def moving_left(self, move_player)->None:
        """Represents movement of player left

        Args:
            move_player (bool): True if the player should be animated
        """
        self.m_last_direction = 2
        if self.m_moving_left:
            self.animated_movement(2)
        else:
            self.m_player.image = self.m_player.m_standing_textures[2]
            self.flags_left()
        if move_player:
            self.m_player.rect.x -= self.m_player.m_speed

        self.m_player.m_real_pos_x -= self.m_player.m_speed

    def moving_right(self, move_player)->None:
        """Represents movement of player right

        Args:
            move_player (bool): True if the player should be animated
        """
        self.m_last_direction = 3
        if self.m_moving_right:
            self.animated_movement(3)
        else:
            self.m_player.image = self.m_player.m_standing_textures[3]
            self.flags_right()
        if move_player:
            self.m_player.rect.x += self.m_player.m_speed

        self.m_player.m_real_pos_x += self.m_player.m_speed

    def animated_movement(self, direction_index)->None:
        """Represents the basic animation of movement for the player

        Args:
            direction_index (int): Describes the direction and based on that the right texture is set
        """
        self.m_tick_count +=1
        if self.m_tick_count % 25 == 0:
            if direction_index == 0:
                self.m_player.image = self.m_player.m_moving_textures[0][self.m_moving_index % 2]
                self.m_moving_index +=1
            if direction_index == 1:
                self.m_player.image = self.m_player.m_moving_textures[1][self.m_moving_index % 2]
                self.m_moving_index +=1
            self.m_tick_count = 0
            if direction_index == 2:
                self.m_player.image = self.m_player.m_moving_textures[2][self.m_moving_index % 2]
                self.m_moving_index +=1
            self.m_tick_count = 0
            if direction_index == 3:
                self.m_player.image = self.m_player.m_moving_textures[3][self.m_moving_index % 2]
                self.m_moving_index +=1
            self.m_tick_count = 0

    def flags_up(self)->None:
        """Sets flags for moving up
        """
        self.m_moving_up = True
        self.m_moving_down = False
        self.m_moving_left = False
        self.m_moving_right = False

    def flags_down(self)->None:
        """Sets flags for moving down
        """
        self.m_moving_up = False
        self.m_moving_down = True
        self.m_moving_left = False
        self.m_moving_right = False

    def flags_left(self)->None:
        """Sets flags for moving left
        """
        self.m_moving_up = False
        self.m_moving_down = False
        self.m_moving_left = True
        self.m_moving_right = False

    def flags_right(self)->None:
        """Sets flags for moving right
        """
        self.m_moving_up = False
        self.m_moving_down = False
        self.m_moving_left = False
        self.m_moving_right = True
