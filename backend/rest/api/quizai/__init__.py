from ollama import chat
from ollama import ChatResponse
from .regex import QUESTION_ANSWER_PATTERN, INSTRUCTION_PATTERN
import re


class GemmaAI:
    model = "gemma3:1b"
    role = "user"

    def __init__(self):
        pass

    def create_prompt(self, text: str, metadata: dict) -> str:
        items_per_type = []
        if "items_per_type" in metadata:
            for (quiz_type, items) in metadata["items_per_type"].items():
                items_per_type.append(f"{quiz_type} with {items} items")

        return f'{text} \n\n I need a quiz based on the information above make sure that the questions are all about the text. The quiz should consist of {", ".join(items_per_type)}.  This is going to be the format of your response, give the instructions as "INSTRUCTIONS:", new line, then "QUESTION:" followed by its "ANSWER:" then repeat it. Do not ask about the goal of the text or something similar make sure that the questions are all about the data inside the text but do not refer to the "Text" as "Text".'

    def create_quiz(self, text: str, metadata: dict) -> tuple:
        try:
            prompt = self.create_prompt(text, metadata)
            response: ChatResponse = chat(model=self.model, messages=[
                {
                    'role': self.role,
                    'content': prompt,
                },
            ])
            print(response.message.content)
            formatted_quiz = self.format_quiz(response.message.content)

            return (prompt, formatted_quiz)
        except Exception as e:
            print(e)
            return ("No Prompt", "No Created quiz")

    def format_quiz(self, text: str) -> dict:
        instructions = self.get_instructions(text)
        questions = self.get_question_answer_pairs(text)

        return {
            "instructions": instructions,
            "questions": questions,
        }

    def get_question_answer_pairs(self, text: str) -> list:
        question_answers = []
        matches = re.findall(QUESTION_ANSWER_PATTERN, text, re.DOTALL)

        if not matches:
            return question_answers

        for index, (question, answer) in enumerate(matches, 1):
            qna = {}
            qna["number"] = index
            qna["question"] = question.strip()
            qna["answer"] = answer.strip() if answer else "No Answer"
            question_answers.append(qna)

        return question_answers

    def get_instructions(self, text: str) -> str:
        instructions = re.search(INSTRUCTION_PATTERN, text)
        return instructions.group() if instructions else "No Instructions Found"
