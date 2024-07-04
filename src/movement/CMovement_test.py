# test_cmovement.py

import pytest
from src.movement.CMovement import CMovement
class MockPlayer:
    """Mock class for CPlayer to use in tests"""
    def __init__(self):
        self.m_real_pos_x = 100
        self.m_real_pos_y = 100
        self.rect = MockRect(50, 50)
        self.m_speed = 10
        self.image = None
        self.m_standing_textures = ["up_standing", "down_standing", "left_standing", "right_standing"]
        self.m_moving_textures = [
            ["up_moving_1", "up_moving_2"],
            ["down_moving_1", "down_moving_2"],
            ["left_moving_1", "left_moving_2"],
            ["right_moving_1", "right_moving_2"]
        ]

class MockRect:
    """Mock class for Rect to use in tests"""
    def __init__(self, width, height):
        self.x = 100
        self.y = 100
        self.width = width
        self.height = height

@pytest.fixture
def player():
    return MockPlayer()

@pytest.fixture
def movement(player):
    return CMovement(player)

def test_moving_up(movement, player):
    movement.moving_up(True)
    assert player.m_real_pos_y == 90
    assert player.rect.y == 90
    assert player.image == "up_standing"
    assert movement.m_last_direction == 0
    assert movement.m_moving_up is True

def test_moving_down(movement, player):
    movement.moving_down(True)
    assert player.m_real_pos_y == 110
    assert player.rect.y == 110
    assert player.image == "down_standing"
    assert movement.m_last_direction == 1
    assert movement.m_moving_down is True

def test_moving_left(movement, player):
    movement.moving_left(True)
    assert player.m_real_pos_x == 90
    assert player.rect.x == 90
    assert player.image == "left_standing"
    assert movement.m_last_direction == 2
    assert movement.m_moving_left is True

def test_moving_right(movement, player):
    movement.moving_right(True)
    assert player.m_real_pos_x == 110
    assert player.rect.x == 110
    assert player.image == "right_standing"
    assert movement.m_last_direction == 3
    assert movement.m_moving_right is True

def test_flags_up(movement):
    movement.flags_up()
    assert movement.m_moving_up is True
    assert movement.m_moving_down is False
    assert movement.m_moving_left is False
    assert movement.m_moving_right is False

def test_flags_down(movement):
    movement.flags_down()
    assert movement.m_moving_up is False
    assert movement.m_moving_down is True
    assert movement.m_moving_left is False
    assert movement.m_moving_right is False

def test_flags_left(movement):
    movement.flags_left()
    assert movement.m_moving_up is False
    assert movement.m_moving_down is False
    assert movement.m_moving_left is True
    assert movement.m_moving_right is False

def test_flags_right(movement):
    movement.flags_right()
    assert movement.m_moving_up is False
    assert movement.m_moving_down is False
    assert movement.m_moving_left is False
    assert movement.m_moving_right is True
