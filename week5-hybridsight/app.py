import streamlit as st
import uuid

from langchain_core.messages import HumanMessage, AIMessage

from agent import chatbot, retrieve_all_threads

from tools.tools_rag import create_vector_store
from tools import shared_state

import traceback

import shutil
import os


st.set_page_config(
    page_title='HybridSight',
    page_icon='🤖',
    layout='wide'
)

st.markdown(
    """
    <h1 style="text-align:center;">
        🤖 HybridSight
    </h1>
    <p style="text-align:center;color:gray;">
        RAG + Web Search + Vision Agent
    </p>
    """,
    unsafe_allow_html=True
)

TOOL_STATUS = {
    "search_documents": "📄 Searching documents...",
    "search_web": "🔍 Searching the web...",
    "search_wikipedia": "📚 Searching Wikipedia...",
    "describe_image": "🖼️ Analyzing image..."
}

def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        
def load_conversation(thread_id):
    state = chatbot.get_state(
        config={
            'configurable':{
                'thread_id': thread_id
            }
        }
    )
    
    if not state.values:
        return []
    return state.values.get(
        'messages',
        []
    )
    
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()
    
if 'pdf_indexed' not in st.session_state:
    st.session_state['pdf_indexed'] = False
    
if 'image_uploaded' not in st.session_state:
    st.session_state['image_uploaded'] = False
    
add_thread(st.session_state['thread_id'])

def reset_chat():

    thread_id = generate_thread_id()

    st.session_state['thread_id'] = thread_id

    add_thread(thread_id)

    st.session_state['message_history'] = []

    st.session_state['pdf_indexed'] = False

    st.session_state['image_uploaded'] = False

    shared_state.CURRENT_IMAGE_PATH = None

    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")

    if os.path.exists("uploaded.pdf"):
        os.remove("uploaded.pdf")

    if (
        shared_state.CURRENT_IMAGE_PATH is not None
        and os.path.exists(shared_state.CURRENT_IMAGE_PATH)
    ):
        os.remove(shared_state.CURRENT_IMAGE_PATH)

    
def get_chat_title(messages):
    for message in messages:
        if isinstance(message, HumanMessage):
            title = message.content.strip()
            if len(title)>30:
                return title[ :30] + '...'
            return title
    return 'New Chat'


# ==========================================
#               Sidebar UI
# ==========================================

st.sidebar.title("🤖 HybridSight")

uploaded_pdf = st.sidebar.file_uploader(
    "📄 Upload PDF",
    type=['pdf']
)

uploaded_image = st.sidebar.file_uploader(
    "🖼️ Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_pdf is not None and not st.session_state['pdf_indexed']:
    
    with open("uploaded.pdf", 'wb') as f:
        f.write(uploaded_pdf.getbuffer())
        
    create_vector_store('uploaded.pdf')
    
    st.session_state['pdf_indexed'] = True
    
    st.sidebar.success(
        "✅ PDF uploaded and indexed!"
    )
    
if uploaded_image is not None and not st.session_state['image_uploaded']:
    
    file_extension = uploaded_image.name.split('.')[-1]
    
    image_path = f'uploaded_image.{file_extension}'
    
    with open(image_path, 'wb') as f:
        f.write(uploaded_image.getbuffer())
        
    shared_state.CURRENT_IMAGE_PATH = image_path
    
    st.session_state['image_uploaded'] = True
    
    st.sidebar.success(
        "✅ Image uploaded successfully!"
    )

if st.sidebar.button("➕ New Chat", use_container_width=True):
    reset_chat()
    
st.sidebar.divider()

st.sidebar.subheader("💬 Conversations")

for thread_id in st.session_state['chat_threads'][::-1]:
    
    messages = load_conversation(thread_id)
    
    title = get_chat_title(messages)
    
    label = (
        f"👉 💬 {title}"
        if thread_id == st.session_state["thread_id"]
        else f"💬 {title}"
    )
    
    if st.sidebar.button(
        label,
        key=str(thread_id),
        use_container_width=True
    ):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        temp_messages = []
        
        for message in messages:
            
            role = (
                'user'
                if isinstance(message, HumanMessage)
                else 'assistant'
            )
            
            temp_messages.append(
                {
                    'role': role,
                    'content': message.content
                }
            )
            
        st.session_state["message_history"] = temp_messages
        
# ==========================================
#                 Main UI
# ==========================================

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        
user_input = st.chat_input(
    "Ask anything..."
)

if user_input:
    st.session_state['message_history'].append(
        {
            'role': 'user',
            'content': user_input
        }
    )
    
    with st.chat_message('user'):
        st.markdown(user_input)
        
    CONFIG = {
        'configurable':{
            'thread_id': st.session_state['thread_id']
        }
    }
    
    with st.chat_message('assistant'):
        
        status = st.status(
            label="🤖 Working...",
            expanded=True
        )
        
        try:
            
            def only_ai_message():
                
                for message_chunk, metadata in chatbot.stream(
                    {
                        'messages':[
                            HumanMessage(content=user_input)
                        ]
                    },
                    config=CONFIG,
                    stream_mode='messages'
                ):
                    
                    if metadata['langgraph_node'] == 'tools':
                        status.update(
                            label=TOOL_STATUS.get(
                                message_chunk.name,
                                "🔧 Using Tool..."
                            ),
                            state='running',
                            expanded=True
                        )
                        
                    if isinstance(message_chunk, AIMessage) and message_chunk.content:
                        yield message_chunk.content
                        
            ai_message = st.write_stream(
                only_ai_message()
            )
            
            status.update(
                label="✅ Completed",
                state="complete",
                expanded=False
            )
            
        except Exception as e:

            traceback.print_exc()

            ai_message = f"❌ {e}"

            status.update(
                label="❌ Error",
                state="error",
                expanded=True
            )

            st.error(ai_message)
            
    st.session_state['message_history'].append(
        {
            'role': 'assistant',
            'content': ai_message
        }
    )