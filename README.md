
# 🤖 AI Coding Agent

This is a terminal-based AI assistant built with Gemini API (using OpenAI compatibility) that can generate full-stack apps using plain English prompts. It writes code, creates files, executes terminal commands, and can fetch weather data — all through intelligent step-by-step planning.

---

## 📦 Features

- 🧠 Uses Gemini AI (via OpenAI wrapper)
- 🛠️ Executes commands like `mkdir`, `npm install`, `npm run dev`
- 🗂️ Writes HTML/CSS/JS/React code into proper file structure
- 📁 Creates project folders like `todo-app`, `weather-app`
- 🔄 Follows intelligent plan → action → observe → output loop
- 🌦️ Uses wttr.in API to fetch weather by city (no API key needed)

---

## 🧪 Example Prompts

```text
Make a to-do app in React using Vite
Create a weather app using HTML, CSS, and JavaScript that fetches weather using wttr.in
Add a login page to the React app
```

---

## 🧰 Toolset

The agent can call the following tools:

- `run_command`: Execute terminal commands
- `write_file`: Write content into files (e.g., `src/App.jsx`)
- `change_directory`: Move into a folder (e.g., `weather-app`)
- `get_weather`: Fetch weather using `https://wttr.in/<city>?format=%C+%t`

---

## 📁 Project Structure Example

```
AI CODING AGENT/
├── app/
│   └── main.py
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

1. Clone the repo or copy files into your local folder
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your Gemini API key to `.env`:
   ```env
   GOOGLE_API_KEY=your-api-key-here
   ```
5. Run the agent:
   ```bash
   python app/main.py
   ```

---

## ❌ `.gitignore` (Important)

Make sure to exclude:
```
venv/
.env
__pycache__/
.vscode/
```

---

## 📜 License

MIT – Use freely, build anything!

---

## 🙋‍♂️ Need Help?

Just open a terminal and ask your agent:

> Make a weather app using HTML, CSS and JS

and it will plan, generate code, and even run it for you.
