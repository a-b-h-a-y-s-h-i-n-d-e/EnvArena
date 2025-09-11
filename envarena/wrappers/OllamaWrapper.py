from ollama import chat

class OllamaWrapper:

    def __init__(self, 
                 model_name: str, 
                 temperature: float = None
        ):
        self.model_name = model_name
        self.temperature = temperature
    

    def stream_response(self, prompt: str):
        """Yield streaming chunks of the model's response."""
        stream = chat(
            model=self.model_name,
            messages=[{
                'role': 'user',
                'content': prompt,
            }],
            stream=True
        )

        for chunk in stream:
            yield chunk['message']['content']