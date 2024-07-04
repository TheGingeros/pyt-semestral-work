# test_cdeadmenu.py

import pytest
import pygame
from unittest.mock import Mock, patch
from src.menu.CDeadMenu import CDeadMenu
@pytest.fixture
def screen():
    pygame.init()
    return pygame.display.set_mode((800, 600))

@pytest.fixture
def menu(screen):
    return CDeadMenu(screen)

def test_init(menu, screen):
    assert menu.rect.width == screen.get_width()
    assert menu.rect.height == screen.get_height()
    assert menu.m_options == ["Play Again", "Load Save", "Quit"]
    assert menu.m_active_option == 0
    assert isinstance(menu.m_key_update_time, int)

def test_handle_key_input_play_again(menu):
    with patch('pygame.key.get_pressed', return_value={pygame.K_RETURN: True}):
        assert menu.handle_key_input() == 1

def test_handle_key_input_load_save(menu):
    menu.m_active_option = 1
    with patch('pygame.key.get_pressed', return_value={pygame.K_RETURN: True}):
        assert menu.handle_key_input() == 2

def test_handle_key_input_quit(menu):
    menu.m_active_option = 2
    with patch('pygame.key.get_pressed', return_value={pygame.K_RETURN: True}):
        assert menu.handle_key_input() == 3

def test_handle_key_input_no_action(menu):
    with patch('pygame.key.get_pressed', return_value={pygame.K_RETURN: False, pygame.K_UP: False, pygame.K_DOWN: False}):
        assert menu.handle_key_input() == 0
def test_render(menu, screen):
    with patch.object(menu, 'render_options') as mock_render_options:
        with patch.object(menu, 'handle_key_input', return_value=1) as mock_handle_key_input:
            result = menu.render(screen)
            assert result == 1
            mock_render_options.assert_called_once_with(screen)
            mock_handle_key_input.assert_called_once()
