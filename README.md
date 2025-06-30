# LLM-based-drone-voice-control-agent

This project enables voice-controlled autonomous flight using a Tello drone. It combines LangGraph, Google Gemini, and LangChain to interpret user speech, plan actions, and execute drone maneuvers using ReAct-style agents.
example video link:
https://www.linkedin.com/posts/ron-salomon96_can-llms-operate-in-the-real-world-as-activity-7342246338752884736-38m4?utm_source=share&utm_medium=member_desktop&rcm=ACoAAC_mZc4BRPay8Hlblk3_Q1IlaAooTUeFZPo
## Features

- Voice Input: Speak natural-language missions to the drone.
- LLM Planning: Uses Gemini 1.5 Flash to convert missions into atomic drone actions.
- LangGraph Workflow: Modular, ReAct-style state machine powered by LangGraph.
- Tool Integration: Each drone operation is a tool (move_left, take_photo, etc.).
- Camera Control: Takes photos with onboard drone camera.
- Instruction Execution: One mission turns into multiple actions executed step-by-step.

## Tech Stack

- Drone: Ryze Tello
- LLM: Google Gemini 1.5 Flash (langchain_google_genai)
- LangChain and LangGraph
- Speech Recognition: Python speech_recognition
- Drone SDK: djitellopy

## Setup Instructions

### 1. Clone the repo


### 2. Install dependencies

pip install -r requirements.txt

### 3. Add .env file
Create a .env file in the root directory with:

```
GOOGLE_API_KEY=your_gemini_api_key
```

If using OpenAI:
```
OPENAI_API_KEY=your_openai_api_key
```

### 4. Connect the drone

## How to Run

python main.py


Then:
1. Speak your mission (e.g., "Fly forward and take a photo").
2. The system will:
   - Convert voice to text
   - Summarize it into actionable instructions
   - Use the LLM to select tools
   - Execute them via the drone

Type `exit` to stop.
