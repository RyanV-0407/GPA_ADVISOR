<div align="center">
  <img src="https://img.icons8.com/color/96/000000/student-center.png" alt="GPA Advisor Logo" width="80" height="80">
  
  # GPA Advisor Agent 🎓
  
  **An AI-Powered Academic Trajectory Planner & Digital Transcript Metaphor**
  
  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
</div>

---

## 📖 Overview

**GPA Advisor Agent (Topic T28)** is an intelligent automation tool designed to help students track, calculate, and project their academic trajectory using a deterministic, memory-aware AI. By combining the natural language understanding of a Large Language Model (LLM) with strict mathematical tools, it provides highly accurate advice for academic planning.

This project was built for **CSE476 – Agentic AI & Intelligent Automation**.

## ✨ Features

- **Deterministic Math Engine:** Resolves the common LLM hallucination issue in arithmetic. It relies on deterministic Python tools like `add_grade(course, grade, credits)` and `compute_gpa()` to calculate exact credit-weighted GPAs based on the 10-point scale (O=10 to F=0).
- **Session Memory Tracking:** Powered by the `GPAMemory` class, the agent persistently stores recorded courses, grades, and credits across multi-turn dialogues. You don't need to repeat your transcript every time you ask a question.
- **Target GPA Feasibility Check:** The agent calculates whether ambitious target GPAs are mathematically possible based on your current standing and remaining credits, returning explicit statuses (e.g., `ACHIEVABLE` or `Mathematically IMPOSSIBLE`).
- **Interactive UI:** A beautifully designed Streamlit interface employing classical academic iconography (Oxford Paper & Cambridge Chalkboard themes).

## 🛠️ Architecture: THINK ➔ ACT ➔ OBSERVE

The system forces the agent to ground its final advice strictly on verifiable tool results:
1. **Tool Invocation Directives:** The system prompt enforces strict rules to prevent the LLM from attempting "mental math".
2. **Session State Storage:** Holds historical course data, enabling long-term reasoning.
3. **Deterministic Feasibility Checks:** Offloads grade capability checks strictly to Python calculations, ensuring no false encouragement is given.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RyanV-0407/GPA_ADVISOR.git
   cd GPA_ADVISOR
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory for any required API keys (e.g. LLM configuration).

### Usage

Run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

## 👨‍🎓 Author Information

- **Name:** Vikram Singh Rathour
- **Registration No:** 12324502
- **Course:** CSE476 – Agentic AI & Intelligent Automation
- **GitHub:** [RyanV-0407](https://github.com/RyanV-0407)

---

<div align="center">
  <i>Built with determination to eliminate AI arithmetic hallucinations.</i>
</div>
