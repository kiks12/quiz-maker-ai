from ollama import chat
from ollama import ChatResponse


class GemmaAI:
    model = "gemma3:1b"
    role = "user"

    def __init__(self):
        pass

    def create_quiz(self, text: str):
        try:
            response: ChatResponse = chat(model=self.model, messages=[
                {
                    'role': self.role,
                    'content': f'This is the information \n {text} \n I need a quiz based on the information above make sure that the questions are about the information.  This is going to be the format of your response, no preliminary statements, give instruction, question then answer then repeat',
                },
            ])

            return response.message.content
        except Exception:
            return ""
