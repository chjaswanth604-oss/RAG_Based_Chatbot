import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are an AI College Information Assistant.

Answer the student's question using ONLY the provided college knowledge base context.

Do not invent information.

If the answer cannot be found in the provided context, clearly tell the student that the information is not available in the college knowledge base.

Always provide a concise, polite, and useful answer."""

def generate_llm_answer(question: str, context: str) -> str:
    """
    Sends retrieved context and student question to Groq API.
    If GROQ_API_KEY is missing or API call fails, falls back gracefully to context summary or helpful error.
    """
    if not context or context.strip() == "":
        return "I couldn't find this information in the college knowledge base. Please contact the concerned college department for accurate information."

    user_prompt = f"""Retrieved Context:
{context}

Student Question:
{question}"""

    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        logger.warning("GROQ_API_KEY not found in environment. Generating context-based summary.")
        # Context-based fallback answer generation when API key is not configured yet
        return f"Based on college documents:\n{context[:600]}...\n\n(Note: Add GROQ_API_KEY to backend/.env for full LLM synthesis)."

    try:
        # Try using groq Python package if installed, or fallback to requests HTTP call
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=600
            )
            return completion.choices[0].message.content.strip()
        except ImportError:
            # Fallback to direct HTTP request
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 600
            }
            resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                logger.error(f"Groq API call error: {resp.status_code} - {resp.text}")
                return f"Based on retrieved college documents:\n{context[:500]}..."
    except Exception as e:
        logger.error(f"LLM generation exception: {e}")
        return f"Based on retrieved college documents:\n{context[:500]}..."
