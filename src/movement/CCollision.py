"""Class for representing collisions in the game. Player object cant pass through them"""
class CCollision:
    """Class for representing collisions in the game. Player object cant pass through them"""
    def __init__(self, x, y, width, height):
        """Constructor for CCollision

        Args:
            x (int): x position
            y (int): y position
            width (int): width of collision
            height (int): height of collision
        """
        self.m_top = y
        self.m_bottom = y+height
        self.m_left = x
        self.m_right = x+width
        self.m_border = 20

    def check_top(self, player)->bool:
        """Function to check if player touches the top of the collision

        Args:
            player (CPlayer): Player object

        Returns:
            bool: True if player is on top of collision
        """
        return player.m_real_pos_y + self.m_border >= self.m_top and player.m_real_pos_y <= self.m_bottom and player.m_real_pos_x - self.m_border <= self.m_right and player.m_real_pos_x + self.m_border >= self.m_left
    def check_bottom(self, player)->bool:
        """Function to check if player touches the bottom of the collision

        Args:
            player (CPlayer): Player object

        Returns:
            bool: True if player is on bottom of collision
        """
        return player.m_real_pos_y - player.rect.height/2 <= self.m_bottom and player.m_real_pos_y >= self.m_top and player.m_real_pos_x - self.m_border <= self.m_right and player.m_real_pos_x + self.m_border >= self.m_left
    def check_left(self, player)->bool:
        """Function to check if player touches the left of the collision

        Args:
            player (CPlayer): Player object

        Returns:
            bool: True if player is on left of collision
        """
        return player.m_real_pos_x + player.rect.width/2 >=  self.m_left and player.m_real_pos_x <= self.m_right >= self.m_left and player.m_real_pos_y - self.m_border <= self.m_bottom and player.m_real_pos_y + self.m_border >= self.m_top
    def check_right(self, player)->bool:
        """Function to check if player touches the right of the collision

        Args:
            player (CPlayer): Player object

        Returns:
            bool: True if player is on right of collision
        """
        return player.m_real_pos_x - player.rect.width/2 <=  self.m_right and player.m_real_pos_x >= self.m_left >= self.m_left and player.m_real_pos_y - self.m_border <= self.m_bottom and player.m_real_pos_y + self.m_border >= self.m_top
    def collide_with(self, player)->int:
        """Function to check if player collides with the collision
        Args:
            player (CPlayer): Player object

        Returns:
            int: 0 if on top, 1 if on bottom, 2 if on the left, 3 if on the right, 4 otherwise
        """
        if self.check_top(player):
            return 0
        if self.check_bottom(player):
            return 1
        if self.check_left(player):
            return 2
        if self.check_right(player):
            return 3
        return 4

    def to_dict(self)->dict:
        """Function to convert CCollision to dictionary for json save

        Returns:
            dict: json format dictionary
        """
        return {
            "top": self.m_top,
            "bottom": self.m_bottom,
            "left": self.m_left,
            "right": self.m_right
        }

    @classmethod
    def from_dict(cls, data):
        """Function to create CCollision object from json dictionary

        Args:
            data (dict): data for creating the instance of CCollision

        Returns:
            CCollision: Returns instance of an CCollision
        """
        return cls(data["left"], data["top"], data["right"]-data["left"], data["bottom"]-data["top"])
