import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("LANGCHAIN_API_KEY")


model = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages(
    [(
        "system","You are a helpful Osaka woman.Answer all questions in Japanese,Osaka language."
        ),
     MessagesPlaceholder(variable_name="messages")
    ]
)
chain = prompt | model

response = chain.invoke({"messages":[HumanMessage(content="おばちゃん、はらべったわ！")]})
print(response.content)