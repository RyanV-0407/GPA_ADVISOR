"""
Test script for the GPA Advisor Agent.

Tests:
1. Normal multi-step GPA + target GPA calculation
2. Memory persistence across separate conversation turns
3. Impossible target GPA edge case
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from gpa_agent import (
    run_agent,
    clear_session,
    show_memory,
)


def print_section(title):
    print("\n")
    print("=" * 70)
    print(title)
    print("=" * 70)


# =========================================================
# TEST 1: NORMAL MULTI-STEP AGENT BEHAVIOUR
# =========================================================

print_section(
    "TEST 1 - NORMAL MULTI-STEP GPA AND TARGET CALCULATION"
)

clear_session()

answer, history = run_agent(
    """
    Add Artificial Intelligence with grade A and 4 credits.
    Add Data Mining with grade B+ and 3 credits.
    Add Cloud Computing with grade A+ and 3 credits.

    Calculate my current GPA.

    I have 15 credits remaining.
    What average grade point do I need to reach a final GPA of 8.5?
    """,
    verbose=True,
)

print("\nFINAL ANSWER:")
print(answer)

print("\nMEMORY:")
print(show_memory())


# =========================================================
# TEST 2: MEMORY ACROSS SEPARATE TURNS
# =========================================================

print_section(
    "TEST 2 - MEMORY ACROSS SEPARATE TURNS"
)

clear_session()

history = None


print("\nTURN 1")
answer, history = run_agent(
    "Add Machine Learning with grade A and 4 credits.",
    conversation_history=history,
    verbose=True,
)

print("\nANSWER:")
print(answer)


print("\nTURN 2")
answer, history = run_agent(
    "Add Deep Learning with grade A+ and 3 credits.",
    conversation_history=history,
    verbose=True,
)

print("\nANSWER:")
print(answer)


print("\nTURN 3")
answer, history = run_agent(
    "What is my current GPA?",
    conversation_history=history,
    verbose=True,
)

print("\nFINAL ANSWER:")
print(answer)

print("\nMEMORY AFTER THREE TURNS:")
print(show_memory())


# =========================================================
# TEST 3: IMPOSSIBLE TARGET GPA
# =========================================================

print_section(
    "TEST 3 - IMPOSSIBLE TARGET GPA EDGE CASE"
)

clear_session()

answer, history = run_agent(
    """
    Add Database Systems with grade B and 10 credits.

    My current courses are complete except for 1 remaining credit.

    What average grade point do I need in that remaining
    1 credit to reach a final GPA of 10?
    """,
    verbose=True,
)

print("\nFINAL ANSWER:")
print(answer)

print("\nFINAL MEMORY:")
print(show_memory())


# =========================================================
# TEST COMPLETE
# =========================================================

print_section(
    "ALL TESTS COMPLETED"
)