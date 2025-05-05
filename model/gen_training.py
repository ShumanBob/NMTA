# generate a training file from `nmt_courses_latest.csv`

import random
from pathlib import Path
import pandas as pd


#  phrase banks for various questions

def make_templates():
    about = [
        "tell me about {}",
        "what can you tell me about {}",
        "tell me all about {}",
        "give me info on {}",
        "i'd like details on {}",
        "provide an overview of {}",
        "describe {}",
        "explain {}",
        "can you describe {} for me",
        "details for {}",
    ]
    who = [
        "who teaches {}",
        "who is teaching {} this semester",
        "who is the instructor for {}",
        "who's teaching {}",
        "who teaches {} in fall 2025",
        "who is the professor for {}",
    ]
    classes = [
        "what classes does {} teach",
        "which courses does {} teach",
        "list the courses taught by {} in fall 2025",
        "which classes does {} instruct this semester",
        "what does {} teach",
        "what courses is {} teaching",
    ]
    return about, who, classes


# clean string values
def clean(value) -> str:
    return "" if pd.isna(value) else str(value).strip()

# generate training data
def generate_lines(latest_csv: Path, out_csv: Path, target_lines: int = 100_000, seed: int = 42) -> None:
    random.seed(seed)
    df = pd.read_csv(latest_csv)
    # load phrase templates
    about_t, who_t, classes_t = make_templates()
    # get unique instructors from data file
    instructors = df["instructor"].dropna().unique().tolist()
    # open output file
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write("text\n") # write header
        count = 0

        while count < target_lines:
            # randomly sample one course from the dataset
            row = df.sample(1).iloc[0]

            code = clean(row["course_code"]).lower()
            title = clean(row["title"])
            title_lower = title.lower()
            # choose one of the three types of questions randomly
            intent = random.choice(["about", "who", "classes"])

            if intent == "about":
                # construct based on context
                location = clean(row["location"])
                days = clean(row["days"]).replace(" ", "")
                time_str = clean(row["time"])

                resp_parts = [
                    f"In 202620, the course '{title}' was taught by {clean(row['instructor'])}"
                ]
                if location:
                    resp_parts.append(f"at {location}")
                if days:
                    resp_parts.append(f"on {days}")
                if time_str:
                    resp_parts.append(f"at {time_str}")
                resp = " ".join(resp_parts) + "."

                q = random.choice(about_t).format(random.choice([code, title_lower]))

            elif intent == "who":
                # construct response with instructor
                resp = f"In 202620, '{title}' is taught by {clean(row['instructor'])}."
                q = random.choice(who_t).format(random.choice([code, title_lower]))

            else:
                # construct response list all classes for an instructor
                instr = random.choice(instructors)
                courses_by_instr = df[df["instructor"] == instr]
                course_str = "; ".join(
                    f"{r.course_code} – {r.title}" for _, r in courses_by_instr.iterrows()
                )
                resp = f"In 202620, {instr} teaches: {course_str}."
                q = random.choice(classes_t).format(instr.lower())
            # combine the question and answer into a single instruction block
            block = f"""### Instruction:
{q}

### Response:
{resp}

### End"""
            # escape quotes and write to file
            escaped_block = block.replace('"', '""')
            f.write(f'"{escaped_block}"\n')
            count += 1

    print("Finished")


# main
if __name__ == "__main__":
    # input and output paths
    latest_csv = Path("nmt_courses_latest.csv")
    out_csv = Path("nmt_courses_training.csv")
    generate_lines(latest_csv, out_csv)
