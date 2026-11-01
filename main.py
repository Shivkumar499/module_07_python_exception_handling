import json

class StudentRecordError(Exception):
    pass

valid = []
errors = []
ids = set() #isd=student id

try:
    file = open("students_input.json", "r")
    data = json.load(file)
    file.close()

except FileNotFoundError:
    print("Input file not found.")

except PermissionError:
    print("Permission denied.")

except json.JSONDecodeError:
    print("Invalid JSON file.")

except OSError as e:
    print("File error:", e)

else:
    for i, student in enumerate(data, 1):
        try:
            if not isinstance(student, dict):
                raise TypeError("Record must be a dictionary")

            sid = student["student_id"]
            name = student["name"]
            dept = student["department"]
            marks = student["marks"]

            if not isinstance(sid, str) or not sid:
                raise ValueError("Invalid student ID")

            if not isinstance(name, str) or not name:
                raise ValueError("Invalid name")

            if not isinstance(dept, str) or not dept:
                raise ValueError("Invalid department")

            if sid in ids:
                raise StudentRecordError("Duplicate student ID")

            if not isinstance(marks, list) or len(marks) != 3:
                raise StudentRecordError(
                    "Marks must contain exactly 3 values"
                )

            for mark in marks:
                if type(mark) not in (int, float):
                    raise StudentRecordError("Invalid marks")

                if mark < 0 or mark > 100:
                    raise StudentRecordError("Marks must be 0 to 100")

            ids.add(sid)
            valid.append(student)
            print("Accepted:", sid, "-", name)

        except KeyError as e:
            errors.append(f"Record {i}: Missing field {e}")
            print("Rejected record", i)

        except (TypeError, ValueError, StudentRecordError) as e:
            errors.append(f"Record {i}: {e}")
            print("Rejected record", i, ":", e)

    with open("student_valid.json", "w") as f:
        json.dump(valid, f, indent=4)

    with open("import_errors.txt", "w") as f:
        f.write("\n".join(errors))

    print("\nImport completed.")
    print("Accepted records:", len(valid))
    print("Rejected records:", len(errors))
    print("Valid output: student_valid.json")
    print("Error log: import_errors.txt")

finally:
    print("Program finished.")