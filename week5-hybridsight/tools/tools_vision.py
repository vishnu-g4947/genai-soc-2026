import os 
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.tools import tool
from tools import shared_state

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

vision_model = genai.GenerativeModel(
    model_name= 'gemini-2.5-flash'
)

@tool
def describe_image(question: str) -> str:
    """
    Analyze the uploaded image and answer the user's question.

    Use this tool whenever the user asks about an uploaded image,
    requests a description, wants to identify objects, extract
    information, or understand the contents of the image.

    Examples:

    - "What is in this image?"
    - "Describe the uploaded photo"
    - "What objects can you see?"
    - "Extract the text from this image"
    - "Explain this diagram"

    Do not use this tool for PDF-related questions,
    general knowledge, or web searches.

    Args:
        question: The user's question about the uploaded image.

    Returns:
        A description or answer based on the uploaded image.
    """
    image_path = shared_state.CURRENT_IMAGE_PATH
    
    if image_path is None:
        return "No image has been uploaded yet."
    
    response = vision_model.generate_content(
        [
            question,
            {
                'mime_type': 'image/jpeg',
                'data': open(image_path, 'rb').read()
            }
        ]
    )
    
    return response.text