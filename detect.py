import cv2
import numpy as np
import config

KERNEL = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE, (config.MORPH_KERNEL_SIZE, config.MORPH_KERNEL_SIZE)
)
CLAHE = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))


def preprocess(frame, use_clahe):
    small = cv2.resize(
        frame, None,
        fx=config.PROCESS_SCALE, fy=config.PROCESS_SCALE,
        interpolation=cv2.INTER_AREA,
    )
    small = cv2.GaussianBlur(small, (config.BLUR_SIZE, config.BLUR_SIZE), 0)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    if use_clahe:
        hsv[:, :, 2] = CLAHE.apply(hsv[:, :, 2])
    return hsv


def build_mask(hsv, color):
    lower = np.array([color["h_min"], color["s_min"], color["v_min"]], dtype=np.uint8)
    upper = np.array([color["h_max"], color["s_max"], color["v_max"]], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)

    if color["wrap"]:
        lower2 = np.array([180 - color["h_max"], color["s_min"], color["v_min"]], dtype=np.uint8)
        upper2 = np.array([180 - color["h_min"], color["s_max"], color["v_max"]], dtype=np.uint8)
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower2, upper2))

    return mask


def clean_mask(mask):
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL)
    return mask


def find_objects(mask, color_name):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    scale_back = 1.0 / config.PROCESS_SCALE
    min_area = config.MIN_AREA * config.PROCESS_SCALE * config.PROCESS_SCALE
    objects = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        if area / (w * h) < config.MIN_FILL_RATIO:
            continue

        x = int(x * scale_back)
        y = int(y * scale_back)
        w = int(w * scale_back)
        h = int(h * scale_back)
        objects.append({
            "color": color_name,
            "box": (x, y, w, h),
            "center": (x + w // 2, y + h // 2),
            "area": int(area * scale_back * scale_back),
        })

    return objects