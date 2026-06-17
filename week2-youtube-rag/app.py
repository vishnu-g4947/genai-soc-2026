import gradio as gr

from indexing import get_transcript, create_chunks
from persistence import get_vector_store
from retrieval import get_retriever, answer_question

retriever = None

def index_video(url):
    global retriever
    transcript = get_transcript(url)
    if transcript is None:
        return "Failed to fetch transcript."
    
    chunks = create_chunks(transcript)

    vector_store = get_vector_store(chunks)    

    retriever = get_retriever(vector_store)

    return "Video Indexed Successfully!"

def ask_question(question):
    global retriever

    if retriever is None:
        return "Please index a video first."
    
    answer, docs = answer_question(question, retriever)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return answer, context


with gr.Blocks() as demo:
    gr.Markdown("# 🎥 YouTube RAG Bot")

    video_url = gr.Textbox(label="YouTube URL")

    index_btn = gr.Button("Index Video")

    status = gr.Textbox(label="Status")

    question = gr.Textbox(label="Ask a Question")

    ask_btn = gr.Button("Ask") 

    answer = gr.Textbox(label="Answer")

    index_btn.click(fn = index_video, inputs= video_url, outputs= status)

    context = gr.Textbox(label="Retrieved Context")

    ask_btn.click(fn = ask_question, inputs=question, outputs=[answer, context])

    demo.launch()