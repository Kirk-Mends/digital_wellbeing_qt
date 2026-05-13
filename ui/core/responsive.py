from PyQt6.QtCore import QSize


LAPTOP_MAX_WIDTH = 1440  # you can tweak this


def is_laptop_size(size: QSize) -> bool:
    return size.width() <= LAPTOP_MAX_WIDTH


def should_full_width_on_laptop(size: QSize) -> bool:
    return is_laptop_size(size)
