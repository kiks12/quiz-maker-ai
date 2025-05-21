import ollama
from .regex import QUESTION_ANSWER_PATTERN, INSTRUCTION_PATTERN
import re


class Agent:
    def __init__(self, role, model):
        self.role = role
        self.model = model

    def generate(self, prompt):
        return ollama.generate(
            prompt=prompt,
            system=self.role,
            model=self.model,
            stream=False
        )["response"]


class GemmaAI:
    role = "You are a teacher, you create quizzes"
    model = "gemma3:1b"

    def __init__(self):
        self.agent = Agent(self.role, self.model)

    def create_quiz_type_prompt(self, metadata: dict):
        items_per_type = []

        if "items_per_type" in metadata:
            for (quiz_type, items) in metadata["items_per_type"].items():
                items_per_type.append(f"{quiz_type} with {items} items")

        if len(items_per_type) > 0:
            return f"The quiz should consist of {','.join(items_per_type)}."
        return ""

    def create_prompt(self, text: str, metadata: dict) -> str:
        items_per_type = self.create_quiz_type_prompt(metadata)

        return f'{text} \n\n I need a quiz based on the information above make sure that the questions are all about the text. {items_per_type} This is going to be the format of your response, give the instructions as "INSTRUCTIONS:", new line, then "QUESTION:", new line, new line, "CHOICES:" (if applicable), then "ANSWER:",  new line, new line, then repeat to question.'

    def create_quiz(self, text: str, metadata: dict) -> tuple:
        try:
            prompt = self.create_prompt(text, metadata)
            response = self.agent.generate(prompt)
            print(response)
            formatted_quiz = self.format_quiz(response)

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
