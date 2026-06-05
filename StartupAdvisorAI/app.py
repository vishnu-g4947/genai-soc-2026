from groq import Groq
import os
from dotenv import load_dotenv
import personas

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

few_shot_examples = []
history = []

personas_name = list(personas.PERSONAS.keys())

def build_messages(system_prompt, few_shot_examples, history):
        messages = [
            {
                "role":"system",
                "content": system_prompt
            }
        ]
        messages.extend(few_shot_examples)
        messages.extend(history[-10:])

        return messages

if __name__ == "__main__":
    for i,mode in enumerate(personas_name, start=1):
        print(f"{i}. {mode}")

    while True:
        try:
            choice = int(input("Chose One: "))
            if 1<= choice <= len(personas.PERSONAS):
                break
            print("Invalid choice. Try Again")
        except ValueError:
            print("Please enter a number ")


    system_model = personas_name[choice-1]
    system_prompt = personas.PERSONAS[system_model]["system_prompt"]
    few_shot_examples = personas.PERSONAS[system_model]["few_shot_examples"]

    while True:
        user_prompt = input("User: ")

        if user_prompt.lower() == "exit":
            break

        else:
            history.append(
                {
                    "role": "user",
                    "content": user_prompt
                }
            )

            messages = build_messages(system_prompt, few_shot_examples, history)

            print(f"\nTotal messages sent: {len(messages)}")

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                stream=True
            )

            print("Assitant: ")
            assistant_response = ""
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    assistant_response += content
                    print(content, end = "")
            print("\n")
            history.append(
                {
                    "role": "assistant",
                    "content": assistant_response
                }
            )