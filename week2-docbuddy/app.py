import gradio as gr
from indexing import index_documents
from retrieval import ask

def index_files(files):
    pdf_paths = []

    for file in files:
        pdf_paths.append(file.name)
    total_chunks = index_documents(pdf_paths)
    return f"Indexed {len(files)} documents and created {total_chunks} chunks."

with gr.Blocks() as demo:
    gr.Markdown("# DocBuddy Pro")

    file_upload = gr.File(
        file_count="multiple",
        file_types=[".pdf"]
    )

    index_button = gr.Button("Index Documents")

    status_label = gr.Textbox(
        label = "Status"
    )

    chatbot = gr.Textbox(
        label = "Conversation"
    )

    question_box = gr.Textbox(
        label = "Ask Question"
    )

    with gr.Accordion(
        "🔍 Retrieved Context",
        open=False
    ):
        context_display = gr.Markdown()

    index_button.click(
        fn = index_files,
        inputs=file_upload,
        outputs=status_label
    )

    question_box.submit(
        fn = ask, 
        inputs= question_box,
        outputs=[chatbot, context_display]
    )

demo.launch()