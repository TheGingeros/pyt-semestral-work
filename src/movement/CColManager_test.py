# test_colmanager.py

import pytest
from src.movement.CColManager import ColManager
from src.movement.CCollision import CCollision
@pytest.fixture
def collision():
    return CCollision(50, 50, 100, 100)

@pytest.fixture
def manager(collision):
    manager = ColManager()
    manager.m_collisions.append(collision)
    return manager

def test_to_dict(manager):
    expected_dict = {
        "collision": [
            {
                "top": 50,
                "bottom": 150,
                "left": 50,
                "right": 150
            }
        ]
    }
    assert manager.to_dict() == expected_dict

def test_from_dict():
    data = {
        "collision": [
            {
                "top": 50,
                "bottom": 150,
                "left": 50,
                "right": 150
            }
        ]
    }
    manager = ColManager.from_dict(data)
    assert len(manager.m_collisions) == 1
    collision = manager.m_collisions[0]
    assert collision.m_top == 50
    assert collision.m_bottom == 150
    assert collision.m_left == 50
    assert collision.m_right == 150
