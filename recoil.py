import win32api
import win32con
import numpy as np
from config import normalize_recoil, SCALE_FACTOR_X, SCALE_FACTOR_Y, SCREEN_WIDTH, SCREEN_HEIGHT
from utils import settings


def apply_recoil_compensation():
    """Магический пиздец"""
    if settings.recoil_compensation_enabled and win32api.GetKeyState(0x01) < 0:
        # Вроде фикс резолюшена
        normalized_vertical, normalized_horizontal = normalize_recoil(
            settings.recoil_vertical,
            settings.recoil_horizontal
        )

        # Фикс множ
        horizontal_move = int(normalized_horizontal * settings.recoil_multiplier)
        vertical_move = int(normalized_vertical * settings.recoil_multiplier)

        # магические числа
        if SCREEN_WIDTH > 2560 or SCREEN_HEIGHT > 1440:
            horizontal_move = int(horizontal_move * 0.8)
            vertical_move = int(vertical_move * 0.8)
        elif SCREEN_WIDTH < 1280 or SCREEN_HEIGHT < 720:
            horizontal_move = int(horizontal_move * 1.2)
            vertical_move = int(vertical_move * 1.2)

        # огран по резу
        max_move = 50
        horizontal_move = max(-max_move, min(max_move, horizontal_move))
        vertical_move = max(-max_move, min(max_move, vertical_move))

        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, horizontal_move, vertical_move, 0, 0)

        # дЕГАБ
        if abs(horizontal_move) > 1 or abs(vertical_move) > 1:
            print(
                f"RECOIL INDEPENDENT: H={horizontal_move}, V={vertical_move}, multiplier={settings.recoil_multiplier}")


def get_resolution_factor():
    """Получение коэффициента компенсации для разрешения"""
    base_pixels = 1920 * 1080
    current_pixels = SCREEN_WIDTH * SCREEN_HEIGHT
    pixel_ratio = current_pixels / base_pixels
    resolution_factor = 1.0 / np.sqrt(pixel_ratio)
    resolution_factor = max(0.5, min(2.0, resolution_factor))
    return resolution_factor


def calculate_adaptive_recoil(weapon_type="auto"):
    """Я в душе не ебу где оно вообще существует в гуи"""
    weapon_multipliers = {
        "auto": 1.0,
        "burst": 0.7,
        "semi": 0.3,
        "sniper": 0.1
    }

    base_multiplier = weapon_multipliers.get(weapon_type, 1.0)
    resolution_factor = get_resolution_factor()

    return base_multiplier * resolution_factor
