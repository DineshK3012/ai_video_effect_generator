import google.generativeai as genai
import os
import warnings

# Suppress warnings from google.generativeai about deprecation
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
warnings.filterwarnings("ignore", category=UserWarning, module="google.generativeai")

from dotenv import load_dotenv
from PIL import Image
import io
import numpy as np

load_dotenv()

class GeminiClient:
    def __init__(self, api_key=None, model_name="gemini-nano-banana"):
        """
        Initialize the Gemini Client.
        Args:
            api_key: Optional API key. If not provided, reads from environment.
            model_name: The name of the model to use. Defaults to user's requested 'gemini-nano-banana'.
                        Note: Ensure this model name is valid in your environment or alias it to a valid one like 'gemini-1.5-flash'.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found in environment or arguments.")
        else:
            genai.configure(api_key=self.api_key)
        
        self.model_name = model_name
        self.model = None

    def _ensure_model(self):
        if not self.model:
            if not self.api_key:
                self.api_key = os.getenv("GEMINI_API_KEY")
                if self.api_key:
                    genai.configure(api_key=self.api_key)
                else:
                    raise ValueError("API Key is not set.")
            try:
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"Error initializing model {self.model_name}: {e}")
                print("Falling back to 'gemini-1.5-flash'")
                self.model = genai.GenerativeModel("gemini-1.5-flash")

    def apply_effect_to_frame(self, frame_array, prompt_text):
        """
        Applies an effect to a single frame using Gemini.
        Returns the processed frame or original if failed.
        """
        self._ensure_model()
        
        # Convert numpy array to PIL Image
        img = Image.fromarray(frame_array)
        
        try:
            # Send prompt and image to the model
            response = self.model.generate_content([prompt_text, img])
            
            # Parse response for image data
            processed_image = None
            
            # Check parts for image data (standard for Gemini image output)
            if hasattr(response, 'parts'):
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # Extract header and data if necessary, or just distinct bytes
                        # The library usually simplifies this, but let's handle the raw proto wrapper if needed
                        # part.inline_data.data is the raw bytes
                        img_data = part.inline_data.data
                        processed_image = Image.open(io.BytesIO(img_data))
                        break
            
            # Fallback/Alternative check (some versions/models might behave differently)
            if not processed_image and hasattr(response, 'text'):
                # Just a log, don't crash if it's empty
                try:
                    print(f"  > Text Response: {response.text[:50]}...")
                except Exception:
                    pass

            if processed_image:
                # Convert back to numpy array (RGB)
                # Resize if needed to match original? For now assume model handles or we resize to input
                if processed_image.size != img.size:
                    processed_image = processed_image.resize(img.size)
                
                return np.array(processed_image)
            else:
                print("  > No image data found in response. Returning original frame.")
                return frame_array

        except Exception as e:
            print(f"Error processing frame: {e}")
            return frame_array
