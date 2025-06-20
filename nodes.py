from langgraph.prebuilt import ToolNode
from langgraph.graph import END , add_messages
from typing import TypedDict, Annotated
from tools import tools
from typing import TypedDict, Annotated, Optional
from langchain_core.messages import HumanMessage, AIMessage


# define intial state 
# optional makes the field able to hold none 
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # user/agent conversation
    instruction: Optional[str] 
 

# define graph nodes
tool_node = ToolNode(tools=tools)


#define drone expert node 
def drone_expert(llm):
    def expert(state):
        messages = state.get("messages", [])
        instruction = state.get("instruction")
        prompt = f"""
You are a tello drone controler expert.

Your task:
1. Analyze the following instrution sentence, Do not invent or add extra instructions.

this is the context massages:
{
    messages
}
you need to use the tool you have and execute the relevant drone instrution 

Input instruction:
{instruction}
if the instrution is not in the tool list just finish

you need to choose the most relevant instruction and use the relevant tool

"""

        response = llm.invoke([HumanMessage(content=prompt)])
        
        if "finish" in response.content:
                print(response.content)
                return {
            "messages": [response],
            "instruction": []
        }
        else:
            return {
                "messages": [response],
            }

    return expert


    

