# Real-Time Color Detection Dashboard

A real-time computer vision project built with Python, OpenCV and NumPy. It detects red and green objects from a webcam, tracks them with persistent IDs, and shows the results in a modern dashboard with live HSV sliders.

No pretrained AI models are used. All detection is classical computer vision.

## Features

- Accurate red and green detection with HSV color segmentation
- Correct handling of red's hue wrap-around (0 and 179)
- Separate detection of pure red and orange, and of deep green and gray or black
- Real-time adjustable HSV sliders
- Centroid-based object tracking with IDs and movement trails
- Color names and object counts on the video and on the dashboard
- Dark side-panel dashboard with FPS, counts and live mask preview
- Optimized for real-time use (threaded camera, half-size processing)

## Project Structure

```
color_detection/
├── main.py            Main loop that connects everything
├── config.py          All settings and default HSV ranges
├── camera.py          Threaded webcam reader
├── detector.py        Preprocessing, color masks, object finding
├── tracker.py         Centroid tracker (IDs and trails)
├── gui.py             Sliders, drawing, dashboard
└── requirements.txt   Dependencies
```

## Installation

1. Install Python 3.8 or newer.
2. Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

```
python main.py
```

Two windows open: the dashboard and the HSV Controls window.

### Keyboard controls

| Key | Action |
|---|---|
| `C` | Switch which color the sliders edit (red / green) |
| `L` | Turn CLAHE brightness normalization on or off |
| `Q` or `ESC` | Quit |

## How It Works

1. **Capture.** `camera.py` reads frames in a background thread so processing always uses the newest frame.
2. **Preprocess.** The frame is shrunk to half size, blurred, and converted to HSV. Optionally CLAHE evens out brightness on the V channel.
3. **Mask.** `cv2.inRange` keeps only pixels inside the color's HSV range. Red uses two ranges, one near hue 0 and a mirrored one near hue 179.
4. **Clean.** Morphological opening removes specks, and closing fills holes.
5. **Find objects.** Contours are filtered by minimum area and fill ratio, then converted to bounding boxes at full resolution.
6. **Track.** Each detection is matched to the nearest previous object of the same color, or gets a new ID.
7. **Display.** Boxes, labels, trails and the dashboard are drawn and shown.

## HSV Sliders

| Slider | Meaning | Range |
|---|---|---|
| `h_min`, `h_max` | Hue (the color itself) | 0 to 179 |
| `s_min`, `s_max` | Saturation (how vivid) | 0 to 255 |
| `v_min`, `v_max` | Value (how bright) | 0 to 255 |

For red, the sliders set the lower hue band, and the upper band (near 179) is mirrored automatically.

### Tuning guide

1. Press `C` to choose a color.
2. Watch the mask preview on the dashboard while moving the sliders.
3. Your object should be solid white and the background black.

Common fixes:

- Dark green is missed: lower `v_min`.
- Red is missed: lower `s_min`.
- Orange or pink is detected as red: narrow the hue range or raise `s_min`.
- One object is split into several boxes: increase `MORPH_KERNEL_SIZE` in `config.py`.
- Small noise is detected: increase `MIN_AREA` in `config.py`.

## Configuration (`config.py`)

| Setting | Purpose |
|---|---|
| `CAMERA_INDEX` | Which webcam to use (0 is the default camera) |
| `FRAME_WIDTH`, `FRAME_HEIGHT` | Capture resolution |
| `PROCESS_SCALE` | Detection resolution factor (0.5 is faster, 1.0 is more precise) |
| `BLUR_SIZE` | Gaussian blur kernel size (odd number) |
| `MORPH_KERNEL_SIZE` | Mask cleanup strength |
| `USE_CLAHE` | Brightness normalization at startup |
| `MIN_AREA` | Smallest object size in pixels |
| `MIN_FILL_RATIO` | Minimum fraction of the box the object must fill |
| `MAX_TRACK_DISTANCE` | Maximum pixel distance to match an object between frames |
| `MAX_DISAPPEARED` | Frames an object may vanish before its ID is dropped |
| `TRAIL_LENGTH` | Length of the movement trail |
| `COLORS` | HSV ranges and drawing color for each detected color |

## Adding a New Color

Add an entry to `COLORS` in `config.py`. Everything else (sliders, tracking, dashboard) picks it up automatically.

```python
"blue": {
    "h_min": 95, "h_max": 130,
    "s_min": 100, "s_max": 255,
    "v_min": 50, "v_max": 255,
    "box": (255, 0, 0),
    "wrap": False,
},
```

Set `"wrap": True` only for colors that cross the hue boundary, such as red.

## Troubleshooting

- **"Could not open the webcam":** try `CAMERA_INDEX = 1` in `config.py`, and close other apps using the camera.
- **Low FPS:** lower `PROCESS_SCALE` (for example 0.4) or lower the camera resolution.
- **Colors unstable in dim light:** keep CLAHE on, and light the scene more evenly.
- **Sliders not visible:** the HSV Controls window may be behind the dashboard, so drag the dashboard aside.

## Possible Future Improvements

- Save and load slider values (JSON)
- More colors (blue, yellow, orange)
- Better tracking with Kalman filters
- Record video with the overlay
- Speed or direction estimation for tracked objects

## Tech Stack

Python, OpenCV, NumPy
