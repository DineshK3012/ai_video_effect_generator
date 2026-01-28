# Video Effects Project - Mixed Media Collage

This project uses Google's Gemini Models (specifically the "Nano Banana" familiy) to apply complex, frame-by-frame video effects to input videos. It allows you to transform standard videos into mixed-media collages using AI.

## Features

*   **AI-Powered Effects**: Uses Gemini 3 Pro ("Nano Banana Pro") for high-quality image manipulation.
*   **Prompt Engineering**: Uses a modular prompt system to apply styles like "paper cutout," "scribbles," and "mixed media."
*   **Web Interface**: Simple Streamlit frontend to upload, process, and preview videos.
*   **Customizable FPS**: Option to process at lower frame rates (e.g., 1 FPS) for rapid prototyping and artistic stop-motion looks.

## Prerequisites

1.  **API Key**:
    *   Get a Google Gemini API Key.
    *   Open (or create) the `.env` file in the root directory.
    *   Add your key: `GEMINI_API_KEY=your_actual_api_key_here`

2.  **Environment**:
    *   Python 3.8+ installed.

## Installation

1.  **Create and Activate Virtual Environment**:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Web Interface (Recommended)
The easiest way to use the tool is via the Streamlit web app.

```bash
python -m streamlit run app.py
```
*   Allows you to **Upload** any `.mp4`, `.mov`, or `.avi` file.
*   Adjust **Target FPS** using the slider (1 FPS is recommended for testing).
*   **Edit Prompt** directly in the sidebar to change the artistic effects.
*   **Preview & Download** the result immediately in the browser.
*   *Note: If the terminal says "Command not found" for streamlit, try `.\venv\Scripts\streamlit run app.py`.*

### 2. Command Line Interface
You can also run the processing script directly from the terminal.

1.  Place a video file (e.g., `input.mp4`) in the project root.
2.  Run:
    ```bash
    python main.py input.mp4
    ```
3.  The output will be saved as `output.mp4`.

## Configuration

*   **Model Selection**: The system defaults to **Gemini 3 Pro Image Preview** via the `src/model_registry.py`. You can modify this file to switch between "Flash" (faster) and "Pro" (better quality) models.
*   **Prompts**: The default prompt is located in `prompts/collage_prompt.txt`.

## Troubleshooting

*   **Browser Preview Issues**: If the generated video doesn't play in the browser, ensure your system supports H.264 encoding. The script attempts to use the `avc1` codec.
*   **API Errors**: If you encounter 404s or quota limits, check your API key status and limits in the Google AI Studio dashboard.
