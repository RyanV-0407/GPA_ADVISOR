"""
GPA Advisor Agent

CSE476-style agent architecture:

THINK -> ACT -> OBSERVE -> THINK AGAIN

The agent uses deterministic GPA tools and keeps course
information in session memory.
"""

import json

from cse476.lanes import get_client, MODEL, describe

from gpa_tools import GPAMemory


# =========================================================
# CLIENT
# =========================================================

client = get_client()


# =========================================================
# SESSION MEMORY
# =========================================================

memory = GPAMemory()


# =========================================================
# TOOL FUNCTIONS
# =========================================================

def add_grade(
    course: str,
    grade: str,
    credits: float = 1.0,
) -> str:
    """
    Add or update a course grade in session memory.
    """

    return memory.add_grade(
        course=course,
        grade=grade,
        credits=credits,
    )


def compute_gpa() -> str:
    """
    Calculate the current credit-weighted GPA.
    """

    return memory.compute_gpa()


def remove_grade(course: str) -> str:
    """
    Remove a course grade from session memory.
    """
    if hasattr(memory, "remove_grade"):
        return memory.remove_grade(course)
    if course in memory.courses:
        del memory.courses[course]
        return f"Removed {course} from session memory."
    return f"Error: Course '{course}' not found in memory."


def calculate_target_gpa(
    target_gpa: float,
    remaining_credits: float,
) -> str:
    """
    Calculate the average grade point required in future
    courses to reach a target GPA.
    """

    return memory.calculate_target_gpa(
        target_gpa=target_gpa,
        remaining_credits=remaining_credits,
    )


def show_memory() -> str:
    """
    Show all courses currently stored in session memory.
    """
    return memory.get_course_details()


# =========================================================
# TOOL REGISTRY
# =========================================================

REGISTRY = {
    "add_grade": add_grade,
    "compute_gpa": compute_gpa,
    "calculate_target_gpa": calculate_target_gpa,
    "show_memory": show_memory,
    "remove_grade": remove_grade,
}


# =========================================================
# TOOL SCHEMAS
# =========================================================

