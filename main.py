import time
import cv2
import config
import detector
import gui
from camera import CameraStream
from tracker import CentroidTracker


def main():
    camera = CameraStream()
    if not camera.is_opened():
        print("Could not open the webcam. Check config.CAMERA_INDEX.")
        return

    tracker = CentroidTracker()
    names = list(config.COLORS.keys())
    selected = 0
    use_clahe = config.USE_CLAHE
    fps = 0.0
    last_time = time.time()

    gui.create_sliders(names[selected])

    while True:
        ok, frame = camera.read()
        if not ok:
            time.sleep(0.01)
            continue

        if frame.shape[1] != config.FRAME_WIDTH or frame.shape[0] != config.FRAME_HEIGHT:
            frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
        frame = cv2.flip(frame, 1)

        gui.read_sliders(names[selected])

        hsv = detector.preprocess(frame, use_clahe)

        detections = []
        masks = {}
        for name in names:
            mask = detector.build_mask(hsv, config.COLORS[name])
            mask = detector.clean_mask(mask)
            masks[name] = mask
            detections += detector.find_objects(mask, name)

        tracker.update(detections)
        gui.draw_detections(frame, detections, tracker)

        counts = {}
        for name in names:
            counts[name] = sum(1 for d in detections if d["color"] == name)

        now = time.time()
        fps = 0.9 * fps + 0.1 * (1.0 / max(now - last_time, 1e-6))
        last_time = now

        dashboard = gui.build_dashboard(
            frame, counts, tracker.total_seen, fps,
            names[selected], masks[names[selected]], use_clahe,
        )
        cv2.imshow("Color Detection Dashboard", dashboard)
        gui.show_slider_banner(names[selected])

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break
        if key == ord("c"):
            selected = (selected + 1) % len(names)
            gui.load_sliders(names[selected])
        if key == ord("l"):
            use_clahe = not use_clahe

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
