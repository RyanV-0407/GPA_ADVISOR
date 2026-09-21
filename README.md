# GPA Advisor Agent (Topic T28)

**Author:** Vikram Singh Rathour  
**Registration No:** 12324502  
**Course:** CSE476 – Agentic AI & Intelligent Automation  

---

The agent relies on two core deterministic Python tools: `add_grade(course, grade, credits)` and `compute_gpa()`. The `add_grade` tool validates course titles, standardizes letter grades against the 10-point scale (O = 10 down to F = 0), and records each course with its credit weight into session storage. When current standing or advice is requested, the agent calls `compute_gpa()` to deterministically compute the exact credit-weighted Grade Point Average ($\sum (\text{points} \times \text{credits}) / \sum \text{credits}$), preventing the language model from hallucinating or approximating arithmetic.

The session memory is managed by the `GPAMemory` class, which persists all recorded courses, grades, and credit hours across multiple conversation turns. Rather than losing context between messages or requiring the user to re-enter their transcript, this memory retains an active course dictionary throughout the session. This enables the agent to reference historical coursework across multi-turn dialogues, track cumulative credits, and calculate future grade requirements for target GPAs using verified historical data.

One honest failure we encountered was that the LLM frequently attempted mental math rather than invoking tools, hallucinated that ambitious target averages (like 9.7/10) were impossible because it assumed A+ (9.0) was the maximum grade, and offered false encouragement for targets that were mathematically impossible. We handled this by enforcing strict tool-use directives in the system prompt and offloading all mathematical feasibility calculations to deterministic Python functions that return clear, explicit statuses (`ACHIEVABLE` via grade O or `Mathematically IMPOSSIBLE`), forcing the agent to ground its final advice strictly on verifiable tool results.
