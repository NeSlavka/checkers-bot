from PIL import ImageGrab
import time

def get_pixel_color(x, y):
    bbox = (x, y, x + 1, y + 1)
    img = ImageGrab.grab(bbox=bbox)
    return img.getpixel((0, 0))

# Меняем значение по умолчанию на 5
def is_color_similar(color1, color2, tolerance_percent=2):
    r1, g1, b1 = color1[:3]
    r2, g2, b2 = color2[:3]
    
    diff_r = abs(r1 - r2)
    diff_g = abs(g1 - g2)
    diff_b = abs(b1 - b2)
    
    average_diff = (diff_r + diff_g + diff_b) / 3
    percent_diff = (average_diff / 255) * 100
    
    return percent_diff <= tolerance_percent

# time.sleep(2)
# # --- Основная часть ---
# x1, y1 = 980, 705
# x2, y2 = 730, 355

# color1 = get_pixel_color(x1, y1)
# color2 = get_pixel_color(x2, y2)

# print(f"Цвет в ({x1}, {y1}): RGB{color1}")
# print(f"Цвет в ({x2}, {y2}): RGB{color2}")

# result = is_color_similar(color1, color2, tolerance_percent=5)