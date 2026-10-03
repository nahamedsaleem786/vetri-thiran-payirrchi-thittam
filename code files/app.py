import html
import os

import requests
import streamlit as st

from utils.document_formatter import format_docx
from utils.pdf_formatter import format_pdf

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown(
    """
    <style>
    .hero { padding: 1rem 0 .4rem; text-align: center; }
    .hero h1 { font-size: 3rem; margin-bottom: .15rem; }
    .hero p { color: #777; font-size: 1.05rem; }
    .preview { border: 1px solid #777; border-radius: 12px; padding: 24px;
               min-height: 300px; white-space: pre-wrap; line-height: 1.65; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>⚖️ LegalEase</h1>
      <p>AI-Assisted Legal Document Generator</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Connection")
    st.caption(f"Backend: {BACKEND_URL}")
    if st.button("Check backend", use_container_width=True):
        try:
            health = requests.get(f"{BACKEND_URL}/health", timeout=5).json()
            if health.get("gemini_configured"):
                st.success(f"API ready • {health.get('model')}")
            else:
                st.warning("Backend is running, but GEMINI_API_KEY is not configured.")
        except requests.RequestException:
            st.error("FastAPI backend is not reachable.")

st.divider()

left, right = st.columns([1, 1])

with left:
    st.subheader("Document Details")
    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "General Agreement",
        ],
    )
    parties = st.text_area(
        "Parties Involved",
        placeholder="John Doe (Employee)\nABC Technologies (Employer)",
        height=130,
    )
    terms = st.text_area(
        "Terms & Conditions",
        placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
        height=180,
    )
    effective_date = st.date_input("Effective Date")
    generate = st.button("Generate Document", type="primary", use_container_width=True)

with right:
    st.subheader("How it works")
    st.info(
        "Enter the details, generate an AI-assisted draft, edit it, and download TXT, DOCX, or PDF."
    )
    st.markdown(
        """
        **Included**
        - FastAPI backend
        - Current Gemini SDK
        - Editable preview
        - TXT / DOCX / PDF export
        - Unicode-safe PDF export
        - Backend health check
        """
    )

if generate:
    if not parties.strip() or not terms.strip():
        st.warning("Please provide both parties and terms.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties.strip(),
            "terms": terms.strip(),
            "effective_date": effective_date.isoformat(),
        }
        with st.spinner("Generating document with Gemini..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=180,
                )
                response.raise_for_status()
                data = response.json()
                if data.get("success") and data.get("document"):
                    st.session_state.document = data["document"]
                    st.session_state.document_type = document_type
                    st.session_state.terms = terms
                    st.success("Document generated successfully.")
                else:
                    st.error("The backend did not return a document.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI. Start it with: uvicorn main:app --reload")
            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")
            except requests.exceptions.HTTPError as exc:
                try:
                    detail = response.json().get("detail", str(exc))
                except Exception:
                    detail = str(exc)
                st.error(f"Backend error: {detail}")
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")

if "document" in st.session_state:
    st.divider()
    st.subheader("Edit & Preview")
    edited = st.text_area(
        "Editable Document",
        value=st.session_state.document,
        height=550,
        key="document_editor",
    )
    st.session_state.document = edited

    safe_preview = html.escape(edited).replace("\n", "<br>")
    st.markdown(f'<div class="preview">{safe_preview}</div>', unsafe_allow_html=True)

    st.subheader("Download")
    try:
        txt_data = edited.encode("utf-8")
        docx_data = format_docx(edited, st.session_state.document_type, st.session_state.terms)
        pdf_data = format_pdf(edited, st.session_state.document_type)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("⬇️ TXT", txt_data, "legalease_document.txt", "text/plain", use_container_width=True)
        with c2:
            st.download_button(
                "⬇️ DOCX", docx_data, "legalease_document.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with c3:
            st.download_button("⬇️ PDF", pdf_data, "legalease_document.pdf", "application/pdf", use_container_width=True)
    except Exception as exc:
        st.error(f"Could not prepare downloads: {exc}")

st.divider()
st.caption("LegalEase creates AI-assisted drafts, not legal advice. Review documents with a qualified legal professional before actual use.")
