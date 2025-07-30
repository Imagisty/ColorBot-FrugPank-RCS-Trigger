import cv2
import numpy as np
from mss import mss
import win32api
import threading
import time
import sys
from pynput import keyboard, mouse
from pynput.mouse import Listener as MouseListener, Button

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS, FRAME_TIME
from utils import settings
from detection import detect_enemies
from aiming import enhanced_aim_at_target, enhanced_auto_shoot, create_bypass_process
from recoil import apply_recoil_compensation
from gui import create_enhanced_interface

# Глобальные переменные
shoot_button_pressed = False
sct = mss()

def on_mouse_click(x, y, button, pressed):
    """Выстрел!"""
    global shoot_button_pressed
    if button == Button.x1:  # Вторая боковая кнопка мыши
        shoot_button_pressed = pressed

def setup_listeners():
    """Тут идет чек на нажатия клава мышка """
    def on_press_key(key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                key_str = key.char
            else:
                key_str = str(key).replace('Key.', '')

            for action, binding in settings.key_bindings.items():
                if key_str == binding:
                    if action == "toggle_auto_aim":
                        from gui import toggle_auto_aim
                        toggle_auto_aim()
                    elif action == "toggle_auto_shoot":
                        from gui import toggle_auto_shoot
                        toggle_auto_shoot()
                    elif action == "toggle_recoil_compensation":
                        from gui import toggle_recoil_compensation
                        toggle_recoil_compensation()
                    break
        except Exception as e:
            pass

    def on_click_control(x, y, button, pressed):
        if pressed:
            button_str = str(button).replace('Button.', '')
            for action, binding in settings.key_bindings.items():
                if button_str == binding:
                    # Обработка клика
                    break

    keyboard_listener = keyboard.Listener(on_press=on_press_key)
    mouse_listener = mouse.Listener(on_click=on_click_control)
    shoot_listener = MouseListener(on_click=on_mouse_click)

    return keyboard_listener, mouse_listener, shoot_listener

def main_program(pipe):
    """В душе не ебу клауди кодил """
    settings.load_settings()
    settings.update_capture_zone()

    keyboard_listener, mouse_listener, shoot_listener = setup_listeners()

    keyboard_listener.start()
    mouse_listener.start()
    shoot_listener.start()

    print("🚀 Enhanced Dev")
    print(f"🖥️ Разрешение экрана: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"📹 Зона захвата: {settings.capture_zone_width}x{settings.capture_zone_height}")
    print(f"🎯 Центр прицела: ({SCREEN_WIDTH // 2}, {SCREEN_HEIGHT // 2})")
    print(f"🎮 FPS: {TARGET_FPS}")

    last_time = time.time()

    try:
        while settings.running:
            current_time = time.time()

            # Контроль FPS
            if current_time - last_time < FRAME_TIME:
                time.sleep(FRAME_TIME - (current_time - last_time))

            # Захват экрана
            monitor = settings.get_monitor_config()
            screenshot = np.array(sct.grab(monitor))[:, :, :3]
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

            enemy_centers, enhanced_mask, enemy_contours = detect_enemies(screenshot)

            if enemy_centers:
                crosshair_x = SCREEN_WIDTH // 2
                crosshair_y = SCREEN_HEIGHT // 2

                closest_distance = float("inf")
                closest_target = None

                # Поиск ближайшей цели
                for i, (center_x, center_y) in enumerate(enemy_centers):
                    distance = np.sqrt((crosshair_x - center_x) ** 2 + (crosshair_y - center_y) ** 2)

                    if distance < closest_distance:
                        closest_distance = distance
                        closest_target = (center_x, center_y)

                    # Визуализация
                    if i < len(enemy_contours):
                        cv2.drawContours(screenshot, [enemy_contours[i]], -1, (0, 255, 255), 2)

                    local_x = center_x - settings.capture_offset_x
                    local_y = center_y - settings.capture_offset_y

                    if 0 <= local_x < settings.capture_zone_width and 0 <= local_y < settings.capture_zone_height:
                        cv2.circle(screenshot, (local_x, local_y), 10, (0, 255, 0), -1)
                        cv2.circle(screenshot, (local_x, local_y), 15, (255, 255, 255), 3)
                        cv2.putText(screenshot, f"D:{int(distance)}", (local_x - 30, local_y - 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

                # Наведение и стрельба
                if settings.auto_aim_mode and closest_target is not None:
                    enhanced_aim_at_target(closest_target, crosshair_x, crosshair_y)

                if closest_target is not None and settings.auto_shoot_mode:
                    target_x, target_y = closest_target
                    enhanced_auto_shoot(target_x, target_y, crosshair_x, crosshair_y, pipe, shoot_button_pressed)

            # Компенсация отдачи
            apply_recoil_compensation()

            # Отображение
            resized_screenshot = cv2.resize(screenshot, None, fx=settings.scale_factor, fy=settings.scale_factor)

            # Статус на экране
            display_status_overlay(resized_screenshot, enemy_centers)

            cv2.imshow("Enhanced", resized_screenshot)

            if cv2.waitKey(1) == ord("q"):
                settings.running = False
                break

            last_time = current_time

    except KeyboardInterrupt:
        print("\n🛑 Программа прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        settings.running = False
        keyboard_listener.stop()
        mouse_listener.stop()
        shoot_listener.stop()
        cv2.destroyAllWindows()


def display_status_overlay(screenshot, enemy_centers):
    """Статус"""
    status_texts = [
        f"📹 Debug",
        f"🖥️ Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}",
        f"📹 Zone: {settings.capture_zone_width}x{settings.capture_zone_height} ({settings.capture_zone_size:.0f}%)",
        f"🎮 FPS: {TARGET_FPS}",
        f"🎯 Auto-Aim: {'ON' if settings.auto_aim_mode else 'OFF'}",
        f"🔫 Auto-Shoot: {'ON' if settings.auto_shoot_mode else 'OFF'}",
        f"⚡ Instant Snap: {'ON' if settings.instant_snap_mode else 'OFF'}",
        f"🎮 Recoil V/H: {settings.recoil_vertical:.1f}/{settings.recoil_horizontal:.1f}",
        f"👁️ Targets: {len(enemy_centers) if enemy_centers else 0}"
    ]

    for i, text in enumerate(status_texts):
        if "📹" in text or "ON" in text:
            color = (0, 255, 0)
        elif "OFF" in text:
            color = (0, 0, 255)
        else:
            color = (0, 255, 255)

        cv2.putText(screenshot, text, (10, 16 + i * 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, color, 1)

if __name__ == "__main__":
    try:
        # Мой байпас метод из валика
        parent_conn, bypass_process = create_bypass_process()

        # Тут гуи в отдельном потоке, тк винда не умеет в одном это делать вроде
        gui_thread = threading.Thread(target=create_enhanced_interface, daemon=True)
        gui_thread.start()

        time.sleep(2)

        # Запуск основной программы
        main_program(parent_conn)

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        settings.running = False
        if 'bypass_process' in locals():
            bypass_process.terminate()
            bypass_process.join()
        sys.exit(0)
