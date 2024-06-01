import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# Load environment variables
load_dotenv()

# # Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

# Initialize Streamlit app
st.title("Osaka 調べものおじさん")
st.write("調べたいサイトのURLを教えてください。チャットボットが大阪弁で質問に答えます！")  
search_url = st.text_input("URLを入力してください。")
response = requests.get(search_url, timeout=5)
soup = BeautifulSoup(response.content, 'html.parser')
text = soup.get_text()

# setup the retriever
vectorstore = Chroma.from_documents(
    documents=text.split("\n"),
    embedding=OpenAIEmbeddings()
)
retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)

# Set up the model and prompt template
question = st.text_input("質問を入力してください。")

model = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)
message="""
Answer the following question using the context only in japanese.

{question}

Context:
{context}
"""
prompt = ChatPromptTemplate.from_messages(["human",message])
rag_chain = {"context":retriever,"question":RunnablePassthrough()} | prompt | model

response = rag_chain.invoke(question)

st.write(response.content)