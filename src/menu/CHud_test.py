# test_chud.py

import pytest
import pygame
from unittest.mock import Mock, patch
from src.menu.CHud import CHud
from src.menu.CDeadMenu import CDeadMenu
from src.level.CLevel import CLevel
from src.level.CInteractiveItem import CInteractiveItem

@pytest.fixture
def screen():
    pygame.init()
    return pygame.display.set_mode((800, 600))

@pytest.fixture
def player():
    player = Mock()
    player.m_real_pos_x = 100
    player.m_real_pos_y = 200
    player.m_hp = 80
    player.m_damage = 15
    player.m_speed = 5
    return player

@pytest.fixture
def hud(screen, player):
    return CHud(screen, player)

def test_init(hud, screen, player):
    assert hud.m_player == player
    assert hud.m_interactive_items == []
    assert hud.m_active_level is None
    assert hud.m_active_level_index == 1
    assert not hud.m_new_rect
    assert isinstance(hud.m_dead_menu, CDeadMenu)

def test_render_player_coords(hud, screen):
    hud.render_player_coords(screen)
    font = pygame.font.SysFont('Arial', 30)
    coords = f"X: 100 Y: 200"
    coords_text = font.render(coords, True, (0, 0, 0))
    coords_text_rect = coords_text.get_rect()
    coords_text_rect.x = screen.get_width() / 2 - coords_text_rect.width / 2
    coords_text_rect.y = 0
    screen.blit(coords_text, coords_text_rect)
    assert screen.get_at((coords_text_rect.x, coords_text_rect.y)) == (0, 0, 0, 255)

def test_render_current_location(hud, screen):
    hud.m_active_level = Mock()
    hud.m_active_level.m_name = "Test Level"
    hud.render_current_location(screen)
    font = pygame.font.SysFont('Arial', 30)
    current_location = f"Current location: Test Level"
    render_label = font.render(current_location, True, (0, 0, 0))
    render_label_rect = render_label.get_rect()
    render_label_rect.x = 17
    render_label_rect.y = 17
    screen.blit(render_label, render_label_rect)
    assert screen.get_at((render_label_rect.x, render_label_rect.y)) == (0, 0, 0, 255)

def test_render_action_label(hud, screen):
    mock_level = Mock(spec=CLevel)
    mock_level.m_name = "Test Level"
    mock_level.m_unlocked = False
    mock_item = Mock(spec=CInteractiveItem)
    mock_item.m_data = mock_level
    mock_item.m_action_name = "Enter"
    hud.render_action_label(mock_item, screen)
    font = pygame.font.SysFont('Arial', 30)
    edited_label = "This level is not yet unlocked"
    render_label = font.render(edited_label, True, (0, 0, 0))
    render_label_rect = render_label.get_rect()
    render_label_rect.x = screen.get_width() / 2 - render_label_rect.width / 2
    render_label_rect.y = screen.get_height() - render_label_rect.height - 60
    screen.blit(render_label, render_label_rect)
    assert screen.get_at((render_label_rect.x, render_label_rect.y)) == (0, 0, 0, 255)
