import os
from langchain_community.tools import TavilySearchResults
from langchain.agents import tool
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from time import sleep
import cv2
from djitellopy import Tello

drone = Tello()
drone.connect()
# Get battery level
battery = drone.get_battery()
print(f"🔋 Battery level: {battery}%")
drone.streamon()
load_dotenv()

# llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

############# Setup Gemini #############
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=api_key
)



@tool
def move_left() -> str:
    """Move the drone to the left."""
    print("📡 Executing: move_left")
    drone.send_rc_control(-50, 0, 0, 0)
    sleep(2)
    drone.send_rc_control(0, 0, 0, 0)
    print("✅ Action complete: Moved left")
    return "Moved left"

@tool
def move_right() -> str:
    """Move the drone to the right."""
    print("📡 Executing: move_right")
    drone.send_rc_control(50, 0, 0, 0)
    sleep(2)
    drone.send_rc_control(0, 0, 0, 0)
    print("✅ Action complete: Moved right")
    return "Moved right"

@tool
def move_forward() -> str:
    """Move the drone forward."""
    print("📡 Executing: move_forward")
    drone.send_rc_control(0, 50, 0, 0)
    sleep(4)
    drone.send_rc_control(0, 0, 0, 0)
    print("✅ Action complete: Moved forward")
    return "Moved forward"

@tool
def move_backward() -> str:
    """Move the drone backward."""
    print("📡 Executing: move_backward")
    drone.send_rc_control(0, -50, 0, 0)
    sleep(2)
    drone.send_rc_control(0, 0, 0, 0)
    print("✅ Action complete: Moved backward")
    return "Moved backward"

@tool
def rotate_left() -> str:
    """Rotate the drone to the left (counter-clockwise)."""
    print("📡 Executing: rotate_left")
    drone.rotate_counter_clockwise(90)
    print("✅ Action complete: Rotated left")
    return "Drone rotated left"

@tool
def rotate_right() -> str:
    """Rotate the drone to the right (clockwise)."""
    print("📡 Executing: rotate_right")
    drone.rotate_clockwise(90)
    print("✅ Action complete: Rotated right")
    return "Drone rotated right"

@tool
def take_photo() -> str:
    """Take a photo with the drone's camera."""
    print("📸 Executing: take_photo")
    frame = drone.get_frame_read().frame
    cv2.imwrite("tello_photo.jpg", frame)
    print("✅ Photo saved as 'tello_photo.jpg'")
    return "Photo taken and saved as 'tello_photo.jpg'"

@tool
def takeoff() -> str:
    """Command the drone to take off."""
    print("🛫 Executing: takeoff")
    drone.takeoff()
    print("✅ Action complete: Drone takeoff")
    return "Drone takeoff"

@tool
def land() -> str:
    """Command the drone to land."""
    print("🛬 Executing: land")
    drone.land()
    print("✅ Action complete: Drone landing")
    return "Drone landing"
@tool
def move_up() -> str:
    """Move the drone upward (ascend)."""
    print("📡 Executing: move_up")
    drone.send_rc_control(0, 0, 50, 0)
    sleep(2)
    drone.send_rc_control(0, 0, 0, 0)
    print("✅ Action complete: Moved up")
    return "Moved up"

@tool
def move_down() -> str:
    """Move the drone downward (descend)."""
    print("📡 Executing: move_down")
    drone.send_rc_control(0, 0, -50, 0)
    sleep(2)
    drone.send_rc_control(0, 0, 0, 0)
    print("✅ Action complete: Moved down")
    return "Moved down"



def summarize_instructions(mission: str) -> List[str]:
    """Summarize user mission to instructions and return a list of instrutions (or empty if none)."""
    
    prompt = f"""You are a tello drone control expert.

Analyze the following user mission and 
Respond with a short bullet list of instructions (e.g., '- take a photo '), or just say "."
Do not include explanations or suggestions.
if take off and land are not explicitly asked dont use them 

Manifest:
{mission}
"""

    # 1. Call LLM
    response = llm.invoke([HumanMessage(content=prompt)])

    # 2. Extract text
    summary_text = response.content.strip()
    print(f"🧠 Final summary used:\n{summary_text}\n")

    # 3. Convert to Python list
    if "no instruction found" in summary_text.lower():
        return []

    # Split lines that begin with "-", "*" or are numbered
    instruction = [
        line.strip("-*•1234567890. ").strip()
        for line in summary_text.splitlines()
        if line.strip() and not line.lower().startswith("no issues")
    ]

    return instruction



tools = [
    move_left,
    move_right,
    move_forward,
    move_backward,
    rotate_left,
    rotate_right,
    take_photo,
    takeoff,
    land,
    move_up,
    move_down
]





