import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables
load_dotenv()

# Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

# Set up the model and prompt template
model = ChatOpenAI(model="gpt-4", api_key=openai_api_key)
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You are a helpful Osaka woman. Answer all questions in Japanese, Osaka dialect."),
        MessagesPlaceholder(variable_name="messages")
    ]
)

# Initialize Streamlit app
st.title("Osaka Chatbot")
st.write("質問を入力してください。チャットボットが大阪弁で答えます！")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Input for user messages
user_input = st.text_input("あなたのメッセージ:", key="input", value="")

# Process user input and generate response
if user_input and st.button("送信"):
    # Add user's message to the chat history
    st.session_state.messages.append(HumanMessage(content=user_input))
    
    # Create a chain and generate response
    chain = prompt | model

    try:
        response = chain.invoke({"messages": st.session_state.messages})
        if response:
            # Add AI's response to the chat history
            st.session_state.messages.append(AIMessage(content=response.content))
        else:
            st.error("応答が空です。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

# Display chat history
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        st.write(f"**あなた:** {message.content}")
    elif isinstance(message, AIMessage):
        st.write(f"**チャットボット:** {message.content}")

# Add a button to clear chat history
if st.button("履歴をクリア"):
    st.session_state.messages = []
    st.experimental_rerun()
