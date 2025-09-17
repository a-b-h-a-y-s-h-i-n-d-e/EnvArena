from google import genai
import os

class GeminiWrapper:

    def __init__(self, 
                 model_name : str = None,
                 temperature : float = None
            ):
        self.model_name = model_name or "gemini-2.5-flash"
        self.temperature = temperature
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        self.client = genai.Client(api_key=self.GEMINI_API_KEY)

    def stream_response(self, prompt: str):
        response = self.client.models.generate_content_stream(
            model=self.model_name,
            contents=prompt
        )

        for chunk in response:
            yield chunk.text