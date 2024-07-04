"""Function collection for the game"""
import math
import pygame

def load_texture(name):
    """Function for loading textures

    Args:
        name (string): texture path

    Raises:
        SystemExit: If we cant locate the image

    Returns:
        pygame.image: Returns pygame.image object
    """
    image = None
    try:
        image = pygame.image.load(name).convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {image}")
        raise SystemExit
    return image

def inside_circle(rect, item_rect, radius)->bool:
    """Checks if one rect is inside the other

    Args:
        rect (pygame.Rect): first object rect
        item_rect (pygame.Rect): second object rect
        radius (int): radius of the intersection

    Returns:
        bool: Returns true if they are inside each other
    """
    a = item_rect.x+item_rect.width/2
    b = item_rect.y+item_rect.height/2
    x = rect.x+rect.width/2
    y = rect.y+rect.height/2
    z = (x-a)**2 + (y-b)**2
    return z <= radius**2
def distance_of_two_points(rect_a, rect_b)->int:
    """Function for calculating distance of two points in 2D

    Args:
        rect_a (pygame.Rect): first object rect
        rect_b (pygame.Rect): second object rect

    Returns:
        int: Returns the distance of the two points
    """
    x1 = rect_a.x + rect_a.width/2
    y1 = rect_a.y + rect_a.height/2
    x2 = rect_b.x + rect_b.width/2
    y2 = rect_b.y + rect_b.height/2
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))
