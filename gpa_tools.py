"""
GPA Advisor - Tools and session memory.

Uses the LPU-style grade-point scale and credit-weighted GPA calculation.
"""


GRADE_POINTS = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "D": 4,
    "E": 0,
    "F": 0,
}


class GPAMemory:
    """
    Stores course grades and credits for one GPA Advisor session.
    """

    def __init__(self):
        self.courses = {}

    def add_grade(
        self,
        course: str,
        grade: str,
        credits: float = 1.0,
    ) -> str:

        course = course.strip()
        grade = grade.strip().upper()

        if not course:
            return "Error: Course name cannot be empty."

        if grade not in GRADE_POINTS:
            valid_grades = ", ".join(GRADE_POINTS.keys())

            return (
                f"Error: Unsupported grade '{grade}'. "
                f"Valid grades are: {valid_grades}."
            )

        try:
            credits = float(credits)
        except (TypeError, ValueError):
            return "Error: Credits must be a valid number."

        if credits <= 0:
            return "Error: Credits must be greater than 0."

        if course in self.courses:

            old_data = self.courses[course]

            self.courses[course] = {
                "grade": grade,
                "credits": credits,
            }

            return (
                f"Updated {course}. "
                f"Old grade: {old_data['grade']}, "
                f"new grade: {grade}, "
                f"credits: {credits}."
            )

        self.courses[course] = {
            "grade": grade,
            "credits": credits,
        }

        return (
            f"Added {course} with grade {grade} "
            f"and {credits} credits."
        )

    def remove_grade(self, course: str) -> str:
        """Remove a course from session memory."""
        course = course.strip()
        if course in self.courses:
            del self.courses[course]
            return f"Removed {course} from session memory."
        return f"Error: Course '{course}' not found in memory."

    def get_current_gpa_data(self) -> dict:

        if not self.courses:
            return {
                "gpa": None,
                "total_credits": 0,
                "total_weighted_points": 0,
                "course_count": 0,
            }

        total_weighted_points = 0
        total_credits = 0

        for course_data in self.courses.values():

            grade_point = GRADE_POINTS[
                course_data["grade"]
            ]

            credits = course_data["credits"]

            total_weighted_points += (
                grade_point * credits
            )

            total_credits += credits

        gpa = (
            total_weighted_points / total_credits
        )

        return {
            "gpa": gpa,
            "total_credits": total_credits,
            "total_weighted_points": total_weighted_points,
            "course_count": len(self.courses),
        }

    def compute_gpa(self) -> str:

        data = self.get_current_gpa_data()

        if data["gpa"] is None:
            return (
                "No courses have been added yet. "
                "Please add at least one course first."
            )

        return (
            f"Current GPA: {data['gpa']:.2f}\n"
            f"Courses counted: {data['course_count']}\n"
            f"Total credits: {data['total_credits']}"
        )

    def calculate_target_gpa(
        self,
        target_gpa: float,
        remaining_credits: float,
    ) -> str:
        """
        Calculate the average grade point required over
        the remaining credits to reach a target GPA.
        """

        if not self.courses:
            return (
                "Error: No completed courses are stored. "
                "Add your completed course grades first."
            )

        try:
            target_gpa = float(target_gpa)
            remaining_credits = float(remaining_credits)

        except (TypeError, ValueError):
            return (
                "Error: Target GPA and remaining credits "
                "must be valid numbers."
            )

        if target_gpa < 0 or target_gpa > 10:
            return (
                "Error: Target GPA must be between 0 and 10."
            )

        if remaining_credits <= 0:
            return (
                "Error: Remaining credits must be greater than 0."
            )

        current = self.get_current_gpa_data()

        current_points = (
            current["total_weighted_points"]
        )

        current_credits = (
            current["total_credits"]
        )

        final_credits = (
            current_credits + remaining_credits
        )

        points_needed_total = (
            target_gpa * final_credits
        )

        future_points_needed = (
            points_needed_total - current_points
        )

        required_average = (
            future_points_needed / remaining_credits
        )

        # Target already guaranteed.
        if required_average <= 0:

            return (
                f"Target GPA: {target_gpa:.2f}\n"
                f"Current GPA: {current['gpa']:.2f}\n"
                f"Remaining credits: {remaining_credits}\n\n"
                "You have already earned enough grade points "
                "to reach this target, even before future courses."
            )

        # Impossible target.
        if required_average > 10:

            return (
                f"Target GPA: {target_gpa:.2f}\n"
                f"Current GPA: {current['gpa']:.2f}\n"
                f"Remaining credits: {remaining_credits}\n\n"
                f"Required future average: {required_average:.2f}/10\n"
                f"Status: Mathematically IMPOSSIBLE because the required average ({required_average:.2f}) "
                f"exceeds the maximum possible grade point of 10.0 (Grade O)."
            )

        return (
            f"Target GPA: {target_gpa:.2f}\n"
            f"Current GPA: {current['gpa']:.2f}\n"
            f"Completed credits: {current_credits}\n"
            f"Remaining credits: {remaining_credits}\n"
            f"Required average grade point in remaining courses: {required_average:.2f}/10\n"
            f"Status: Mathematically ACHIEVABLE because the required average ({required_average:.2f}) "
            f"is <= the maximum possible grade point of 10.0 (Grade O).\n"
            f"Advice: The student can reach this target by earning grade O (10.0 points) in their remaining courses."
        )

    def get_course_details(self) -> str:

        if not self.courses:
            return (
                "No courses are currently stored in memory."
            )

        details = []

        for course, data in self.courses.items():

            details.append(
                f"{course}: "
                f"Grade {data['grade']}, "
                f"Credits {data['credits']}"
            )

        return "\n".join(details)

    def clear_memory(self) -> str:

        self.courses.clear()

        return "All GPA Advisor memory has been cleared."