from gpa_tools import GPAMemory


memory = GPAMemory()

print(memory.add_grade("Machine Learning", "A", 4))
print(memory.add_grade("Deep Learning", "A+", 3))
print(memory.add_grade("Data Structures", "B+", 4))

print("\n--- STORED COURSES ---")
print(memory.get_course_details())

print("\n--- GPA ---")
print(memory.compute_gpa())

print("\n--- STRUCTURED GPA DATA ---")
print(memory.get_current_gpa_data())