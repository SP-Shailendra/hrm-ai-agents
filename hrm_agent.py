import os
import streamlit as st
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# -----------------------------
# Unified Groq client
# -----------------------------
def get_client():
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    base_url = os.getenv("GROQ_BASE_URL") or st.secrets.get(
        "GROQ_BASE_URL", "https://api.groq.com/openai/v1"
    )

    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in environment or Streamlit secrets")

    return OpenAI(api_key=api_key, base_url=base_url)


def get_model():
    return os.getenv("GROQ_MODEL") or st.secrets.get(
        "GROQ_MODEL", "llama-3.3-70b-versatile"
    )


client = get_client()
model = get_model()

# -----------------------------
# LLM call
# -----------------------------
def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# -----------------------------
# Agents
# -----------------------------
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
    return ask_llm(prompt)


def topic_modeling_agent(feedback_list):
    prompt = f"""
You are an AI agent specializing in topic extraction.

Extract 3–5 themes from this feedback dataset:
{feedback_list}

Provide each theme with:
- Theme name
- Summary
"""
    return ask_llm(prompt)


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
    return ask_llm(prompt)


def hr_chat_agent(query):
    prompt = f"""
You are an HR Assistant AI Agent.

The user asked:
{query}

Provide a clear HR-friendly response.
"""
    return ask_llm(prompt)


def hr_document_generator(doc_type, employee_name, role, salary=None, reason=None):
    prompt = f"""
You are an HR Document Generator AI.

Create a {doc_type} for the employee:

Employee Name: {employee_name}
Role: {role}
Salary: {salary}
Reason: {reason}

Professional, HR-compliant, and ready to use.
"""
    return ask_llm(prompt)


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
- Promotion Readiness
"""
    return ask_llm(prompt)



# -----------------------------
# PDF helper (unchanged)
# -----------------------------
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

