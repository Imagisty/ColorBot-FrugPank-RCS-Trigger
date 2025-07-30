import cv2
import numpy as np
from utils import settings


def conservative_contour_processing(mask, aggressiveness=1.0):
    """Консервативная обработка контуров"""
    blur_size = max(3, int(3 + aggressiveness))
    if blur_size % 2 == 0:
        blur_size += 1

    blurred = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)

    kernel_size = max(3, int(2 + aggressiveness))
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # ИСПРАВЛЕНО: Правильный порядок параметров
    closed = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel, iterations=1)
    return closed


def calculate_precise_target_center(contour, original_mask):
    """Максимально точное вычисление центра цели"""
    x, y, w, h = cv2.boundingRect(contour)
    roi_mask = original_mask[y:y + h, x:x + w]

    if roi_mask.size == 0:
        return None

    white_pixels = np.where(roi_mask == 255)
    if len(white_pixels[0]) == 0:
        return None

    pixel_weights = roi_mask[white_pixels] / 255.0
    weighted_y = np.average(white_pixels[0], weights=pixel_weights)
    weighted_x = np.average(white_pixels[1], weights=pixel_weights)

    local_x = int(weighted_x) + x
    local_y = int(weighted_y) + y

    global_x, global_y = settings.convert_coordinates_to_screen(local_x, local_y)

    calibrated_x = global_x + int(settings.center_bias_x)
    calibrated_y = global_y + int(settings.center_bias_y)

    # Небольшая корректировка по Y для лучшего попадания
    adjusted_y = calibrated_y - int(h * 0.08)

    return (calibrated_x, adjusted_y)


def detect_enemies(image):
    """Детекция с фокусом на точность центрирования"""
    try:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # HSV диапазоны для neon pink-purple
        lower_neon_pink1 = np.array([145, 100, 150])
        upper_neon_pink1 = np.array([165, 255, 255])

        lower_neon_pink2 = np.array([135, 120, 180])
        upper_neon_pink2 = np.array([155, 255, 255])

        lower_magenta = np.array([140, 150, 200])
        upper_magenta = np.array([170, 255, 255])

        # Создание и объединение масок
        mask1 = cv2.inRange(hsv, lower_neon_pink1, upper_neon_pink1)
        mask2 = cv2.inRange(hsv, lower_neon_pink2, upper_neon_pink2)
        mask3 = cv2.inRange(hsv, lower_magenta, upper_magenta)

        mask = cv2.bitwise_or(mask1, mask2)
        mask = cv2.bitwise_or(mask, mask3)

        # Исключение красного и синего
        red_lower1 = np.array([0, 100, 100])
        red_upper1 = np.array([10, 255, 255])
        red_lower2 = np.array([170, 100, 100])
        red_upper2 = np.array([179, 255, 255])

        red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
        red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        blue_lower = np.array([100, 100, 100])
        blue_upper = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

        mask = cv2.bitwise_and(mask, cv2.bitwise_not(red_mask))
        mask = cv2.bitwise_and(mask, cv2.bitwise_not(blue_mask))

        original_mask = mask.copy()

        # Обработка контуров
        mask = conservative_contour_processing(mask, settings.contour_fill_aggressive)

        # Расширение пикселей если нужно
        if settings.pixel_expansion > 1.0:
            expansion_kernel = np.ones((3, 3), np.uint8)
            mask = cv2.dilate(mask, expansion_kernel, iterations=int(settings.pixel_expansion - 1.0))

        # Поиск контуров
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        enemy_centers = []
        enemy_contours = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > settings.min_area:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h

                # Фильтр по соотношению сторон
                if 0.3 <= aspect_ratio <= 3.0:
                    if settings.precise_center_mode:
                        center_point = calculate_precise_target_center(contour, original_mask)
                    else:
                        M = cv2.moments(contour)
                        if M['m00'] != 0:
                            local_cx = int(M['m10'] / M['m00'])
                            local_cy = int(M['m01'] / M['m00'])
                            global_cx, global_cy = settings.convert_coordinates_to_screen(local_cx, local_cy)
                            center_point = (global_cx, global_cy)
                        else:
                            center_point = None

                    if center_point:
                        enemy_centers.append(center_point)
                        enemy_contours.append(contour)

        return enemy_centers, mask, enemy_contours

    except Exception as e:
        print(f"Ошибка при обнаружении: {e}")
        return [], None, []
