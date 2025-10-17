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
    of what is shown in the frame using the Gemini Flash model.
    """

    print("Processing frame for screen description...")
    try:
        # Convert OpenCV BGR frame to RGB, as PIL and Gemini expect RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        print("Converted frame to PIL image.")

        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            system_instruction=(
                "You are a helpful assistant that analyzes frames from lecture videos. "
                "Describe what is visible on the screen concisely and objectively."
            )
        )

        # Define generation configuration for the model
        generation_config = genai.GenerationConfig(
            max_output_tokens=100,
            temperature=0.1
        )

        # Simpler prompt
        prompt = "Describe what is shown in this image concisely."

        # Generate content using the model without safety settings
        response = model.generate_content(
            [prompt, pil_image],
            generation_config=generation_config
        )

        # Check if response was blocked
        if response.prompt_feedback.block_reason:
            return f"Response blocked: {response.prompt_feedback.block_reason}"

        # Handle cases where response has no text
        if not response.text:
            return "No text generated. Response may have been filtered."

        return response.text.strip()

    except Exception as e:
        print(f"Error processing frame: {e}")
        # Print more detailed error information
        if hasattr(e, 'response'):
            print(f"Response details: {e.response}")
        return f"Error: {str(e)}"


def test_api_connection():
    """
    Test function to verify API key and list available models
    """
    try:
        print("Testing API connection...")
        models = genai.list_models()
        print("\nAvailable Gemini models:")
        for model in models:
            if 'gemini' in model.name.lower() and 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        return True
    except Exception as e:
        print(f"API connection test failed: {e}")
        return False