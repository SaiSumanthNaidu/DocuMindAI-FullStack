import re


def extract_email(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    match = re.search(email_pattern, text)

    return match.group() if match else ""


def extract_phone(text):
    phone_pattern = r'(\+91[-\s]?)?[6-9]\d{9}'
    match = re.search(phone_pattern, text)

    return match.group() if match else ""


def extract_name(text):
    lines = text.split('\n')

    for line in lines:
        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:
            return line

    return ""

SKILLS_DB = [
    "Python",
    "Django",
    "Flask",
    "FastAPI",
    "Java",
    "JavaScript",
    "React",
    "MySQL",
    "MongoDB",
    "HTML",
    "CSS",
    "Git",
    "Docker",
    "AWS",
    "Linux",
]


def extract_skills(text):
    found_skills = []

    for skill in SKILLS_DB:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills