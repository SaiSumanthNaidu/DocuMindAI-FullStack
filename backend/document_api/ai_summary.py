import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_resume_summary(text):
    prompt = f"""
    You are an HR recruiter.

    Generate a professional summary
    for the following resume:

    {text}
    """

    response = model.generate_content(prompt)

    return response.text