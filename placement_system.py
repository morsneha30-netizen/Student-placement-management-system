from collections import deque


class Student:
    def __init__(self, student_id, name, branch, cgpa):
        self.id = student_id
        self.name = name
        self.branch = branch
        self.cgpa = cgpa


class Company:
    def __init__(self, company_id, name, min_cgpa, required_branch):
        self.id = company_id
        self.name = name
        self.min_cgpa = min_cgpa
        self.required_branch = required_branch


class PlacementSystem:
    def __init__(self):
        # Phase 1: Student management
        self.students = []
        self.student_hash = {}

        # Phase 2: Company management
        self.companies = []
        self.company_hash = {}

        # Queue stores applications waiting to be processed
        self.application_queue = deque()

        # Keeps a record of all submitted applications
        self.application_history = []
        self.application_keys = set()

    def read_id(self, message):
        try:
            value = int(input(message))
            if value <= 0:
                print("ID must be a positive number.")
                return None
            return value
        except ValueError:
            print("Please enter a valid numeric ID.")
            return None

    def read_cgpa(self, message):
        try:
            value = float(input(message))
            if not 0 <= value <= 10:
                print("CGPA must be between 0 and 10.")
                return None
            return value
        except ValueError:
            print("Please enter a valid CGPA.")
            return None

    # ---------------- STUDENT MANAGEMENT ----------------

    def add_student(self):
        student_id = self.read_id("Enter Student ID: ")
        if student_id is None:
            return

        if student_id in self.student_hash:
            print("Student ID already exists.")
            return

        name = input("Enter Student Name: ").strip()
        branch = input("Enter Branch: ").strip()

        if not name or not branch:
            print("Name and branch cannot be empty.")
            return

        cgpa = self.read_cgpa("Enter CGPA: ")
        if cgpa is None:
            return

        student = Student(student_id, name, branch, cgpa)

        self.students.append(student)
        self.student_hash[student_id] = student

        print("Student added successfully.")

    def display_students(self):
        if not self.students:
            print("No student records found.")
            return

        print("\n" + "=" * 65)
        print(f"{'ID':<10}{'NAME':<25}{'BRANCH':<15}{'CGPA':>8}")
        print("=" * 65)

        for student in self.students:
            print(
                f"{student.id:<10}{student.name:<25}"
                f"{student.branch:<15}{student.cgpa:>8.2f}"
            )

    def search_student(self):
        student_id = self.read_id("Enter Student ID: ")
        if student_id is None:
            return

        student = self.student_hash.get(student_id)

        if student is None:
            print("Student not found.")
            return

        print("\nStudent Details")
        print("ID:", student.id)
        print("Name:", student.name)
        print("Branch:", student.branch)
        print(f"CGPA: {student.cgpa:.2f}")

    def sort_students(self):
        if not self.students:
            print("No students available to sort.")
            return

        self.students.sort(key=lambda student: student.cgpa, reverse=True)

        print("\nStudents sorted by CGPA (highest first):")
        self.display_students()

    # ---------------- COMPANY MANAGEMENT ----------------

    def add_company(self):
        company_id = self.read_id("Enter Company ID: ")
        if company_id is None:
            return

        if company_id in self.company_hash:
            print("Company ID already exists.")
            return

        name = input("Enter Company Name: ").strip()
        if not name:
            print("Company name cannot be empty.")
            return

        min_cgpa = self.read_cgpa("Enter Minimum CGPA: ")
        if min_cgpa is None:
            return

        branch = input("Enter Required Branch: ").strip()
        if not branch:
            print("Required branch cannot be empty.")
            return

        company = Company(company_id, name, min_cgpa, branch)

        self.companies.append(company)
        self.company_hash[company_id] = company

        print("Company added successfully.")

    def display_companies(self):
        if not self.companies:
            print("No company records found.")
            return

        print("\n" + "=" * 75)
        print(f"{'ID':<10}{'COMPANY':<25}{'MIN CGPA':<15}{'BRANCH':<20}")
        print("=" * 75)

        for company in self.companies:
            print(
                f"{company.id:<10}{company.name:<25}"
                f"{company.min_cgpa:<15.2f}{company.required_branch:<20}"
            )

    def search_company(self):
        company_id = self.read_id("Enter Company ID: ")
        if company_id is None:
            return

        company = self.company_hash.get(company_id)

        if company is None:
            print("Company not found.")
            return

        print("\nCompany Details")
        print("ID:", company.id)
        print("Name:", company.name)
        print(f"Minimum CGPA: {company.min_cgpa:.2f}")
        print("Required Branch:", company.required_branch)

    # ---------------- PLACEMENT ELIGIBILITY ----------------

    def is_eligible(self, student, company):
        cgpa_ok = student.cgpa >= company.min_cgpa
        branch_ok = (
            student.branch.strip().casefold()
            == company.required_branch.strip().casefold()
        )
        return cgpa_ok and branch_ok

    def check_eligibility(self):
        student_id = self.read_id("Enter Student ID: ")
        if student_id is None:
            return

        company_id = self.read_id("Enter Company ID: ")
        if company_id is None:
            return

        student = self.student_hash.get(student_id)
        company = self.company_hash.get(company_id)

        if student is None:
            print("Student not found.")
            return

        if company is None:
            print("Company not found.")
            return

        print("\nEligibility Result")
        print("-" * 35)
        print("Student:", student.name)
        print("Company:", company.name)
        print(f"Student CGPA: {student.cgpa:.2f}")
        print(f"Required CGPA: {company.min_cgpa:.2f}")
        print("Student Branch:", student.branch)
        print("Required Branch:", company.required_branch)

        if self.is_eligible(student, company):
            print("\nResult: ELIGIBLE")
        else:
            print("\nResult: NOT ELIGIBLE")

            if student.cgpa < company.min_cgpa:
                print("Reason: CGPA is below the requirement.")

            if student.branch.strip().casefold() != company.required_branch.strip().casefold():
                print("Reason: Branch does not match.")

    def display_eligible_students(self):
        company_id = self.read_id("Enter Company ID: ")
        if company_id is None:
            return

        company = self.company_hash.get(company_id)

        if company is None:
            print("Company not found.")
            return

        eligible = [
            student for student in self.students
            if self.is_eligible(student, company)
        ]

        print(f"\nEligible Students for {company.name}")
        print("-" * 50)

        if not eligible:
            print("No eligible students found.")
            return

        for student in eligible:
            print(
                f"ID: {student.id} | Name: {student.name} | "
                f"Branch: {student.branch} | CGPA: {student.cgpa:.2f}"
            )

        print("Total eligible students:", len(eligible))

    # ---------------- APPLICATION MANAGEMENT ----------------

    def apply_for_company(self):
        student_id = self.read_id("Enter Student ID: ")
        if student_id is None:
            return

        company_id = self.read_id("Enter Company ID: ")
        if company_id is None:
            return

        student = self.student_hash.get(student_id)
        company = self.company_hash.get(company_id)

        if student is None:
            print("Student not found.")
            return

        if company is None:
            print("Company not found.")
            return

        application_key = (student_id, company_id)

        if application_key in self.application_keys:
            print("This student has already applied to this company.")
            return

        if not self.is_eligible(student, company):
            print("Application rejected. Student is not eligible.")
            if student.cgpa < company.min_cgpa:
                print("Reason: CGPA does not meet the requirement.")
            if student.branch.strip().casefold() != company.required_branch.strip().casefold():
                print("Reason: Branch does not match.")
            return

        application = {
            "student_id": student.id,
            "student_name": student.name,
            "company_id": company.id,
            "company_name": company.name,
            "status": "Pending"
        }

        self.application_queue.append(application)
        self.application_history.append(application)
        self.application_keys.add(application_key)

        print("Application submitted successfully.")
        print("Application added to the processing queue.")

    def display_applications(self):
        if not self.application_history:
            print("No applications have been submitted.")
            return

        print("\n" + "=" * 90)
        print(
            f"{'STUDENT':<22}{'STUDENT ID':<13}"
            f"{'COMPANY':<22}{'COMPANY ID':<13}{'STATUS':<15}"
        )
        print("=" * 90)

        for app in self.application_history:
            print(
                f"{app['student_name']:<22}{app['student_id']:<13}"
                f"{app['company_name']:<22}{app['company_id']:<13}"
                f"{app['status']:<15}"
            )

        print("\nPending applications:", len(self.application_queue))

    def process_application(self):
        if not self.application_queue:
            print("No pending applications to process.")
            return

        # FIFO: first submitted, first processed
        application = self.application_queue.popleft()
        application["status"] = "Processed"

        print("\nApplication Processed Successfully")
        print("-" * 40)
        print("Student:", application["student_name"])
        print("Student ID:", application["student_id"])
        print("Company:", application["company_name"])
        print("Company ID:", application["company_id"])
        print("Status:", application["status"])
        print("Remaining pending applications:", len(self.application_queue))

    # ---------------- MAIN MENU ----------------

    def menu(self):
        while True:
            print("\n" + "=" * 48)
            print("       STUDENT PLACEMENT MANAGEMENT")
            print("=" * 48)

            print("\n--- Student Management ---")
            print("1. Add Student")
            print("2. Display Students")
            print("3. Search Student")
            print("4. Sort Students by CGPA")

            print("\n--- Company Management ---")
            print("5. Add Company")
            print("6. Display Companies")
            print("7. Search Company")

            print("\n--- Placement Management ---")
            print("8. Check Eligibility")
            print("9. Display Eligible Students")
            print("10. Apply for Company")
            print("11. Display Applications")
            print("12. Process Application")

            print("\n0. Exit")

            choice = input("\nEnter your choice: ").strip()

            actions = {
                "1": self.add_student,
                "2": self.display_students,
                "3": self.search_student,
                "4": self.sort_students,
                "5": self.add_company,
                "6": self.display_companies,
                "7": self.search_company,
                "8": self.check_eligibility,
                "9": self.display_eligible_students,
                "10": self.apply_for_company,
                "11": self.display_applications,
                "12": self.process_application
            }

            if choice == "0":
                print("Thank you for using the Placement Management System.")
                break

            action = actions.get(choice)

            if action:
                action()
            else:
                print("Invalid choice. Please select a valid menu option.")


if __name__ == "__main__":
    system = PlacementSystem()
    system.menu()