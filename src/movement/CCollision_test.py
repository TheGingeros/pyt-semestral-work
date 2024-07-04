# test_ccollision.py

import pytest
from src.movement.CCollision import CCollision

class MockPlayer:
    """Mock class for CPlayer to use in tests"""
    def __init__(self, x, y, width, height):
        self.m_real_pos_x = x
        self.m_real_pos_y = y
        self.rect = MockRect(width, height)

class MockRect:
    """Mock class for Rect to use in tests"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

@pytest.fixture
def collision():
    return CCollision(50, 50, 100, 100)

def test_check_top(collision):
    player = MockPlayer(100, 40, 50, 50)
    assert collision.check_top(player) is True

def test_check_top_false(collision):
    player = MockPlayer(100, 20, 50, 50)
    assert collision.check_top(player) is False

def test_check_bottom_false(collision):
    player = MockPlayer(100, 200, 50, 50)
    assert collision.check_bottom(player) is False

def test_check_left(collision):
    player = MockPlayer(40, 100, 50, 50)
    assert collision.check_left(player) is True

def test_check_left_false(collision):
    player = MockPlayer(20, 100, 50, 50)
    assert collision.check_left(player) is False

def test_check_right(collision):
    player = MockPlayer(160, 100, 50, 50)
    assert collision.check_right(player) is True

def test_check_right_false(collision):
    player = MockPlayer(180, 100, 50, 50)
    assert collision.check_right(player) is False

def test_collide_with_top(collision):
    player = MockPlayer(100, 40, 50, 50)
    assert collision.collide_with(player) == 0

def test_collide_with_no_collision(collision):
    player = MockPlayer(200, 200, 50, 50)
    assert collision.collide_with(player) == 4

def test_to_dict(collision):
    expected_dict = {
        "top": 50,
        "bottom": 150,
        "left": 50,
        "right": 150
    }
    assert collision.to_dict() == expected_dict

def test_from_dict():
    data = {
        "top": 50,
        "bottom": 150,
        "left": 50,
        "right": 150
    }
    collision = CCollision.from_dict(data)
    assert collision.m_top == 50
    assert collision.m_bottom == 150
    assert collision.m_left == 50
    assert collision.m_right == 150