TOOL_SCHEMA = [

    {
        "type": "function",
        "function": {
            "name": "add_grade",
            "description": (
                "Add or update a course grade in memory. "
                "Use this whenever the user provides a course "
                "and grade to record or update."
            ),
            "parameters": {
                "type": "object",
                "properties": {

                    "course": {
                        "type": "string",
                        "description": "Course name.",
                    },

                    "grade": {
                        "type": "string",
                        "description": (
                            "Grade. Valid grades are: "
                            "O, A+, A, B+, B, C, D, E, F."
                        ),
                    },

                    "credits": {
                        "type": "number",
                        "description": (
                            "Course credit value. "
                            "Default is 1 if not specified."
                        ),
                    },
                },
                "required": [
                    "course",
                    "grade",
                ],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "compute_gpa",
            "description": (
                "Calculate the student's current credit-weighted "
                "GPA using all grades stored in session memory."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_target_gpa",
            "description": (
                "Calculate the average grade point required "
                "in the remaining credits to reach a target GPA. "
                "Use this when the user asks what grades or "
                "average they need in future courses to reach "
                "a target GPA."
            ),
            "parameters": {
                "type": "object",
                "properties": {

                    "target_gpa": {
                        "type": "number",
                        "description": (
                            "Desired final GPA between 0 and 10."
                        ),
                    },

                    "remaining_credits": {
                        "type": "number",
                        "description": (
                            "Total credits remaining to complete."
                        ),
                    },
                },
                "required": [
                    "target_gpa",
                    "remaining_credits",
                ],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "show_memory",
            "description": (
                "View all courses, grades, and credits currently stored in session memory. "
                "Use this whenever the user asks to view, check, list, or inspect their courses, "
                "transcript, or course history."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "remove_grade",
            "description": (
                "Remove a course grade from session memory. Use this when the user asks "
                "to delete, remove, or drop a course."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "course": {
                        "type": "string",
                        "description": "Name of the course to remove.",
                    },
                },
                "required": ["course"],
            },
        },
    },
]


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM = """
You are an intelligent GPA Advisor.

You help students manage grades, calculate their current GPA,
and determine what academic performance they need to reach
a target GPA.

GRADE SCALE (Maximum grade is O = 10):

O  = 10 (Outstanding - HIGHEST possible grade on this scale, 10.0 grade points)
A+ = 9  (Excellent, 9.0 grade points)
A  = 8  (Very Good, 8.0 grade points)
B+ = 7  (Good, 7.0 grade points)
B  = 6  (Above Average, 6.0 grade points)
C  = 5  (Average, 5.0 grade points)
D  = 4  (Pass, 4.0 grade points)
E  = 0  (Fail, 0 grade points)
F  = 0  (Fail, 0 grade points)


AVAILABLE TOOLS:

1. add_grade
   Use when a user provides a course and grade to record.

2. compute_gpa
   Use when a user asks for current GPA or when GPA
   information is required.

3. calculate_target_gpa
   Use when a user asks what average or grades they need
   in future courses to reach a target GPA.
   If the user does not specify remaining credits in their question,
   immediately call calculate_target_gpa with target_gpa;
   do NOT stop to ask the user for remaining credits, as their active profile credits
   are automatically used by default.

4. show_memory
   Use when a user asks to see, check, review, or list their
   course history, recorded courses, or transcript.

5. remove_grade
   Use when a user asks to delete, remove, or drop a recorded course.


IMPORTANT RULES:

- Do not manually calculate GPA.
- Always use the appropriate tool for GPA calculations.
- ALWAYS invoke `compute_gpa` first when the user asks for their current GPA.
  Do NOT assume no courses exist; courses may have already been entered into session memory.
- When asked what grade or average is needed for a target GPA (e.g. "how much grade I need for 9.9"),
  immediately call `calculate_target_gpa(target_gpa=...)`. Do not stop to ask for remaining credits,
  as the student's active remaining credits from session memory are used by default.
- ALWAYS invoke `show_memory` when the user asks to check, review, or inspect their course history or recorded courses.
- NEVER add a course named 'History' or 'Course History' when the user is asking to check, view, or inspect course history.
- The MAXIMUM possible grade point on this scale is 10.0 for grade 'O' (Outstanding).
- Grade 'O' (10.0) is strictly HIGHER than 'A+' (9.0). NEVER claim that A+ (9.0) is the maximum grade!
- 10.0 is strictly GREATER than 9.97, 9.73, and any value below 10.0.
- If the required average returned by calculate_target_gpa is <= 10.0 (e.g. 9.73 or 9.97), it IS MATHEMATICALLY ACHIEVABLE by scoring grade 'O' (10.0). NEVER claim that a required average <= 10.0 is impossible!
- ONLY declare a target mathematically impossible if the required average returned by the tool is strictly GREATER than 10.0 (e.g. > 10.00).
- Always trust the `Status:` returned by `calculate_target_gpa`. If the tool says it is achievable, explain that it is achievable with grade 'O' (10.0).
- Never claim a grade is stored unless add_grade succeeded.
- Previously stored courses remain available in session memory.
- If the user provides multiple courses, store every course.
- Use tool results before deciding the next action.
- If information required for a calculation is missing after calling tools,
  ask the user for it.
- Clearly explain mathematically impossible GPA targets.
- Keep responses concise and helpful.

- When explaining a required future average grade point,
  never claim that a lower grade point is sufficient.
  Base the explanation strictly on the numerical result
  returned by the tool.

- Do not invent grade labels that are not present in the
  defined grade scale.

- When converting a required numerical average into advice,
  remember that the available grade points are discrete:
  10 = O, 9 = A+, 8 = A, 7 = B+, 6 = B,
  5 = C, 4 = D, 0 = E/F.

- If the required future average is between two grade points,
  explain that the student needs a combination of grades whose
  weighted average meets or exceeds the required value.
"""


# =========================================================
# AGENT LOOP
# =========================================================

def run_agent(
    goal: str,
    conversation_history: list | None = None,
    max_steps: int = 10,
    verbose: bool = True,
):
    """
    Run the GPA Advisor agent.

    Agent workflow:

    THINK -> ACT -> OBSERVE -> THINK AGAIN
    """

    # -----------------------------------------------------
    # CONVERSATION STATE
    # -----------------------------------------------------

    if conversation_history is None:

        messages = [
            {
                "role": "system",
                "content": SYSTEM,
            }
        ]

    else:

        messages = conversation_history.copy()

        # Ensure the system prompt is present.
        if (
            not messages
            or messages[0]["role"] != "system"
        ):

            messages.insert(
                0,
                {
                    "role": "system",
                    "content": SYSTEM,
                },
            )

    # Add the user's current request.
    messages.append(
        {
            "role": "user",
            "content": goal,
        }
    )


    # =====================================================
    # THINK -> ACT -> OBSERVE LOOP
    # =====================================================

    for step in range(1, max_steps + 1):

        # -------------------------------------------------
        # THINK
        # -------------------------------------------------

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMA,
        )

        message = response.choices[0].message

        # Save the assistant's response, including any
        # requested tool calls.
        messages.append(
            message.model_dump(
                exclude_none=True
            )
        )


        # -------------------------------------------------
        # DONE
        # -------------------------------------------------

        if not message.tool_calls:

            if verbose:

                print(
                    f"[step {step}] DONE"
                )

            return (
                message.content or "",
                messages,
            )


        # -------------------------------------------------
        # ACT
        # -------------------------------------------------

        for call in message.tool_calls:

            name = call.function.name

            try:

                args = json.loads(
                    call.function.arguments
                    or "{}"
                )

            except json.JSONDecodeError:

                args = {}

                result = (
                    "Error: Tool arguments could not be parsed."
                )

            else:

                # Tool whitelist.
                if name in REGISTRY:

                    try:

                        result = REGISTRY[name](
                            **args
                        )

                    except TypeError as error:

                        result = (
                            f"Error executing {name}: "
                            f"{error}"
                        )

                else:

                    result = (
                        f"Error: Unknown tool '{name}'. "
                        f"Available tools: "
                        f"{list(REGISTRY.keys())}"
                    )


            # -------------------------------------------------
            # TRACE
            # -------------------------------------------------

            if verbose:

                print(
                    f"\n[step {step}] "
                    f"TOOL: {name}({args})"
                )

                print(
                    f"[step {step}] "
                    f"RESULT:\n{result}"
                )


            # -------------------------------------------------
            # OBSERVE
            # -------------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )


    # =====================================================
    # SAFETY EXIT
    # =====================================================

    return (
        (
            f"Stopped after {max_steps} steps "
            "without reaching a final answer."
        ),
        messages,
    )


# =========================================================
# MEMORY HELPERS
# =========================================================

def show_memory() -> str:
    """
    Show all courses currently stored in memory.
    """

    return memory.get_course_details()


def clear_session() -> str:
    """
    Clear all GPA Advisor session memory.
    """

    return memory.clear_memory()


# =========================================================
# MAIN DEMONSTRATION
# =========================================================

if __name__ == "__main__":

    print(describe())

    print(
        "\n--- GPA ADVISOR "
        "MULTI-STEP DEMONSTRATION ---\n"
    )

    answer, history = run_agent(
        """
        Add Machine Learning with grade A and 4 credits.
        Add Deep Learning with grade A+ and 3 credits.
        Add Data Structures with grade B+ and 4 credits.

        Then calculate my current GPA.

        I have 20 credits remaining.
        What average grade point do I need to reach
        a final GPA of 8.5?
        """,
        verbose=True,
    )

    print(
        "\n--- FINAL ANSWER ---"
    )

    print(answer)

    print(
        "\n--- SESSION MEMORY ---"
    )

    print(show_memory())