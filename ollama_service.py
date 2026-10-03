import ollama


class OllamaService:

    def __init__(self, model="phi4-mini"):
        self.model = model

    def check_connection(self):
        try:
            ollama.list()
            return True, "Ollama is connected"
        except Exception as e:
            return False, str(e)

    def get_models(self):
        try:
            response = ollama.list()

            models = []

            for model in response.models:
                models.append(model.model)

            return models

        except Exception:
            return []

    def chat(self, messages, temperature=0.7):

        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature
            },
            stream=True
        )

        for chunk in response:
            if chunk.message and chunk.message.content:
                yield chunk.message.content