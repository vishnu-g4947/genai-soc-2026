import streamlit as st
from graph import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid

st.set_page_config(page_title="AgentX", page_icon="🤖", layout="wide")

st.title("🤖 AgentX")
st.caption("AI Research Assistant powered by LangGraph")

TOOL_STATUS = {
    "duckduckgo_search": "🔍 Searching Web...",
    "wikipedia": "📚 Reading Wikipedia...",
    "get_current_date": "📅 Getting Current Date...",
}

# ==========================================
#               Utility Functions
# ==========================================


def get_thread_id():
    return str(uuid.uuid4())


def add_threads(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    st.session_state["thread_id"] = get_thread_id()
    add_threads(st.session_state["thread_id"])
    st.session_state["message_history"] = []


def load_chat(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})

    if not state.values:
        return []

    return state.values.get("messages", [])


# ==========================================
#               Session Setup
# ==========================================

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = get_thread_id()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_threads(st.session_state["thread_id"])


# ==========================================
#               Sidebar UI
# ==========================================

with st.sidebar:

    st.title("Chats")

    st.button("➕ New Chat", use_container_width=True, on_click=reset_chat)

    st.header("My Conversations")

    st.divider()

    for thread in st.session_state["chat_threads"][::-1]:

        if st.button(str(thread), use_container_width=True):

            st.session_state["thread_id"] = thread

            messages = load_chat(thread)

            temp_messages = []

            for message in messages:

                if isinstance(message, HumanMessage):

                    temp_messages.append({"role": "user", "content": message.content})

                elif isinstance(message, AIMessage):

                    if not message.content:
                        continue

                    temp_messages.append(
                        {"role": "assistant", "content": message.content}
                    )

            st.session_state["message_history"] = temp_messages
            st.rerun()

# ==========================================
#                 Main UI
# ==========================================

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask AgentX anything...")

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state["message_history"].append({"role": "user", "content": prompt})

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "recursion_limit": 10,
    }

    with st.chat_message("assistant"):
        try:

            def only_ai_message():
                """
                Stream LangGraph updates and return
                the final assistant response.
                """

                final_response = ""

                status = st.status("🤖 Thinking...")

                for event in chatbot.stream(
                    {"messages": [HumanMessage(content=prompt)]},
                    config=CONFIG,
                    stream_mode="updates",
                ):

                    # Assistant node
                    if "assistant" in event:

                        ai_message = event["assistant"]["messages"][-1]

                        # Skip assistant messages that only contain tool calls
                        if ai_message.tool_calls:
                            continue

                        # Skip empty assistant messages
                        if not ai_message.content:
                            continue

                        # Store final response
                        final_response = ai_message.content

                    if "tools" in event:

                        tool_message = event["tools"]["messages"][-1]

                        if tool_message.name in TOOL_STATUS:
                            status.update(label=TOOL_STATUS[tool_message.name])

                status.update(label="✅ Done", state="complete", expanded=False)

                return final_response

            # Execute the stream
            final_response = only_ai_message()

            # Display the final response
            st.markdown(final_response)

        except Exception as e:
            st.exception(e)
            st.stop()

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": final_response}
    )
