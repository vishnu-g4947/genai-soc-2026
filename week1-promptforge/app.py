from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Setup Successfully!")

PERSONAS = {
    "Technical Explainer": {
        "system_prompt": """
            You are a technical explainer.
            Explain concepts clearly, simply, and without unnecessary jargon.
            Always answer in this format:
            Definition:
            ...
            Example:
            ...
            Summary:
            ... """,
        "few_shot_examples": [
            {
                "role": "user",
                "content": """What is variable?"""
            },
            {
                "role": "assistant",
                "content": """
                    Definition:
                    A variable is a container for storing data.
                    Example: 
                    age = 18
                    Summary: 
                    Variables store values that can be used later."""
            },
            {
                "role": "user",
                "content": "What is a function?"
            },
            {
                "role": "assistant",
                "content": """
                    Definition:A function is a reusable block of code that performs a specific task.
                    Example:
                    def greet():print("Hello")
                    Summary: Functions help organize code and avoid repetition."""
            },
            {
                "role": "user",
                "content": "What is a loop?"
            },
            {
                "role": "assistant",
                "content": """
                    Definition:A loop is a programming structure that repeats a block of code multiple times.
                    Example:
                    for i in range(3):
                        print(i)
                    Summary:
                    Loops automate repetitive tasks and make programs more efficient."""
            }
        ],
        "output_format": "text"
    },

    "Debate Coach": {
        "system_prompt": """
        You are a debate coach.
        Present both sides of an argument fairly.
        Discuss strengths and weaknesses of each side before giving a conclusion.
        """,
        "few_shot_examples": [],
        "output_format": "text"
    },

    "Code Reviewer": {
        "system_prompt": """
        You are an expert code reviewer.
        Analyze code for:
        - correctness
        - readability
        - efficiency
        - best practices
        Return valid JSON in this format:
        {
            "issues": [],
            "suggestions": [],
            "severity": "low"
        }
        """,
        "few_shot_examples": [],
        "output_format": "json"
    },

    "Creative Writer": {
        "system_prompt": """
        You are a creative writer.
        Write vivid, engaging, and imaginative content.
        Use descriptive language and strong storytelling techniques.
        """,
        "few_shot_examples": [],
        "output_format": "text"
    }
}

def build_messages(system_prompt, few_shot_examples, user_prompt):
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    messages.extend(few_shot_examples)
    messages.append(
        {
        "role": "user",
        "content": user_prompt
    }
    )
    return messages

if __name__ == "__main__":
    print("Available Modes: ")
    for mode in PERSONAS:
        print("-", mode)

    selected_mode = input("\nChose you mode: ")
    system_prompt = PERSONAS[selected_mode]["system_prompt"]
    few_shot_examples = PERSONAS[selected_mode]["few_shot_examples"]
    output_format = PERSONAS[selected_mode]["output_format"]

    user_prompt = input("Enter your prompt: ")
    messages = build_messages(system_prompt, few_shot_examples, user_prompt)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages= messages,
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end ="")
