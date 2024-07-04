"""Class for handling CCollisions"""
from src.movement.CCollision import CCollision

class ColManager:
    """Class for handling CCollisions"""
    def __init__(self):
        """Constructor for ColManager
        """
        self.m_collisions = []

    def check_for_collisions(self, player)->int:
        """Handles if the player is near any CCollision object

        Args:
            player (CPlayer): Player Object

        Returns:
            int: Returns direction on which the player collides with the collision
        """
        flag = False
        col = -1
        for collision in self.m_collisions:
            temp_col = collision.collide_with(player)
            if temp_col != 4:
                #print(f"There is a col: {temp_col}")
                flag = True
                col = temp_col
                return col
            if temp_col == 4 and flag:
                #print(f"There isnt a col, but old one is left: {col}")
                return col
        return 4

    def to_dict(self)->dict:
        """Function for saving CColManager into json dict

        Returns:
            dict: json dict
        """
        return {
            "collision": [collision.to_dict() for collision in self.m_collisions]
        }

    @classmethod
    def from_dict(cls, data):
        """Creates CColManager instance from json dict

        Args:
            data (dict): Json Data for creating CColManager instance

        Returns:
            CColManager: Returns an instance of CColManager with attributes from the json dict file
        """
        new_manager = cls()
        new_manager.m_collisions = [CCollision.from_dict(col) for col in data["collision"]]
        return new_manager
