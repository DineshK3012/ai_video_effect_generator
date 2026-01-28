import cv2
import os

# Suppress annoying OpenCV/FFMPEG logs
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
try:
    if hasattr(cv2, 'setLogLevel'):
        cv2.setLogLevel(0)  # 0 = Silent
except Exception:
    pass

def read_video_frames(video_path, target_fps=None):
    """
    Reads a video and yields frames.
    Args:
        video_path: Path to the video file.
        target_fps: Optional. If set, extracts frames at this rate (e.g., 1 for 1 frame per second).
    Returns:
        List of frames (numpy arrays in RGB format).
        fps (float): Frames per second of the returned list (either source fps or target_fps).
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {video_path}")
    
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    
    # Calculate step size
    step = 1
    return_fps = original_fps
    
    if target_fps:
        if target_fps > original_fps:
             print(f"Warning: Target FPS {target_fps} is higher than video FPS {original_fps}. capturing all frames.")
        else:
            step = int(round(original_fps / target_fps))
            step = max(1, step)
            return_fps = target_fps
            print(f"Extracting 1 frame every {step} frames (Target FPS: {target_fps})")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % step == 0:
            # OpenCV reads in BGR, convert to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
        
        frame_count += 1
    
    cap.release()
    return frames, return_fps

def create_video_from_frames(frames, output_path, fps=30.0):
    """
    Creates a video from a list of frames.
    Args:
        frames: List of numpy arrays (RGB).
        output_path: Path to save the video.
        fps: Frames per second.
    """
    if not frames:
        print("No frames to write.")
        return

    height, width, layers = frames[0].shape
    size = (width, height)
    
    # Select Best Available Codec
    # Browsers prefer 'avc1' (H.264) or 'vp09' (VP9).
    # 'mp4v' is the standard fallback for OpenCV on Windows but may not play in all browsers.
    codecs_to_try = [
        ('avc1', 'H.264'),
        ('vp09', 'VP9'),
        ('mp4v', 'MPEG-4')
    ]

    out = None
    selected_codec = None

    for codec, name in codecs_to_try:
        try:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            temp_out = cv2.VideoWriter(output_path, fourcc, fps, size)
            if temp_out.isOpened():
                out = temp_out
                selected_codec = name
                print(f"Initialized VideoWriter with codec: {name} ('{codec}')")
                break
        except Exception as e:
            print(f"Failed to check codec {codec}: {e}")
            continue

    if not out:
        print("Error: Failed to initialize any video writer. Output video will not be saved.")
        return

    for frame in frames:
        # Convert RGB back to BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
    
    out.release()
    print(f"Video saved to {output_path}")
