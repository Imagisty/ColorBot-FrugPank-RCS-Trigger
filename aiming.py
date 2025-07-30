import win32api
import win32con
import numpy as np
import time
from ctypes import windll
from multiprocessing import Pipe, Process
from pynput.mouse import Controller
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR_X, SCALE_FACTOR_Y,
                    SCALE_FACTOR_COMBINED, normalize_mouse_movement, normalize_distance)
from utils import settings

# Инициализация мыши
mouse_controller = Controller()


def bypass(pipe):
    """Функция для отправки клавиш в обход защиты"""
    keybd_event = windll.user32.keybd_event
    while True:
        try:
            key = pipe.recv()
            if key == b'\x01':
                keybd_event(0x4F, 0, 0, 0)  # Нажатие клавиши O
                keybd_event(0x4F, 0, 2, 0)  # Отпускание клавиши O
        except EOFError:
            break


def send_key_multiprocessing(pipe):
    """Отправка сигнала на выстрел"""
    try:
        pipe.send(b'\x01')
    except:
        pass


def enhanced_shoot(pipe):
    """Улучшенная функция стрельбы с задержкой"""
    if settings.shoot_delay > 0:
        time.sleep(settings.shoot_delay / 1000.0)
    send_key_multiprocessing(pipe)


def enhanced_aim_at_target(target, crosshair_x, crosshair_y):
    """ИСПРАВЛЕНО: Наведение независимо от зоны захвата"""
    target_x, target_y = target

    delta_x = target_x - crosshair_x
    delta_y = target_y - crosshair_y
    distance = np.sqrt(delta_x ** 2 + delta_y ** 2)

    # ИСПРАВЛЕНО: Используем отдельные настройки для ограничения аим асиста
    max_aim_distance = settings.max_aim_distance

    if win32api.GetKeyState(0x01) < 0 and distance <= max_aim_distance:
        if settings.instant_snap_mode:
            if distance > 2:
                # Базовое движение
                base_move_x = delta_x * settings.snap_sensitivity * 1.2
                base_move_y = delta_y * settings.snap_sensitivity * 1.2

                # Нормализация движения
                move_x, move_y = normalize_mouse_movement(base_move_x, base_move_y)

                # Ограничиваем максимальное движение
                max_move = int(150 / min(SCALE_FACTOR_X, SCALE_FACTOR_Y)) if min(SCALE_FACTOR_X,
                                                                                 SCALE_FACTOR_Y) > 1 else 150
                move_x = max(-max_move, min(max_move, move_x))
                move_y = max(-max_move, min(max_move, move_y))

                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, move_x, move_y, 0, 0)
                print(f"AIM FIXED: distance={distance:.1f}, max_distance={max_aim_distance}, move=({move_x}, {move_y})")
            else:
                # Точное наведение
                base_move_x = delta_x * 0.9
                base_move_y = delta_y * 0.9
                move_x, move_y = normalize_mouse_movement(base_move_x, base_move_y)
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, move_x, move_y, 0, 0)
                print(f"AIM PRECISION: distance={distance:.1f}, move=({move_x}, {move_y})")


def enhanced_auto_shoot(target_x, target_y, crosshair_x, crosshair_y, pipe, shoot_button_pressed):
    """ИСПРАВЛЕНО: Автострельба независимо от зоны захвата"""
    horizontal_diff = abs(target_x - crosshair_x)
    vertical_diff = abs(target_y - crosshair_y)

    # ИСПРАВЛЕНО: Используем фиксированные радиусы стрельбы независимо от зоны захвата
    base_h_radius = settings.auto_shoot_radius_horizontal
    base_v_radius = settings.auto_shoot_radius_vertical

    # Применяем только масштабирование разрешения, НЕ зоны захвата
    shoot_h_radius = int(base_h_radius * SCALE_FACTOR_X)
    shoot_v_radius = int(base_v_radius * SCALE_FACTOR_Y)

    if (horizontal_diff <= shoot_h_radius and
            vertical_diff <= shoot_v_radius and
            shoot_button_pressed):
        enhanced_shoot(pipe)
        print(
            f"AUTO-SHOOT FIXED: target=({target_x}, {target_y}), crosshair=({crosshair_x}, {crosshair_y}), radius=({shoot_h_radius}, {shoot_v_radius})")


def create_bypass_process():
    """Создание процесса bypass"""
    parent_conn, child_conn = Pipe()
    bypass_process = Process(target=bypass, args=(child_conn,))
    bypass_process.start()
    return parent_conn, bypass_process
