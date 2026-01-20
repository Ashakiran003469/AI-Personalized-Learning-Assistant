def get_ai_answer(level: str, subject: str, question: str) -> str:
    level = level.lower()
    subject = subject.lower()
    question = question.lower()

    # -------------------------------
    # MATH
    # -------------------------------
    if subject == "math":
        if "multiplication" in question:
            return (
                "Multiplication means adding the same number many times.\n\n"
                "Example:\n"
                "3 × 4 = 12\n"
                "This means adding 3 four times:\n"
                "3 + 3 + 3 + 3 = 12\n\n"
                "Multiplication helps us solve problems faster."
            )

        if "addition" in question:
            return (
                "Addition means combining numbers to find their total.\n\n"
                "Example:\n"
                "5 + 2 = 7\n"
                "This means you have 5 items and add 2 more."
            )

        if "subtraction" in question:
            return (
                "Subtraction means taking away a number from another.\n\n"
                "Example:\n"
                "10 − 4 = 6\n"
                "This means removing 4 from 10."
            )

        return (
            "This is a math question. To solve math problems:\n"
            "1. Understand the question\n"
            "2. Identify the numbers\n"
            "3. Apply the correct operation\n"
            "4. Solve step-by-step"
        )

    # -------------------------------
    # SCIENCE
    # -------------------------------
    if subject == "science":
        if "photosynthesis" in question:
            return (
                "Photosynthesis is the process by which plants make their food.\n\n"
                "Plants use:\n"
                "- Sunlight\n"
                "- Water\n"
                "- Carbon dioxide\n\n"
                "They produce food and oxygen."
            )

        return (
            "Science helps us understand how the world works.\n"
            "Try to observe, ask questions, and learn through experiments."
        )

    # -------------------------------
    # ENGLISH
    # -------------------------------
    if subject == "english":
        if "noun" in question:
            return (
                "A noun is the name of a person, place, animal, or thing.\n\n"
                "Examples:\n"
                "- Person: teacher\n"
                "- Place: school\n"
                "- Thing: book"
            )

        return (
            "English helps us communicate clearly using words, sentences, and grammar."
        )

    # -------------------------------
    # DEFAULT
    # -------------------------------
    return (
        "This question is interesting.\n"
        "Think carefully, break it into parts, and try to understand the concept."
    )
