import streamlit as st
import os
import tempfile
import time
from src.video_utils import read_video_frames, create_video_from_frames
from src.gemini_client import GeminiClient
from src.prompt_manager import PromptManager
from src.model_registry import ModelRegistry

# Page Config
st.set_page_config(page_title="Video Effects with Gemini", layout="centered")

def process_video(input_path, output_path, prompt, target_fps=1):
    """
    Orchestrates the video processing.
    """
    # Use st.status for a nice loader/status container
    with st.status("Starting video generation...", expanded=True) as status:
        
        # 1. Read Frames
        st.write("Reading video frames...")
        try:
            frames, fps = read_video_frames(input_path, target_fps=target_fps)
            st.write(f"Extracted {len(frames)} frames. Output FPS: {fps}")
        except Exception as e:
            st.error(f"Error reading video: {e}")
            status.update(label="Failed", state="error")
            return False

        # 2. Init Client
        st.write("Initializing Gemini Nano Banana Model...")
        model_name = ModelRegistry.get_best_model()
        client = GeminiClient(model_name=model_name)

        # 3. Process Loops
        processed_frames = []
        total_frames = len(frames)
        
        # Create a progress bar inside the status or outside? 
        # Usually outside is better for visibility, but inside keeps it contained.
        # Let's put it inside.
        progress_bar = st.progress(0)
        
        for i, frame in enumerate(frames):
            # Update the status label to show liveliness
            status.update(label=f"Processing frame {i+1}/{total_frames} with AI Effect...")
            
            new_frame = client.apply_effect_to_frame(frame, prompt)
            processed_frames.append(new_frame)
            
            # Update progress
            progress_bar.progress((i + 1) / total_frames)

        # 4. Save Video
        st.write("Reassembling video frames...")
        create_video_from_frames(processed_frames, output_path, fps=fps)
        
        status.update(label="Video Generation Complete!", state="complete", expanded=False)
    
    return True

def main():
    st.title("✨ AI Video Effects Generator")
    st.markdown("Upload a video, apply Gemini Nano Banana effects, and download the result.")

    # Sidebar Config
    with st.sidebar:
        st.header("Settings")
        target_fps = st.slider("Process FPS (Lower = Faster)", min_value=1, max_value=30, value=1)
        
        prompt_file = "prompts/collage_prompt.txt"
        if os.path.exists(prompt_file):
            with open(prompt_file, 'r') as f:
                default_prompt = f.read()
        else:
            default_prompt = "Apply creative effects."
            
        custom_prompt = st.text_area("Edit Prompt", value=default_prompt, height=200)

    # File Uploader
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        # Display Input Video
        st.subheader("Input Video")
        st.video(uploaded_file)
        
        if st.button("Apply Magic ✨", type="primary"):
            # Create temp files
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') 
            tfile.write(uploaded_file.read())
            input_path = tfile.name
            tfile.close() # Close so other process can read it

            output_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            output_path = output_temp.name
            output_temp.close()

            try:
                # Run Processing
                success = process_video(input_path, output_path, custom_prompt, target_fps=target_fps)
                
                if success:
                    st.divider()
                    st.markdown("### ✨ Magic Result")
                    
                    st.video(output_path)
                    
                    st.divider()
                    
                    with open(output_path, 'rb') as f:
                        video_bytes = f.read()
                        
                    st.download_button(
                        label="⬇️ Download Processed Video",
                        data=video_bytes,
                        file_name="processed_video.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
            finally:
                # Cleanup
                if os.path.exists(input_path):
                    os.unlink(input_path)
                # We don't delete output_path immediately so user can download, 
                # but OS temp cleaner will handle eventually or we could rely on Streamlit session state.
                # For this minimal app, leaving it in temp is fine.

if __name__ == "__main__":
    main()
