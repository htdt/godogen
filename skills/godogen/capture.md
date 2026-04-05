# Godot Capture

Screenshot and video capture for Godot projects. Supports Windows, macOS (Metal), and Linux (X11/xvfb + optional GPU).

The Godot project is the working directory. All paths below are relative to it.

Tools live at `${CLAUDE_SKILL_DIR}/tools/`. Run from the project root.

## Setup

No setup is required. The `capture.py` script automatically detects the platform, GPU availability, and handles timeout settings. It manages appropriate platform-specific Godot arguments (such as using xvfb on Linux headless environments or forward_plus on Windows/macOS/Linux with GPU).

## Screenshot Capture

Screenshots go in `screenshots/` (gitignored). Each task gets a subfolder.

```bash
python ${CLAUDE_SKILL_DIR}/tools/capture.py --task {task_folder} --fps {FPS} --frames {N} --script test/test_task.gd
```

Where `{task_folder}` is derived from the task name/number (e.g., `task_01_terrain`). Use lowercase with underscores. The tool manages timeouts inherently.

### Frame Rate and Duration

`--frames {N}` is the frame count. Choose based on scene type:
- **Static scenes** (decoration, terrain, UI): `--fps 1`. Adjust `--frames` for however many views needed (e.g. 8 frames for a camera orbit).
- **Dynamic scenes** (physics, movement, gameplay): `--fps 10`. Low FPS breaks physics — `delta` becomes too large, causing tunneling and erratic behavior. Typical: 3-10s (30-100 frames).

## Video Capture

Video capture requires hardware rendering (Windows natively, macOS Metal, or Linux with GPU). Software rendering is too slow for video — the tool skips and reports if GPU is unavailable.

```bash
python ${CLAUDE_SKILL_DIR}/tools/capture.py --video --task presentation --fps 30 --frames 900 --script test/presentation.gd
```

The script will automatically handle capturing to AVI and converting to H.264 MP4 with ffmpeg (scale to 1280px max width, +faststart). The resulting file will be located at `screenshots/presentation/gameplay.mp4`.