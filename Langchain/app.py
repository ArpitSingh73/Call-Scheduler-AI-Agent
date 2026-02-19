# import getpass
# import os
# import dotenv

# from langchain_core.tools import tool


# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b


# dotenv.load_dotenv('.env')
# # if "GOOGLE_API_KEY" not in os.environ:
# #     os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

# KEY = os.environ.get("GEMINI_API_KEY")
# from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0,
#     google_api_key=KEY,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )


# llm = llm.bind_tools([multiply])

# messages = [
#     (
#         "system",
#         "answer user query.",
#     ),
#     ("human", "multiply 3 and 4"),
# ]
# ai_msg = llm.invoke(messages)
# print(ai_msg)


# ===========================================================
# import getpass
# import os
# import dotenv
# from langchain.chat_models import init_chat_model
# from pydantic import BaseModel
# from typing import List
# from langchain_core.tools import tool
# from langchain_core.messages import HumanMessage, SystemMessage


# dotenv.load_dotenv(".env")


# class Schema(BaseModel):
#     #  Village : str
#     #  Power : str
#     #  justu : List[str]
#     operand1: int
#     operand2: int
#     operator: str
#     answer: int


# @tool
# def add(a: int, b: int) -> int:
#     """Add two numbers."""
#     return a + b


# @tool
# def subtract(a: int, b: int) -> int:
#     """Subtract two numbers."""
#     return a - b


# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b


# @tool
# def divide(a: int, b: int) -> int:
#     """Divide two numbers."""
#     return a / b


# prompt = """ You are an advanced AI which is capable of generating responses using tools provided to you./
# Use the tools provided within you and answer the query as Output is -  """

# KEY = os.environ.get("GEMINI_API_KEY")
# if not KEY:
#     os.environ["GEMINI_API_KEY"] = getpass.getpass("APi key :")

# try:
#     model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
#     # model = model.with_structured_output(Schema)
#     # model = model.bind_tools([add, subtract, multiply, divide])
#     human_message = HumanMessage(content="What is sum of 2 and 3 ?")
#     system_message = SystemMessage(content=prompt)
#     response = model.invoke([human_message, system_message])
#     print(response)
# except Exception as e:
#     print(e)


from typing import Annotated
from typing_extensions import TypedDict
import dotenv, os, getpass
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from IPython.display import Image, display
import requests
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

dotenv.load_dotenv(".env")

KEY = os.environ.get("GOOGLE_API_KEY")

if not KEY:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Your API Key here :")


class State(TypedDict):
    answer: str
    data: list
    messages: Annotated[list, add_messages]


graph = StateGraph(State)


def getdata(state: State) -> State:
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users/1")
        # print(response)
        if response.status_code == 200:
            # print([response.text])
            return {"data": [response.text]}
        else:
            print("Nahi mila")
    except Exception as e:
        print(e)


def chatbot(state: State) -> State:
    try:
        print("in chatbot ----- ")
        llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
        input_message = [HumanMessage(
            content=f"summarize this data in human redable language for me - data : {state["data"]}"
        )]
        response = llm.invoke(input_message)
        print("Chatbot_response : ##### ", response.content)
        return {"messages":response.content, "answer": response.content}
    except Exception as e:
        print(e)


# graph.add_node("start",START)
graph.add_node("getdata", getdata)
graph.add_node("chatbot", chatbot)
# graph.add_node("end",END)

# graph.add_edge(START,"start")
graph.add_edge(START, "getdata")
graph.add_edge("getdata", "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile() 
for result in app.stream({ }):
    print(result)
try:
    display(Image(app.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass
