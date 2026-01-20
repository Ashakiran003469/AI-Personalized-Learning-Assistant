from typing import Dict, Any, Optional
import uuid
import re


class SimpleAIAgent:
    """
    Rule-based AI Agent that answers educational questions
    without external APIs or LLM keys.
    """

    def __init__(self, storage=None):
        self.storage = storage

    async def handle_message(
        self,
        session_id: Optional[str],
        user_id: Optional[str],
        message: str,
        language: Optional[str] = "en"
    ) -> Dict[str, Any]:

        session_id = session_id or str(uuid.uuid4())

        intent = self.detect_intent(message)
        topic = self.detect_topic(message)
        response = self.generate_answer(message, topic)

        return {
            "session_id": session_id,
            "response": {
                "text": response
            },
            "intent": intent,
            "topic": topic,
            "next_action": "ask_next_question"
        }

    # -----------------------------
    # INTENT DETECTION
    # -----------------------------
    def detect_intent(self, message: str) -> str:
        message = message.lower()
        if any(word in message for word in ["why", "how", "explain"]):
            return "concept_explanation"
        if any(word in message for word in ["define", "what is"]):
            return "definition"
        if any(word in message for word in ["solve", "calculate"]):
            return "problem_solving"
        return "general_question"

    # -----------------------------
    # SUBJECT / TOPIC DETECTION
    # -----------------------------
    def detect_topic(self, message: str) -> str:
        message = message.lower()
        if any(word in message for word in ["photosynthesis", "cell", "biology"]):
            return "Biology"
        if any(word in message for word in ["algebra", "equation", "math"]):
            return "Mathematics"
        if any(word in message for word in ["atom", "chemical", "chemistry"]):
            return "Chemistry"
        if any(word in message for word in ["history", "war", "freedom"]):
            return "Social Studies"
        if any(word in message for word in ["grammar", "noun", "english"]):
            return "English"
        return "General Knowledge"

    # -----------------------------
    # ANSWER GENERATION (CORE AI)
    # -----------------------------
    def generate_answer(self, question: str, topic: str) -> str:
        question_lower = question.lower()

        if "why is the sky blue" in question_lower:
            return (
                "The sky appears blue because of a process called Rayleigh scattering. "
                "Sunlight contains all colors, but blue light is scattered more by air "
                "molecules in the atmosphere, making the sky look blue."
            )

        if topic == "Biology":
            return (
                "In biology, this concept relates to how living organisms function. "
                "Let me explain it step by step in a simple way so it is easy to understand."
            )

        if topic == "Mathematics":
            return (
                "In mathematics, problems are solved using logical steps and formulas. "
                "First, understand the question, then apply the correct method to reach the solution."
            )

        if topic == "Chemistry":
            return (
                "Chemistry explains how substances interact with each other. "
                "This concept is based on reactions between atoms and molecules."
            )

        if topic == "English":
            return (
                "In English, this topic focuses on language structure, meaning, and usage. "
                "I can explain it with examples to make it clear."
            )

        if topic == "Social Studies":
            return (
                "Social Studies helps us understand society, history, and human behavior. "
                "This topic explains how past events influence the present."
            )

        return (
            "That is an interesting question. Let me explain it clearly in simple terms. "
            "If you want, you can ask a follow-up question for deeper understanding."
        )
