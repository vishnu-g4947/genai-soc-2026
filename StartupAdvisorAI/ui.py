import app
import gradio as gr
import personas

def chat(system_model, user_prompt):

    system_prompt = personas.PERSONAS[system_model]["system_prompt"]
    few_shot_examples = personas.PERSONAS[system_model]["few_shot_examples"]

    messages = app.build_messages(
        system_prompt,
        few_shot_examples,
        [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    response = app.client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True
    )

    full_response = ""

    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            full_response += content
            yield full_response


demo = gr.Interface(
    fn=chat,
    inputs=[
        gr.Dropdown(
            choices=list(personas.PERSONAS.keys()),
            label="Choose Persona"
        ),
        gr.Textbox(
            label="Prompt"
        )
    ],
    outputs="text",
    title="Startup Advisor AI",
    description="Choose an advisor and ask your startup-related questions."
)

demo.launch()