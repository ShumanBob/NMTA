import re

def main():
        
        course_list = [] # will be used to store course objects
        with open("courses.txt", 'r', encoding='utf-8') as file:
                content = file.read()

        # Split courses using delimiter "-@-"
        raw_courses = content.split('-@-')

        # Clean up each course entry by stripping newlines and extra spaces
        courses = [' '.join(course.split()) for course in raw_courses if course.strip()]

        
        for course in courses:
                course_info = []
                # Extracting course code(s)
                match = re.match(r"([A-Z]+\s\d+(?:,\s\d+D)*)", course)
                if match:
                        course_code = match.group(1)
                        course_info.append(course_code)
                else:
                        course_info.append("Unknown Code")

                # Extracting course title
                remaining_text = course[len(course_code):].strip(", ")  # Remove extracted code and trim commas/spaces
                title_match = re.match(r"([A-Za-z\s\-]+)", remaining_text)  # Match only title words
                if title_match:
                        course_title = title_match.group(1).strip()
                        course_info.append(course_title)
                else:
                        course_info.append("Unknown Title")

                # Extracting credit hours
                credit_match = re.search(r"(\d+)\s*cr", course)  # Look for a number followed by "cr"
                if credit_match:
                        credit_hours = int(credit_match.group(1))  # Convert to integer
                        course_info.append(credit_hours)
                else:
                        course_info.append(0)  # Default to 0 if no credit hours found


                # Extracting semester of year (Fall, Spring, Both)
                semester_match = re.search(r"\b(Fall|Spring|Both)\b", course, re.IGNORECASE)
                if semester_match:
                        semester_offered = semester_match.group(1)  # Fall, Spring, or Both
                        if semester_offered == 'both':
                                course_info.append("Fall/Spring")
                        else:
                                course_info.append(semester_offered)
                else:
                        course_info.append("Unknown Time Offered")  # Default if no semester found


                # Extracting prerequisites (if any)
                prereqs_match = re.search(r"Pre?-?requisite?s?:\s*([\w\s,;]+)", course)
                if prereqs_match:
                        prereqs_text = prereqs_match.group(1)
                        prereqs = re.findall(r"[A-Z]+\s?\d+L?", prereqs_text)  # change +\s to *\s
                        course_info.append(prereqs)
                else:
                        course_info.append([])  # No prerequisites


                # Extracting corequisites (if any)
                coreqs_match = re.search(r"Co?-?requisite?s?:\s*([\w\s,;]+)", course)
                if coreqs_match:
                        coreqs_text = coreqs_match.group(1)
                        # Extracting only course codes, ignoring extra terms like "grade of C or higher"
                        coreqs = re.findall(r"[A-Z]+\s?\d+L?", coreqs_text, re.IGNORECASE)
                        course_info.append(coreqs)
                else:
                        course_info.append([])  # No corequisites


                time_match = re.findall(r"([MTWRF]+)\s+(\d{1,2}:\d{2}\s*[ap]m\s*-\s*\d{1,2}:\d{2}\s*[ap]m?\s[Lb]?)", course)
                if time_match:
                        course_info.append(time_match)
                else:
                        course_info.append([])  # No times

                # Create Course object from course_info list
                #print(course_info)
                course_c = Course(course_info[0],course_info[1],course_info[2],course_info[3],course_info[4],course_info[5],course_info[6])
                course_list.append(course_c)

        return course_list

# prints course objects and all their info stored in the course_list
def print_courses(course_list):

        for course in course_list:
                print(f"Course Code: {course.course_code}")
                print(f"Course Name: {course.name}")
                print(f"Credit Hours: {course.credit_hours}")
                print(f"Semester Offered: {course.time_offered}")
                print(f"Prerequisites: {', '.join(course.prereqs) if course.prereqs else 'None'}")
                print(f"Corequisites: {', '.join(course.coreqs) if course.coreqs else 'None'}")
                
                if course.class_time:
                        print("Class Times:")
                        for days, time in course.class_time:
                                print(f"  {days}: {time}")
                else:
                        print("Class Times: None")

                print("-" * 50)  # Separator for readability



       
class Course:
        def __init__(self, course_code, name, credit_hours, time_offered=None, prereqs=None, coreqs=None, class_time=None):
                self.course_code = course_code
                self.name = name
                self.credit_hours = credit_hours
                self.time_offered = time_offered
                self.prereqs = prereqs if prereqs else []
                self.coreqs = coreqs if coreqs else []
                self.class_time = class_time if class_time else []


if __name__ == "__main__":
        main()
