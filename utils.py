import json
import numpy as np
from config import *


class Settings:
    def __init__(self):
        """Тож чутка фикса разрешения """
        self.key_bindings = DEFAULT_KEY_BINDINGS.copy()
        self.radius_settings = DEFAULT_RADIUS_SETTINGS.copy()
        self.color_ranges = COLOR_RANGES.copy()

        # Загружаем настройки из DEFAULT_SETTINGS
        for key, value in DEFAULT_SETTINGS.items():
            setattr(self, key, value)

        # Убеждаемся что все атрибуты существуют с безопасными значениями
        self.smoothing_factor = getattr(self, 'smoothing_factor', 0.9)
        self.snap_sensitivity = getattr(self, 'snap_sensitivity', 0.8)
        self.center_bias_x = getattr(self, 'center_bias_x', 0.0)
        self.center_bias_y = getattr(self, 'center_bias_y', 0.0)
        self.instant_snap_mode = getattr(self, 'instant_snap_mode', True)
        self.precise_center_mode = getattr(self, 'precise_center_mode', True)

        # Настройки отдачи
        self.recoil_vertical = getattr(self, 'recoil_vertical', 0.2)
        self.recoil_horizontal = getattr(self, 'recoil_horizontal', -0.15)

        # Настройки детекции
        self.min_area = getattr(self, 'min_area', 1000)
        self.scale_factor = getattr(self, 'scale_factor', 0.4)
        self.fill_strength = getattr(self, 'fill_strength', 0.5)
        self.pixel_expansion = getattr(self, 'pixel_expansion', 0.8)
        self.contour_fill_aggressive = getattr(self, 'contour_fill_aggressive', 1.0)

        # Настройки зоны захвата
        self.capture_zone_size = getattr(self, 'capture_zone_size', 100.0)
        self.capture_zone_width = SCREEN_WIDTH
        self.capture_zone_height = SCREEN_HEIGHT
        self.capture_offset_x = 0
        self.capture_offset_y = 0

        # Настройки стрельбы
        self.shoot_delay = getattr(self, 'shoot_delay', 1)

        # НОВЫЕ НАСТРОЙКИ: Независимые от зоны захвата
        self.max_aim_distance = getattr(self, 'max_aim_distance', 300)
        self.auto_shoot_radius_horizontal = getattr(self, 'auto_shoot_radius_horizontal', 15)
        self.auto_shoot_radius_vertical = getattr(self, 'auto_shoot_radius_vertical', 15)
        self.recoil_multiplier = getattr(self, 'recoil_multiplier', 10)

        # Состояния системы
        self.auto_aim_mode = False
        self.auto_shoot_mode = False
        self.recoil_compensation_enabled = False
        self.running = True

        # Вот тут фикс
        self.base_resolution = [1920, 1080]
        self.current_resolution = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.resolution_scale_x = SCALE_FACTOR_X
        self.resolution_scale_y = SCALE_FACTOR_Y
        self.resolution_scale_combined = SCALE_FACTOR_COMBINED

        print("✅ Settings класс инициализирован с исправленной системой разрешения")
        print(f"📏 Масштабирование разрешения: {self.resolution_scale_x:.2f}x{self.resolution_scale_y:.2f}")
        print("✅ Добавлены независимые настройки для аим асиста и рекоила")

    def update_capture_zone(self):
        """Обновление параметров зоны захвата"""
        try:
            size_factor = self.capture_zone_size / 100.0
            self.capture_zone_width = int(SCREEN_WIDTH * size_factor)
            self.capture_zone_height = int(SCREEN_HEIGHT * size_factor)
            self.capture_offset_x = (SCREEN_WIDTH - self.capture_zone_width) // 2
            self.capture_offset_y = (SCREEN_HEIGHT - self.capture_zone_height) // 2

            print(
                f"📹 Зона захвата обновлена: {self.capture_zone_width}x{self.capture_zone_height} at ({self.capture_offset_x}, {self.capture_offset_y})")
        except Exception as e:
            print(f"❌ Ошибка при обновлении зоны захвата: {e}")

    def get_monitor_config(self):
        """Получение конфигурации монитора для захвата"""
        return {
            "top": self.capture_offset_y,
            "left": self.capture_offset_x,
            "width": self.capture_zone_width,
            "height": self.capture_zone_height
        }

    def convert_coordinates_to_screen(self, x, y):
        """Преобразование координат из зоны захвата в экранные координаты"""
        try:
            screen_x = x + self.capture_offset_x
            screen_y = y + self.capture_offset_y
            return screen_x, screen_y
        except Exception as e:
            print(f"❌ Ошибка при преобразовании координат: {e}")
            return x, y

    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            settings_data = {
                "key_bindings": self.key_bindings,
                "radius_settings": self.radius_settings,
                "color_ranges": {name: {"lower": range_data["lower"].tolist(),
                                        "upper": range_data["upper"].tolist()}
                                 for name, range_data in self.color_ranges.items()},

                # Основные настройки
                "smoothing_factor": self.smoothing_factor,
                "snap_sensitivity": self.snap_sensitivity,
                "center_bias_x": self.center_bias_x,
                "center_bias_y": self.center_bias_y,
                "instant_snap_mode": self.instant_snap_mode,
                "precise_center_mode": self.precise_center_mode,

                # Настройки отдачи
                "recoil_vertical": self.recoil_vertical,
                "recoil_horizontal": self.recoil_horizontal,

                # Настройки детекции
                "min_area": self.min_area,
                "scale_factor": self.scale_factor,
                "fill_strength": self.fill_strength,
                "pixel_expansion": self.pixel_expansion,
                "contour_fill_aggressive": self.contour_fill_aggressive,

                # Настройки зоны
                "capture_zone_size": self.capture_zone_size,

                # Настройки стрельбы
                "shoot_delay": self.shoot_delay,

                # НОВЫЕ НАСТРОЙКИ
                "max_aim_distance": self.max_aim_distance,
                "auto_shoot_radius_horizontal": self.auto_shoot_radius_horizontal,
                "auto_shoot_radius_vertical": self.auto_shoot_radius_vertical,
                "recoil_multiplier": self.recoil_multiplier,

                # Системная информация
                "screen_resolution": [SCREEN_WIDTH, SCREEN_HEIGHT],
                "resolution_fixed": True,  # Флаг исправленной версии
                "independent_aim_recoil": True  # Флаг независимых настроек
            }

            with open("enhanced_settings.json", "w", encoding='utf-8') as file:
                json.dump(settings_data, file, indent=2, ensure_ascii=False)

            print("💾 Настройки успешно сохранены с исправлением разрешения")

        except Exception as e:
            print(f"❌ Ошибка при сохранении настроек: {e}")

    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            with open("enhanced_settings.json", "r", encoding='utf-8') as file:
                data = json.load(file)

            # Проверяем версию исправления
            if data.get("resolution_fixed", False):
                print("✅ Загружены настройки с исправленным разрешением")
            else:
                print("⚠️ Загружены старые настройки, применяем исправления")

            # Загружаем key_bindings
            if "key_bindings" in data:
                self.key_bindings.update(data["key_bindings"])

            # Загружаем radius_settings (базовые значения)
            if "radius_settings" in data:
                self.radius_settings.update(data["radius_settings"])

            # Загружаем основные настройки
            self.smoothing_factor = data.get("smoothing_factor", 0.9)
            self.snap_sensitivity = data.get("snap_sensitivity", 0.8)
            self.center_bias_x = data.get("center_bias_x", 0.0)
            self.center_bias_y = data.get("center_bias_y", 0.0)
            self.instant_snap_mode = data.get("instant_snap_mode", True)
            self.precise_center_mode = data.get("precise_center_mode", True)

            self.recoil_vertical = data.get("recoil_vertical", 0.2)
            self.recoil_horizontal = data.get("recoil_horizontal", -0.15)

            self.min_area = data.get("min_area", 1000)
            self.scale_factor = data.get("scale_factor", 0.4)
            self.fill_strength = data.get("fill_strength", 0.5)
            self.pixel_expansion = data.get("pixel_expansion", 0.8)
            self.contour_fill_aggressive = data.get("contour_fill_aggressive", 1.0)

            self.capture_zone_size = data.get("capture_zone_size", 100.0)
            self.shoot_delay = data.get("shoot_delay", 1)

            # НОВЫЕ НАСТРОЙКИ
            self.max_aim_distance = data.get("max_aim_distance", 300)
            self.auto_shoot_radius_horizontal = data.get("auto_shoot_radius_horizontal", 15)
            self.auto_shoot_radius_vertical = data.get("auto_shoot_radius_vertical", 15)
            self.recoil_multiplier = data.get("recoil_multiplier", 10)

            # Загружаем цветовые диапазоны
            if "color_ranges" in data:
                for name, range_data in data["color_ranges"].items():
                    if name in self.color_ranges:
                        self.color_ranges[name]["lower"] = np.array(range_data["lower"])
                        self.color_ranges[name]["upper"] = np.array(range_data["upper"])

            if data.get("independent_aim_recoil", False):
                print("✅ Загружены независимые настройки аим асиста и рекоила")

            print("✅ Настройки успешно загружены")

        except FileNotFoundError:
            print("⚠️ Файл настроек не найден, создаем новый...")
            self.save_settings()
        except Exception as e:
            print(f"❌ Ошибка при загрузке настроек: {e}")

    def get_status_info(self):
        """Получение информации о текущем состоянии системы"""
        return {
            "auto_aim": "ON" if self.auto_aim_mode else "OFF",
            "auto_shoot": "ON" if self.auto_shoot_mode else "OFF",
            "recoil_comp": "ON" if self.recoil_compensation_enabled else "OFF",
            "instant_snap": "ON" if self.instant_snap_mode else "OFF",
            "capture_zone": f"{self.capture_zone_width}x{self.capture_zone_height}",
            "capture_size": f"{self.capture_zone_size:.0f}%",
            "resolution": f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}",
            "scale_factor": f"{self.resolution_scale_x:.2f}x{self.resolution_scale_y:.2f}"
        }

    def reset_to_defaults(self):
        """Сброс всех настроек к значениям по умолчанию"""
        try:
            for key, value in DEFAULT_SETTINGS.items():
                setattr(self, key, value)

            self.radius_settings = DEFAULT_RADIUS_SETTINGS.copy()
            self.key_bindings = DEFAULT_KEY_BINDINGS.copy()
            self.color_ranges = COLOR_RANGES.copy()

            print("🔄 Настройки сброшены к значениям по умолчанию")
        except Exception as e:
            print(f"❌ Ошибка при сбросе настроек: {e}")

    def validate_settings(self):
        """Проверка корректности настроек"""
        try:
            if not 0.1 <= self.smoothing_factor <= 1.0:
                self.smoothing_factor = 0.9

            if not 0.1 <= self.snap_sensitivity <= 2.0:
                self.snap_sensitivity = 0.8

            if not -50 <= self.center_bias_x <= 50:
                self.center_bias_x = 0.0

            if not -50 <= self.center_bias_y <= 50:
                self.center_bias_y = 0.0

            if not -2.0 <= self.recoil_vertical <= 2.0:
                self.recoil_vertical = 0.2

            if not -2.0 <= self.recoil_horizontal <= 2.0:
                self.recoil_horizontal = -0.15

            print("✅ Валидация настроек завершена")
        except Exception as e:
            print(f"❌ Ошибка при валидации настроек: {e}")


# Создание глобального объекта настроек
settings = Settings()

# Автоматическая загрузка настроек при импорте модуля
if __name__ != "__main__":
    try:
        print("🔄 Автоматическая загрузка настроек...")
        settings.load_settings()
        settings.validate_settings()
        settings.update_capture_zone()
        print("✅ Модуль utils.py успешно инициализирован с исправлениями")
    except Exception as e:
        print(f"⚠️ Ошибка при автоматической загрузке: {e}")
