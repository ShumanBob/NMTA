def main():
        with open("file_reading_test\courses.txt" , "r", encoding="utf-8") as file:
                lines = file.readlines()
        content = "".join(lines)
        course_list = content.split("-@-")
        course_list = [course.strip() for course in course_list if course.strip()]
        for courses in course_list:
                print("-------------")
                print(courses)

if __name__ == "__main__":
        main()