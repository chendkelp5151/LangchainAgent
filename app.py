"""Streamlit Web UI for NVIDIA Nemotron 3 Ultra Chat Agent."""

import streamlit as st
import uuid
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import config
from agent import create_agent

st.set_page_config(
    page_title="NVIDIA Nemotron 3 Ultra Chat Agent",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ NVIDIA Nemotron 3 Ultra Agent")
st.caption(f"Powered by LangChain, LangGraph & NVIDIA NIM ({config.NVIDIA_MODEL})")

# Check API Key
if not config.NVIDIA_API_KEY or config.NVIDIA_API_KEY.startswith("nvapi-your"):
    st.error("⚠️ NVIDIA_API_KEY is not configured! Please configure it in your `.env` file or environment variables.")
    st.stop()

# Initialize session state for memory and agent
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "agent" not in st.session_state:
    st.session_state.agent = create_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Agent Settings")
    st.markdown(f"**Model:** `{config.NVIDIA_MODEL}`")
    st.markdown(f"**Thread ID:** `{st.session_state.thread_id[:8]}`")
    
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")
    st.markdown("### 🛠️ Active Tools")
    st.markdown("- 🌐 **Web Search** (`DuckDuckGo`)")
    st.markdown("- 🧮 **Calculator** (Safe math evaluation)")
    st.markdown("- 🕒 **DateTime** (Timezone & date query)")
    st.markdown("- 📝 **Create Note** (Save memos to `notes.txt`)")
    st.markdown("- 📖 **List Notes** (Retrieve past notes)")

# Render existing conversation messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt input
if prompt := st.chat_input("Ask Nemotron anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Agent response
    with st.chat_message("assistant"):
        agent_config = {"configurable": {"thread_id": st.session_state.thread_id}}
        inputs = {"messages": [HumanMessage(content=prompt)]}
        
        status_placeholder = st.empty()
        response_placeholder = st.empty()
        
        final_response = ""
        
        try:
            for event in st.session_state.agent.stream(inputs, config=agent_config, stream_mode="values"):
                messages = event.get("messages", [])
                if messages:
                    latest = messages[-1]
                    if isinstance(latest, ToolMessage):
                        status_placeholder.info(f"🔧 Tool `{latest.name}` executed: {latest.content[:100]}...")
                    elif hasattr(latest, "content") and latest.content and latest.type == "ai":
                        if not latest.tool_calls:
                            final_response = latest.content
                            response_placeholder.markdown(final_response)
                        else:
                            tool_names = ", ".join([tc['name'] for tc in latest.tool_calls])
                            status_placeholder.warning(f"🤔 Reasoning & invoking tool(s): `{tool_names}`...")
            
            status_placeholder.empty()
            if final_response:
                st.session_state.messages.append({"role": "assistant", "content": final_response})
        except Exception as e:
            st.error(f"Error during agent execution: {str(e)}")
