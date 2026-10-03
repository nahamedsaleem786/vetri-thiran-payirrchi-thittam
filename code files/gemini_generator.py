import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash"


class GeminiDocumentGenerator:
    """Generate AI-assisted legal document drafts with Google's current SDK."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = (api_key or os.getenv("GEMINI_API_KEY", "")).strip()
        self.model_name = (model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)).strip()

        if not self.api_key:
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

    @property
    def configured(self) -> bool:
        return self.client is not None

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        if not self.client:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Create a .env file from "
                ".env.example and add your Google Gemini API key."
            )

        prompt = f"""You are LegalEase, an AI-assisted legal document drafting system.

Draft a professional {document_type} using ONLY the facts supplied below.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE:
{effective_date}

REQUIREMENTS:
- Start with a clear document title.
- Identify all supplied parties and the effective date.
- Organize clauses with numbered headings.
- Preserve the supplied terms accurately.
- Do not invent names, addresses, amounts, dates, duties, rights, or facts.
- If essential information is missing, use [TO BE COMPLETED].
- Use clear, formal, plain English.
- Include a short Important Notice stating that this is an AI-assisted draft and
  should be reviewed by a qualified legal professional before actual use.
- Return only the document text, without markdown code fences.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=8192,
                ),
            )
        except Exception as exc:
            raise RuntimeError(f"Gemini API request failed: {exc}") from exc

        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()
