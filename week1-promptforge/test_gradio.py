import gradio as gr
import app

def chat(selected_mode, user_prompt):
    system_prompt = app.PERSONAS[selected_mode]["system_prompt"]
    few_shot_examples = app.PERSONAS[selected_mode]["few_shot_examples"]
    output_format = app.PERSONAS[selected_mode]["output_format"]

    messages = app.build_messages(system_prompt, few_shot_examples, user_prompt)

    response = app.client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = messages,
        stream=True
    )   

    full_response=""
    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            full_response+=content
            yield full_response

demo = gr.Interface(
    fn = chat,
    inputs=[
        gr.Dropdown(
            choices=[
                "Technical Explainer",
                "Debate Coach",
                "Code Reviewer",
                "Creative Writer"
                ],
                label="Choose Mode"
        ),
        gr.Textbox(label="Prompt")
    ],
    outputs="text"
)

demo.launch()