CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

PROCESS_SCALE = 0.5
BLUR_SIZE = 5
MORPH_KERNEL_SIZE = 5
USE_CLAHE = True

MIN_AREA = 600
MIN_FILL_RATIO = 0.3

MAX_TRACK_DISTANCE = 80
MAX_DISAPPEARED = 15
TRAIL_LENGTH = 30

PANEL_WIDTH = 260

COLORS = {
    "red": {
        "h_min": 0, "h_max": 8,
        "s_min": 130, "s_max": 255,
        "v_min": 70, "v_max": 255,
        "box": (0, 0, 255),
        "wrap": True,
    },
    "green": {
        "h_min": 40, "h_max": 85,
        "s_min": 80, "s_max": 255,
        "v_min": 35, "v_max": 255,
        "box": (0, 200, 0),
        "wrap": False,
    },
}
