from openai import OpenAI
import requests
from datetime import datetime
import os
import json

client = OpenAI(
    api_key="AIzaSyCRgdqi8elWuIGBpr-ecC7lecM_0q2kwr4",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(cmd: str):
    print(f"💻 Running: {cmd}")
    result = os.system(cmd)
    return f"Command '{cmd}' executed with exit code {result}"

def write_file(data: dict):
    path = data.get("path")
    content = data.get("content")

    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"✅ File written: {path}"

def get_weather(city: str):
    if not city or not isinstance(city, str):
        return "Invalid city name."

    url = f"https://wttr.in/{city}?format=%C+%t"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and response.text.strip():
            return f" The weather in {city.title()} is {response.text.strip()}."
        return " City not found or no weather data returned."
    except Exception as e:
        return f"Failed to fetch weather: {str(e)}"

def change_directory(path: str):
    os.chdir(path)
    return f"📁 Changed directory to: {path}"


def get_current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

available_tools = {
    "run_command": run_command,
    "write_file": write_file,
    "change_directory": change_directory,
    "get_weather": get_weather
}



SYSTEM_PROMPT = f"""
You are an AI Coding Agent that helps users build real full-stack and frontend apps using code and terminal commands.
You are a master of React, Vite, HTML, CSS, Python, JavaScript and can generate React components, HTML/CSS/JS files, and Vite projects.
You are an expert in solving user queries


You work in this mode: plan → action → observe → output



🔧 Your Tools:
- run_command: Run shell commands like mkdir, npm install, npm run dev
- write_file: Write code into a file. Input = {{ "path": "src/App.jsx", "content": "<html>" }}
- change_directory: Change working directory
- get_weather: Takes a city name (string), uses https://wttr.in to return current weather. Example: get_weather("Balasore")

Rules:
- Only call tools with real values. For get_weather, don't pass "city" or empty string.
- Only one tool per action.
- Wait for observation before continuing.

Example for the formatting of weather app-
(IN JSON Format):

{{
  "step": "plan | action | observe | output",
  "content": "description",
  "function": "tool name (if action)",
  "input": "value for that tool"
}}

📦 Your Abilities:
- Understand user prompts like:
  - “Make a To-Do app in React”
  - “Create a weather app using HTML/CSS/JS and an API”
  - “Generate a Vite-based React project”
- Use frameworks and tools like React, Vite, HTML/CSS/JS, and public APIs.
- Choose from already available public APIs (like https://wttr.in or open-meteo.com for weather).
- Always generate `*.jsx` files for React components.
- Use semantic folder structure like: `public/`, `src/`, etc.
- Handle iterative prompts like “add a login page” or “style the header”.

🧠 Guidelines:
- Always create a folder (e.g., "weather-app") and write all related files inside it.just a main directory that means for a simple project like weather app the folderstructure will be like this: 

- weather-app/
    - index.html
    - style.css
    - app.js or main.js 
follow this structure
- Use public API: https://wttr.in/<city>?format=%C+%t (no key needed)
- In HTML/JS apps, use fetch() to call the API and display results.
- All static files (HTML, CSS, JS) go in the app folder.
- Always use lowercase filenames like `index.html`, `style.css`, `app.js`
- Use semantic structure in the HTML file.
- Wait for the observe step before continuing.
- Output result only when done.


🧠 Planning Rules:
1. Break down the user’s idea into clear steps.
2. Use the tools one-by-one (never combine steps).
3. Wait for an “observe” response before moving to the next tool/action.

---

📝 Response Format (strict JSON):

{{
  "step": "plan | action | observe | output",
  "content": "what you're doing or found",
  "function": "tool function name (only for action)",
  "input": "the input to send to that tool"
}}

---

📅 Date: {datetime.now().strftime('%Y-%m-%d')}
"""




messages = [
    { "role": "system", "content": SYSTEM_PROMPT }
]

while True:
    query = input("👤 You: ")
    messages.append({ "role": "user", "content": query })

    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={ "type": "json_object" },
            messages=messages
        )

        content = response.choices[0].message.content
        print(f"\n🤖 Raw Response:\n{content}\n")

        messages.append({ "role": "assistant", "content": content })

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            print("❌ Failed to parse JSON from AI response.")
            break

        
        if isinstance(parsed, dict):
            parsed = [parsed]

        for step_obj in parsed:
            step = step_obj.get("step")
            info = step_obj.get("content")
            tool = step_obj.get("function")
            tool_input = step_obj.get("input")

            if step == "plan":
                print(f"🧠 Plan: {info}")
                continue

            if step == "action":
                print(f"🛠️ Executing: {tool} with → {tool_input}")
                if tool in available_tools:
                    result = available_tools[tool](tool_input)
                    messages.append({
                        "role": "user",
                        "content": json.dumps({ "step": "observe", "output": result })
                    })
                    break  
                else:
                    print(f"❌ Tool not found: {tool}")
                    break

            if step == "output":
                print(f"✅ Final Output: {info}")
                break

