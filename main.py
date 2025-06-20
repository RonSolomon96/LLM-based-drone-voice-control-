from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import nodes 
from langgraph.graph import END , StateGraph, add_messages
#from langchain_core.messages import HumanMessage
#from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from tools import tools,summarize_instructions
import speech_recognition as sr
load_dotenv()

############ Setup Gemini #############
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=api_key
)
# voice to text function 
def voice_to_text() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        user_input = recognizer.recognize_google(audio)
        print(user_input)
    return user_input

# ############# Setup openai #############
# llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

# bind the llm with tools
llm_with_tools = llm.bind_tools(tools=tools)


# build graph   
graph = StateGraph(nodes.AgentState)
graph.set_entry_point("drone_expert")
graph.add_node("drone_expert", nodes.drone_expert(llm_with_tools))
graph.add_node("tools", nodes.tool_node)
graph.add_edge("drone_expert", "tools")
graph.add_edge("tools", END)

# start 
# for exit type exit 
app = graph.compile()


flag=0

while True:
    
    if flag == 0:
        user_input = voice_to_text()
        x = 1
    else:    
        user_input = input("mission:")
        
    if user_input == "exit":
        break
    # summarize mission to instruction 
    for instructions in summarize_instructions(user_input):
        state = { 
        "messages":["start"],
        "instruction": instructions,
        }
        r = app.invoke(state)
        print(r["instruction"])
    

            

