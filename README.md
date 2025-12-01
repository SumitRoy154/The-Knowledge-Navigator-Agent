

# 🎓 The Knowledge Navigator Agent

<p align="center">
  <img src="https://raw.githubusercontent.com/SumitRoy154/The-Knowledge-Navigator-Agent/main/Image.png" alt="The Knowledge Navigator Agent Logo and Uses" width="560"/>
  <br>
  <b>LLM Concierge for Curated Learning Paths and Real-Time Course Data.</b>
</p>

## Table of Contents

1.  [🌟 Key Features](https://www.google.com/search?q=%23-key-features)
2.  [💡 The Problem Solved](https://www.google.com/search?q=%23-the-problem-solved)
3.  [⚙️ Architecture & Flow](https://www.google.com/search?q=%23%EF%B8%8F-architecture--flow)
4.  [🚀 Getting Started](https://www.google.com/search?q=%23-getting-started)
5.  [📂 Project Structure](https://www.google.com/search?q=%23-project-structure)
6.  [🛠️ Future Roadmap](https://www.google.com/search?q=%23-future-roadmap)

-----

## 🌟 Key Features

The Knowledge Navigator Agent is designed to transform the process of finding and planning online education:

  * **Curriculum Sequencing:** Converts fragmented course data into a structured, phased learning path (e.g., Phase I: Foundation, Phase II: Application).
  * **Real-Time Data Retrieval:** Uses **Function Calling** to query external sources for up-to-date course prices, reviews, and availability.
  * **Contextual Memory:** Employs **Session Management** to maintain conversational state and user constraints (budget, topic) across multiple turns.
  * **Academic Advisor Persona:** Guided by a custom **System Prompt** to deliver results with a professional, data-driven, and supportive tone.
  * **Terminal-Only:** Lightweight Python application running entirely in the command line.

-----

## 💡 The Problem Solved

### Why Agents?

The problem requires complex, multi-step planning and real-time data access, making it unsuitable for simple chatbots:

1.  **Hallucination Risk:** A standard LLM cannot retrieve current prices or check course availability, leading to false information.
2.  **No Action:** The agent must *act* by executing external code (Function Calling) to search, compare data (price, rating, duration), and then apply **Curriculum Sequencing logic** to order the results.
3.  **Lack of Context:** The agent must remember the user's "beginner" status or budget across turns, which requires explicit **State Management**.

The **LLM-powered Agent** architecture solves these limitations by providing the reasoning (LLM) and the ability to execute code (Tools).

## ⚙️ Architecture & Flow

The agent operates on a **ReAct (Reasoning and Action)** loop driven by the Gemini LLM.

**Core Technical Summary (138 Characters):**

> Knowledge Navigator Agent: An LLM concierge using Function Calling & RAG. Retrieves/compares real-time course data, maintaining State Management with custom tools.

### Key Components

  * **Brain:** **Gemini API** for Reasoning, Planning, and Curriculum Sequencing.
  * **Tool (Custom):** `search_online_courses` for structured course data retrieval.
  * **Tool (Built-in):** Google Search for broad, real-time background context.
  * **Memory:** Session management to track conversation history and constraints.

-----

## 🚀 Getting Started

This guide assumes you have Python 3.10+ installed and a Gemini API key.

### 1\. Clone the Repository

```bash
git clone https://github.com/SumitRoy154/The-Knowledge-Navigator-Agent.git
cd The-Knowledge-Navigator-Agent
```

### 2\. Set up Environment and Install Dependencies

Create a Python virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3\. Configure API Key

Create a file named `.env` in the root directory and add your key:

```ini
# .env file
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 4\. Run the Agent

Start the interactive terminal session:

```bash
python3 main.py
```

**Example Prompt:** `I need to learn Python. I am a beginner, and my budget is $100.`

-----

## 📂 Project Structure

The project is modular, built to separate configuration, logic, and tools.

```
knowledge_navigator_agent/
├── .env                  # Environment variables (API Key)
├── main.py               # Main entry point (starts the terminal chat loop)
├── requirements.txt      # Project dependencies
├── agent.py              # The Agent class, System Prompt, and ReAct logic
├── config.py             # Loads .env settings
├── memory.py             # Session/State Management implementation
└── tools/
    ├── __init__.py
    └── course_finder.py  # Contains the 'search_online_courses' custom function
```

## 🛠️ Future Roadmap

The next phase would focus on moving from sequencing to truly **adaptive learning** using a **Multi-Agent System**:

1.  **Adaptive Learning Path (Advanced RAG):** Implement a **Vector Database** to store long-term user history (past courses, skill gaps). This enables **real-time adaptive guidance** that changes the path based on proven user progress.
2.  **Specialized Multi-Agent System (MAS):** Introduce a dedicated **Path Planning Agent** whose sole job is to ingest course results and calculate the optimal sequence, delegating the final conversational output to the main Concierge Agent.
3.  **Formal Evaluation:** Implement formal metrics to measure **Tool-Use Accuracy** and **Groundedness** (verifying that the LLM's final answer is supported by the data from the custom tool).
