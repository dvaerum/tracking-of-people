from typing import Tuple
import math

x_constant = (1920 / 61) * 0.6 * -1
y_constant = (1080 / 32) * 0.6 * -1

def pixel2degrees(x_start: int, x_width: int, y_start: int, y_height) -> Tuple[int, int]:
    try:

        x_center = x_start + (x_width / 2)
        x_degrees = 35 + x_center / x_constant
        if x_degrees > 360.0:
            x_degrees = x_degrees - 360.0
        elif x_degrees < 0:
            x_degrees = x_degrees + 360.0

            y_degrees = 24 + y_start / y_constant

        return (x_degrees, y_degrees)
    except Exception:
        return (0, 90)

def skip_class_id(class_id: int):
    if class_id in [0, 56]:
        return False
    else:
        #return False
        return True


