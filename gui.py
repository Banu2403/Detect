import cv2
import numpy as np
import config

SLIDER_WINDOW = "HSV Controls"
FONT = cv2.FONT_HERSHEY_SIMPLEX
SLIDER_KEYS = ["h_min", "h_max", "s_min", "s_max", "v_min", "v_max"]
SLIDER_LIMITS = {"h": 179, "s": 255, "v": 255}


def do_nothing(value):
    pass


def create_sliders(color_name):
    cv2.namedWindow(SLIDER_WINDOW)
    cv2.resizeWindow(SLIDER_WINDOW, 420, 300)
    for key in SLIDER_KEYS:
        cv2.createTrackbar(
            key, SLIDER_WINDOW,
            config.COLORS[color_name][key],
            SLIDER_LIMITS[key[0]],
            do_nothing,
        )


def load_sliders(color_name):
    for key in SLIDER_KEYS:
        cv2.setTrackbarPos(key, SLIDER_WINDOW, config.COLORS[color_name][key])


def read_sliders(color_name):
    for key in SLIDER_KEYS:
        config.COLORS[color_name][key] = cv2.getTrackbarPos(key, SLIDER_WINDOW)


def show_slider_banner(color_name):
    banner = np.full((50, 420, 3), (35, 35, 35), np.uint8)
    box_color = config.COLORS[color_name]["box"]
    cv2.rectangle(banner, (10, 12), (40, 38), box_color, -1)
    cv2.putText(banner, "Editing: " + color_name + "  (press C to switch)", (50, 31), FONT, 0.55, (255, 255, 255), 1)
    cv2.imshow(SLIDER_WINDOW, banner)


def draw_detections(frame, detections, tracker):
    for track in tracker.tracks.values():
        if track["disappeared"] > 0:
            continue
        color = config.COLORS[track["color"]]["box"]
        points = track["path"]
        for i in range(1, len(points)):
            cv2.line(frame, points[i - 1], points[i], color, 2)

    for det in detections:
        x, y, w, h = det["box"]
        color = config.COLORS[det["color"]]["box"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        label = det["color"] + " #" + str(det["id"])
        cv2.putText(frame, label, (x, max(y - 8, 15)), FONT, 0.55, color, 2)
        cv2.circle(frame, det["center"], 4, color, -1)


def build_dashboard(frame, counts, totals, fps, selected, mask, use_clahe):
    height = frame.shape[0]
    panel = np.full((height, config.PANEL_WIDTH, 3), (35, 35, 35), np.uint8)
    white = (255, 255, 255)
    gray = (170, 170, 170)

    cv2.putText(panel, "COLOR DETECTOR", (15, 30), FONT, 0.7, white, 2)
    cv2.line(panel, (15, 42), (config.PANEL_WIDTH - 15, 42), (90, 90, 90), 1)
    cv2.putText(panel, "FPS: " + str(round(fps, 1)), (15, 70), FONT, 0.55, (0, 255, 255), 1)

    y = 105
    for name, count in counts.items():
        color = config.COLORS[name]["box"]
        cv2.rectangle(panel, (15, y - 14), (35, y + 6), color, -1)
        text = name.capitalize() + ": " + str(count) + " (seen " + str(totals.get(name, 0)) + ")"
        cv2.putText(panel, text, (45, y), FONT, 0.5, white, 1)
        y += 32

    cv2.putText(panel, "Objects now: " + str(sum(counts.values())), (15, 175), FONT, 0.6, white, 2)
    cv2.putText(panel, "Editing: " + selected, (15, 215), FONT, 0.5, gray, 1)
    cv2.putText(panel, "CLAHE: " + ("ON" if use_clahe else "OFF"), (15, 240), FONT, 0.5, gray, 1)

    cv2.putText(panel, "Mask preview", (15, 285), FONT, 0.5, gray, 1)
    preview_w = 150
    preview_h = int(preview_w * mask.shape[0] / mask.shape[1])
    preview = cv2.resize(mask, (preview_w, preview_h))
    preview = cv2.cvtColor(preview, cv2.COLOR_GRAY2BGR)
    panel[295:295 + preview_h, 15:15 + preview_w] = preview

    cv2.putText(panel, "C: switch color  L: CLAHE", (15, 435), FONT, 0.42, gray, 1)
    cv2.putText(panel, "Q / ESC: quit", (15, 455), FONT, 0.42, gray, 1)

    return np.hstack((frame, panel))
