
import streamlit as st

from ollama_service import OllamaService


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Smart AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .sub-title {
        color: #777;
        font-size: 15px;
        margin-bottom: 20px;
    }

    .status-box {
        padding: 10px;
        border-radius: 8px;
        background-color: #f5f5f5;
        margin-bottom: 10px;
    }

    .model-box {
        padding: 12px;
        border-radius: 10px;
        background-color: #f7f7f7;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are a helpful AI assistant. "
        "Give clear, accurate and concise answers."
    )


# ---------------------------------------------------------
# Ollama service
# ---------------------------------------------------------

service = OllamaService(model="phi4-mini")


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## ⚙️ Configuration")

    st.divider()

    # Model
    st.markdown("### 🤖 Model")

    models = service.get_models()

    if models:

        if "phi4-mini" in models:
            default_index = models.index("phi4-mini")
        else:
            default_index = 0

        selected_model = st.selectbox(
            "Select model",
            models,
            index=default_index
        )

        service.model = selected_model

    else:

        st.warning("No Ollama models found.")

        selected_model = "phi4-mini"

        service.model = selected_model


    # System prompt
    st.markdown("### 📝 System Prompt")

    system_prompt = st.text_area(
        "Instructions for AI",
        value=st.session_state.system_prompt,
        height=150
    )

    st.session_state.system_prompt = system_prompt


    st.divider()


    # Connection status
    st.markdown("### 🔌 Ollama Status")

    connected, status_message = service.check_connection()

    if connected:
        st.success("Ollama Connected")
    else:
        st.error("Ollama Not Connected")


    st.caption(status_message)


    st.divider()


    # Clear chat
    if st.button(
        "🧹 Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    # Download conversation
    if st.session_state.messages:

        conversation_text = ""

        for message in st.session_state.messages:

            role = message["role"].upper()

            conversation_text += (
                f"\n\n{role}\n"
                f"{message['content']}"
            )

        st.download_button(
            "📥 Download Conversation",
            data=conversation_text,
            file_name="Chat_conversation.txt",
            mime="text/plain",
            use_container_width=True
        )


# ---------------------------------------------------------
# Main page
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 Smart AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Local AI assistant powered by Ollama + Microsoft Phi-4 Mini'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Model information
# ---------------------------------------------------------

st.markdown(
    f"""
    <div class="model-box">
        <b>Model:</b> {service.model}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>Mode:</b> Local AI
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Welcome message
# ---------------------------------------------------------

if not st.session_state.messages:

    st.info(
        """
        👋 Welcome!

        You are chatting with **Smart AI Assistant running locally through Ollama**.

        Try asking:

        • Explain dependency injection in ASP.NET Core  
        • Write a C# palindrome program  
        • Explain SOLID principles  
        • Generate a SQL query  
        • Help debug my Python code
        """
    )


# ---------------------------------------------------------
# Display conversation
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

prompt = st.chat_input(
    "Ask Phi-4 Mini anything..."
)


if prompt:

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)


    # -----------------------------------------------------
    # Save user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # -----------------------------------------------------
    # Prepare messages for Ollama
    # -----------------------------------------------------

    ollama_messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    ollama_messages.extend(
        st.session_state.messages
    )


    # -----------------------------------------------------
    # Generate response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        try:

            with st.spinner("AI Assistant is thinking..."):

                for chunk in service.chat(
                    ollama_messages
                ):

                    full_response += chunk

                    response_placeholder.markdown(
                        full_response + "▌"
                    )


            response_placeholder.markdown(
                full_response
            )


            # -------------------------------------------------
            # Save assistant response
            # -------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response
                }
            )


        except Exception as e:

            st.error(
                "Unable to generate a response from Ollama."
            )

            st.exception(e)
