import numpy as np
from mss import mss


def get_screen_resolution():
    """Автоматическое определение разрешения экрана"""
    try:
        with mss() as sct:
            screen = sct.monitors[1]  # Основной монитор
            return screen["width"], screen["height"]
    except:
        return 1920, 1080  # Значение по умолчанию


# Получаем реальное разрешение экрана
SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_resolution()

# Базовое разрешение для нормализации (эталонное)
BASE_WIDTH = 1920
BASE_HEIGHT = 1080

# ИСПРАВЛЕНО: Правильные коэффициенты масштабирования
SCALE_FACTOR_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_FACTOR_Y = SCREEN_HEIGHT / BASE_HEIGHT
SCALE_FACTOR_COMBINED = min(SCALE_FACTOR_X, SCALE_FACTOR_Y)

# Параметры FPS и производительности
TARGET_FPS = 60
FRAME_TIME = 1.0 / TARGET_FPS

# Константы детекции
DETECTION_AREA_MIN = 50

# Границы цвета для отслеживания (неоново-розовый)
COLOR_RANGES = {
    "neon_pink1": {"lower": np.array([145, 100, 150]), "upper": np.array([165, 255, 255])},
    "neon_pink2": {"lower": np.array([135, 120, 180]), "upper": np.array([155, 255, 255])},
    "magenta": {"lower": np.array([140, 150, 200]), "upper": np.array([170, 255, 255])}
}

# ИСПРАВЛЕНО: Настройки БЕЗ предварительного масштабирования
DEFAULT_SETTINGS = {
    "min_area": 1000,  # Базовое значение
    "scale_factor": 0.4,
    "fill_strength": 0.5,
    "pixel_expansion": 0.8,
    "contour_fill_aggressive": 1.0,
    "precise_center_mode": True,
    "center_bias_x": 0.0,
    "center_bias_y": 0.0,
    "instant_snap_mode": True,
    "smoothing_factor": 0.9,
    "snap_sensitivity": 0.8,
    "recoil_vertical": 0.2,
    "recoil_horizontal": -0.15,
    "capture_zone_size": 100.0,
    "shoot_delay": 1,

    # НОВЫЕ НАСТРОЙКИ: Независимые от зоны захвата
    "max_aim_distance": 300,  # Максимальная дистанция для аим асиста (в пикселях)
    "auto_shoot_radius_horizontal": 15,  # Горизонтальный радиус автострельбы
    "auto_shoot_radius_vertical": 15,  # Вертикальный радиус автострельбы
    "recoil_multiplier": 10,  # Множитель для компенсации отдачи
}

# ИСПРАВЛЕНО: Базовые радиусы БЕЗ масштабирования
DEFAULT_RADIUS_SETTINGS = {
    "auto_shoot_horizontal_radius": 15,  # Базовые значения для 1920x1080
    "auto_shoot_vertical_radius": 15,
    "auto_aim_horizontal_radius": 400,
    "auto_aim_vertical_radius": 400,
    "auto_aim_detection_area_x": 600,
    "auto_aim_detection_area_y": 600
}

# Настройки клавиш по умолчанию
DEFAULT_KEY_BINDINGS = {
    "toggle_auto_aim": "0",
    "toggle_auto_shoot": "8",
    "toggle_recoil_compensation": "9",
    "increase_recoil_strength": "+",
    "decrease_recoil_strength": "-"
}


# ИСПРАВЛЕНО: Правильные функции нормализации
def normalize_mouse_movement(x, y):
    """Нормализация движения мыши - ИСПРАВЛЕНО"""
    # Инвертированная нормализация для правильного поведения
    if SCALE_FACTOR_X > 1.0:  # Разрешение больше базового
        normalized_x = x / SCALE_FACTOR_X
    else:  # Разрешение меньше базового
        normalized_x = x * SCALE_FACTOR_X

    if SCALE_FACTOR_Y > 1.0:
        normalized_y = y / SCALE_FACTOR_Y
    else:
        normalized_y = y * SCALE_FACTOR_Y

    return int(normalized_x), int(normalized_y)


def normalize_distance(distance):
    """Нормализация дистанции под текущее разрешение"""
    return distance * SCALE_FACTOR_COMBINED


def normalize_radius(radius_x, radius_y):
    """Нормализация радиусов под текущее разрешение"""
    return int(radius_x * SCALE_FACTOR_X), int(radius_y * SCALE_FACTOR_Y)


def normalize_recoil(vertical, horizontal):
    """Нормализация отдачи - ИСПРАВЛЕНО"""
    # Инвертированная формула для правильной компенсации
    dpi_factor = (SCREEN_WIDTH * SCREEN_HEIGHT) / (BASE_WIDTH * BASE_HEIGHT)

    # Чем больше разрешение, тем меньше нужно движения мыши
    if dpi_factor > 1.0:
        recoil_scale = 1.0 / np.sqrt(dpi_factor)
    else:
        recoil_scale = np.sqrt(dpi_factor)

    # Применяем инвертированное масштабирование
    normalized_vertical = vertical * recoil_scale
    normalized_horizontal = horizontal * recoil_scale

    return normalized_vertical, normalized_horizontal


print(f"🖥️ Разрешение экрана: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
print(f"📏 Масштабирование: X={SCALE_FACTOR_X:.2f}, Y={SCALE_FACTOR_Y:.2f}, Combined={SCALE_FACTOR_COMBINED:.2f}")
print(f"🎯 Целевой FPS: {TARGET_FPS}")
