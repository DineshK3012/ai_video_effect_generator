import os
import sys
from src.video_utils import read_video_frames, create_video_from_frames
from src.gemini_client import GeminiClient
from src.prompt_manager import PromptManager
from src.model_registry import ModelRegistry

def main():
    # Configuration
    input_video_path = "input.mp4" 
    output_video_path = "output.mp4"
    # Use the new prompt template
    prompt_file = "prompts/collage_prompt.txt"
    
    # Allow command line argument for input video
    if len(sys.argv) > 1:
        input_video_path = sys.argv[1]
    
    if not os.path.exists(input_video_path):
        print(f"Input video not found: {input_video_path}")
        print("Usage: python main.py <path_to_video>")
        return

    # 1. Load Prompt using PromptManager
    prompt_manager = PromptManager(prompt_file)
    # If the template had variables (e.g. {color}), we would pass them here: 
    # prompt = prompt_manager.get_prompt(color="blue")
    prompt = prompt_manager.get_prompt()
    
    print(f"Using Prompt:\n---\n{prompt[:100]}...\n---")

    print(f"Starting processing for {input_video_path}...")
    
    # 2. Read Frames
    try:
        # Extract at 1 FPS as requested
        frames, fps = read_video_frames(input_video_path, target_fps=1)
        print(f"Extracted {len(frames)} frames. Processing Video FPS at: {fps}")
    except Exception as e:
        print(f"Error reading video: {e}")
        return

    # 3. Initialize Gemini Client
    # Usign ModelRegistry to select the best "Nano Banana" model (Pro)
    model_name = ModelRegistry.get_best_model()
    
    client = GeminiClient(model_name=model_name)
    
    # 4. Process Frames
    processed_frames = []
    print("Applying effects to frames (this may take a while)...")
    
    # Limit to 30 frames for testing if input is long to avoid hitting quotas quickly
    max_frames_to_process = min(len(frames), 60)
    
    for i in range(max_frames_to_process):
        frame = frames[i]
        
        # Progress log
        if i % 5 == 0:
            print(f"Processing frame {i+1}/{max_frames_to_process}")
        
        # Apply effect
        new_frame = client.apply_effect_to_frame(frame, prompt)
        processed_frames.append(new_frame)

    # 5. Save Video
    create_video_from_frames(processed_frames, output_video_path, fps=fps)
    print(f"Processing complete. Output saved to {output_video_path}")

if __name__ == "__main__":
    main()
