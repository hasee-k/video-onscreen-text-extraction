import cv2
import os
from PIL import Image

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the Gemini API key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=api_key)


def extract_screen_description(frame) -> str:
    """
    Takes a video frame (NumPy array from OpenCV) and returns a concise description
    of what is shown in the frame using the Gemini 1.5 Flash model.
    """
    # Convert OpenCV BGR frame to RGB, as PIL and Gemini expect RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    print("Converted frame to PIL image.")

    # Initialize the Gemini model
    # The system instruction helps set the context for the model's responses
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=(
            "You are a helpful assistant that is given frames from a lecture video. "
            "You help identify what's on the screen so the student knows when to rewatch the lecture. "
            "You should concisely describe what is on the screen."
        )
    )

    # Define generation configuration for the model
    generation_config = genai.types.GenerationConfig(
        max_output_tokens=50,
        temperature=0.0
    )

    # The prompt now includes the text and the PIL image object directly
    prompt_parts = [
        "Describe what is shown in this image concisely.",
        pil_image,
    ]

    # Generate content using the model
    response = model.generate_content(
        prompt_parts,
        generation_config=generation_config
    )

    return response.text