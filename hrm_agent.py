import os
from dotenv import load_dotenv
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def hr_feedback_agent(feedback_text):
    prompt = f"""
    You are an HR Employee Sentiment & Retention AI Agent.

    Analyze the following employee feedback:
    {feedback_text}

    Provide:
    1. Sentiment (Positive/Negative/Neutral)
    2. Key Issues
    3. Suggestions to Improve Satisfaction
    4. Attrition Risk (Low/Medium/High)
    """
    return ask_gpt(prompt)


def topic_modeling_agent(feedback_list):
    prompt = f"""
    You are an AI agent specializing in topic extraction.

    Extract 3–5 themes from this feedback dataset:
    {feedback_list}

    Provide each theme with:
    - Theme name
    - Summary
    """
    return ask_gpt(prompt)


def retention_report_agent(feedback_list):
    prompt = f"""
    You are an Employee Retention AI Analyst.

    Based on these feedback points:
    {feedback_list}

    Create an HR Retention Report including:
    - Top Pain Points
    - Root Causes
    - Recommended Actions
    - Impact on Retention
    - Priority Level
    """
    return ask_gpt(prompt)


def hr_chat_agent(query):
    prompt = f"""
    You are an HR Assistant AI Agent.

    The user asked: {query}

    Provide a clear HR-friendly response.
    """
    return ask_gpt(prompt)
def hr_document_generator(doc_type, employee_name, role, salary=None, reason=None):
    prompt = f"""
    You are an HR Document Generator AI.

    Create a {doc_type} for the employee with the following details:

    Employee Name: {employee_name}
    Role/Position: {role}
    Salary (if applicable): {salary}
    Reason (if applicable): {reason}

    The document should be:
    - Formally written
    - HR-compliant
    - Professional tone
    - Easy to read
    - Ready to copy-paste

    Format with proper paragraphs and spacing.
    """

    return ask_gpt(prompt)


def create_pdf(content, filename="document.pdf"):
    pdf_path = f"./{filename}"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    text = c.beginText(40, height - 50)
    text.setFont("Helvetica", 12)

    for line in content.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()

    return pdf_path
def performance_review_agent(employee_name, role, feedback):
    prompt = f"""
    You are a Performance Review AI Agent.

    Employee: {employee_name}
    Role: {role}

    Feedback:
    {feedback}

    Provide:
    - Performance Summary
    - Key Strengths
    - Areas of Improvement
    - SMART Goals
    - Promotion Readiness (Yes/No/Maybe)
    """
    return ask_gpt(prompt)

def hr_service_agent(query):
    prompt = f"""
    You are an HR Service Desk AI Agent.

    The employee asked:
    {query}

    Provide:
    - Clear answer (if policy-related)
    - OR ticket classification
    - Priority (High/Medium/Low)
    - Next action
    """
    return ask_gpt(prompt)
