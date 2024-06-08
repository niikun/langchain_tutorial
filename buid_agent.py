# import os
# import click
# from dotenv import load_dotenv
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain_openai import ChatOpenAI
# from langgraph.prebuilt import create_react_agent
# from langgraph.checkpoint.sqlite import SqliteSaver

# # Load environment variables
# load_dotenv()

# # Get API keys from environment variables
# openai_api_key = os.getenv("OPENAI_API_KEY")
# langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
# tavily_api_key = os.getenv('TAVILY_API_KEY')

# # define tools
# search = TavilySearchResults(max_results=2, api_key=tavily_api_key)
# tools = [search]

# # setup language model
# model = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)

# # setup memory (not used directly in create_react_agent)
# memory = SqliteSaver.from_conn_string(":memory:")

# # setup agent
# agent_executor = create_react_agent(model, tools, messages_modifier=None)  # messages_modifier を None に設定
# config = {"configurable": {"thread_id": "abc123"}}

# @click.command()
# @click.option("--user_input", help="User input to chat with the agent")
# def chat_with_agent(user_input):
#     if not user_input:
#         print("Error: user_input is required")
#         return

#     for chunk in agent_executor.stream(
#         {"messages": [
#             SystemMessage(content="You are a helpful Osaka woman. Answer all questions in Japanese, Osaka dialect."),
#             HumanMessage(content=user_input)]}, config=config
#     ):
#         print(chunk)

# if __name__ == "__main__":
#     # pylint: disable=no-value-for-parameter
#     chat_with_agent()
