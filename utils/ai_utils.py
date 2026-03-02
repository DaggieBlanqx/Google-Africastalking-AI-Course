import os
import time
from dotenv import load_dotenv
from google import genai
from google.api_core.exceptions import GoogleAPIError

# Load environment variables from .env
load_dotenv()

# Setup Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment")

client = genai.Client(api_key=GEMINI_API_KEY)

# Default model (can override in function calls)
DEFAULT_MODEL = os.getenv("MODEL_ID", "gemini-2.5-flash")


def _call_gemini(prompt: str, model: str, retries: int = 3, delay: float = 2.0):
    """
    Internal helper to call Gemini with retry logic.
    Retries on network or API errors.
    """
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            raise ValueError("Empty response from Gemini")

        except (GoogleAPIError, ValueError, Exception) as e:
            last_error = e
            print(f"⚠️ Gemini call failed (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(delay * attempt)  # exponential backoff

    raise RuntimeError(f"Gemini request failed after {retries} retries: {last_error}")


def ask_gemini(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Ask Gemini a question and return plain text.
    """
    return _call_gemini(prompt, model)


def ask_gemini_as_xml(
    prompt: str, model: str = DEFAULT_MODEL, root_tag: str = "Response"
) -> str:
    """
    Ask Gemini and wrap the response inside an XML response.
    Useful for USSD/Voice APIs.
    """
    text = _call_gemini(prompt, model)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<{root_tag}>\n  <Say>{text}</Say>\n</{root_tag}>'
    return xml


def ask_gemini_structured(
    prompt: str, model: str = DEFAULT_MODEL, output_format: str = "json"
) -> str:
    """
    Ask Gemini and request a structured response.
    Output format can be 'json', 'xml', or any custom instruction.
    """
    structured_prompt = f"Respond in {output_format.upper()} format only. {prompt}"
    return _call_gemini(structured_prompt, model)
