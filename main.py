
"""
STUDENT PERFORMANCE ANALYSIS SYSTEM
Using Python Object-Oriented Programming

"""

from abc import ABC, abstractmethod
import csv
from pathlib import Path


# ==========================================
# 1. ABSTRACT STUDENT CLASS
# ==========================================

class Student(ABC):

    def __init__(self, student_id, name, scores):

        # Encapsulation: private attributes
        self.__student_id = student_id
        self.__name = name
        self.__scores = self.validate_scores(scores)

    @staticmethod
    def validate_scores(scores):

        if not scores:
            raise ValueError("Student must have scores.")

        scores = [float(score) for score in scores]

        if any(score < 0 or score > 100 for score in scores):
            raise ValueError("Marks must be between 0 and 100.")

        return scores

    # Getter methods

    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @property
    def scores(self):
        return tuple(self.__scores)

    # Flexible method demonstrating variable arguments

    def average(self, *additional_scores):

        all_scores = self.__scores + list(additional_scores)

        if any(float(score) < 0 or float(score) > 100
               for score in all_scores):
            raise ValueError("Marks must be between 0 and 100.")

        return sum(map(float, all_scores)) / len(all_scores)

    # Calculate grade

    def grade(self):

        average = self.average()

        if average >= 75:
            return "A"
        elif average >= 65:
            return "B"
        elif average >= 55:
            return "C"
        elif average >= 45:
            return "D"
        else:
            return "F"

    # Abstract methods

    @abstractmethod
    def scholarship_eligible(self):
        pass

    @abstractmethod
    def student_category(self):
        pass


# ==========================================
# 2. UNDERGRADUATE STUDENT CLASS
# ==========================================

class UndergraduateStudent(Student):

    # Method overriding

    def scholarship_eligible(self):

        return self.average() >= 75

    def student_category(self):

        return "Undergraduate"


# ==========================================
# 3. POSTGRADUATE STUDENT CLASS
# ==========================================

class PostgraduateStudent(Student):

    # Method overriding

    def scholarship_eligible(self):

        return self.average() >= 78

    def student_category(self):

        return "Postgraduate"


# ==========================================
# 4. PERFORMANCE ANALYZER CLASS
# ==========================================

class PerformanceAnalyzer:

    def __init__(self, students):

        if not students:
            raise ValueError("No student records found.")

        self.students = students

    # Highest-performing student

    def highest_performer(self):

        return max(
            self.students,
            key=lambda student: student.average()
        )

    # Lowest-performing student

    def lowest_performer(self):

        return min(
            self.students,
            key=lambda student: student.average()
        )

    # Overall class average

    def class_average(self):

        total = sum(
            student.average()
            for student in self.students
        )

        return total / len(self.students)

    # Generate performance report

    def generate_report(self):

        report = []

        report.append("STUDENT PERFORMANCE REPORT")
        report.append("=" * 72)

        report.append(
            f"{'ID':<8} {'NAME':<19} {'CATEGORY':<14} "
            f"{'AVERAGE':>8} {'GRADE':>6} {'SCHOLARSHIP':>13}"
        )

        report.append("-" * 72)

        for student in self.students:

            eligibility = (
                "Eligible"
                if student.scholarship_eligible()
                else "Not eligible"
            )

            report.append(
                f"{student.student_id:<8} "
                f"{student.name:<19} "
                f"{student.student_category():<14} "
                f"{student.average():>8.2f} "
                f"{student.grade():>6} "
                f"{eligibility:>13}"
            )

        highest = self.highest_performer()
        lowest = self.lowest_performer()

        report.append("-" * 72)
        report.append("CLASS SUMMARY")

        report.append(
            f"Total Students: {len(self.students)}"
        )

        report.append(
            f"Class Average: {self.class_average():.2f}%"
        )

        report.append(
            f"Highest Performer: {highest.name} "
            f"({highest.average():.2f}%)"
        )

        report.append(
            f"Lowest Performer: {lowest.name} "
            f"({lowest.average():.2f}%)"
        )

        report.append("")
        report.append("GRADE SCALE")
        report.append("A: 75-100")
        report.append("B: 65-74")
        report.append("C: 55-64")
        report.append("D: 45-54")
        report.append("F: Below 45")

        report.append("")
        report.append("SCHOLARSHIP REQUIREMENTS")
        report.append("Undergraduate: 75% and above")
        report.append("Postgraduate: 78% and above")

        return "\n".join(report)


# ==========================================
# 5. READ CSV DATASET
# ==========================================

def load_students(filename):

    students = []

    with open(filename, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            scores = [
                float(row["cat1"]),
                float(row["cat2"]),
                float(row["assignment"]),
                float(row["exam"])
            ]

            student_type = row["student_type"].lower()

            if student_type == "undergraduate":

                student = UndergraduateStudent(
                    row["student_id"],
                    row["name"],
                    scores
                )

            elif student_type == "postgraduate":

                student = PostgraduateStudent(
                    row["student_id"],
                    row["name"],
                    scores
                )

            else:
                raise ValueError(
                    f"Unknown student type: {student_type}"
                )

            students.append(student)

    return students


# ==========================================
# 6. MAIN PROGRAM
# ==========================================

def main():

    folder = Path(__file__).resolve().parent

    students = load_students(folder / "students.csv")

    analyzer = PerformanceAnalyzer(students)

    report = analyzer.generate_report()

    print(report)

    # Save report to text file

    output_file = folder / "performance_report.txt"

    output_file.write_text(
        report,
        encoding="utf-8"
    )

    print("\nReport successfully generated!")


if __name__ == "__main__":

    main()
