
import streamlit as st
import pandas as pd
import json
import tempfile
from pathlib import Path
from datetime import date
from decimal import Decimal, InvalidOperation

st.set_page_config(
    page_title="DocuStruct AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- DESIGN ----------
st.markdown("""
<style>
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 1250px;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.2);
    }

    .hero {
        padding: 1.6rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #173B57, #286A83);
        color: white;
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        color: white;
        margin-bottom: 0.35rem;
    }

    .hero p {
        color: #E4EFF6;
        margin-bottom: 0;
    }

    .section-label {
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #4486A2;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.22);
        padding: 15px;
        border-radius: 12px;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    .note {
        border-radius: 10px;
        padding: 12px 14px;
        background: rgba(128,128,128,0.09);
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------- SAMPLE DATA ----------
SAMPLE_INVOICE = {
    "invoice_number": "INV-001",
    "vendor": "ABC Traders",
    "invoice_date": "2026-10-20",
    "due_date": "2026-11-20",
    "subtotal": 1000.00,
    "tax": 180.00,
    "total": 1180.00,
}

FIELDS = [
    "invoice_number",
    "vendor",
    "invoice_date",
    "due_date",
    "subtotal",
    "tax",
    "total",
]


# ---------- VALIDATION ----------
def validate_invoice(data):
    errors = []
    required = FIELDS

    for field in required:
        value = data.get(field)

        if value is None or str(value).strip() == "":
            errors.append(f"{field}: Missing required value.")

    parsed_dates = {}

    for field in ["invoice_date", "due_date"]:
        value = data.get(field)

        if value is not None and str(value).strip():
            try:
                parsed_dates[field] = date.fromisoformat(str(value))
            except (ValueError, TypeError):
                errors.append(
                    f"{field}: Use YYYY-MM-DD format."
                )

    amounts = {}

    for field in ["subtotal", "tax", "total"]:
        value = data.get(field)

        if value is not None and str(value).strip():
            try:
                amount = Decimal(str(value))

                if not amount.is_finite():
                    raise InvalidOperation

                amounts[field] = amount

                if amount < 0:
                    errors.append(
                        f"{field}: Amount cannot be negative."
                    )

            except (InvalidOperation, ValueError, TypeError):
                errors.append(
                    f"{field}: Enter a valid numeric amount."
                )

    if all(
        field in amounts
        for field in ["subtotal", "tax", "total"]
    ):
        if all(
            amounts[field] >= 0
            for field in ["subtotal", "tax", "total"]
        ):
            expected = amounts["subtotal"] + amounts["tax"]

            if abs(expected - amounts["total"]) > Decimal("0.02"):
                errors.append(
                    "Total does not equal subtotal + tax."
                )

    if "invoice_date" in parsed_dates and "due_date" in parsed_dates:
        if parsed_dates["due_date"] < parsed_dates["invoice_date"]:
            errors.append(
                "Due date is earlier than invoice date."
            )

    return errors


def format_amount(value):
    try:
        amount = Decimal(str(value))
        if amount.is_finite():
            return f"{amount:,.2f}"
    except (InvalidOperation, ValueError, TypeError):
        pass

    return "—"


# ---------- SESSION STATE ----------
if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = None

if "source_name" not in st.session_state:
    st.session_state.source_name = "Sample invoice"

if "reviewed" not in st.session_state:
    st.session_state.reviewed = False


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 📄 DocuStruct AI")
    st.caption("PDF → Validated Data")
    st.divider()

    st.markdown("### Workflow")
    st.markdown("1. 📤 Upload invoice")
    st.markdown("2. 📝 Review extracted data")
    st.markdown("3. ✅ Validate fields")
    st.markdown("4. 📥 Export results")

    st.divider()

    st.markdown("### Development status")
    st.success("UI ready")
    st.success("Validation ready")
    st.success("JSON / CSV export ready")
    st.success("Extraction code connected")
    st.caption("Ollama must be running locally for AI extraction.")

    st.divider()

    if st.button("Load sample invoice", use_container_width=True):
        st.session_state.invoice_data = SAMPLE_INVOICE.copy()
        st.session_state.source_name = "Sample invoice"
        st.session_state.reviewed = False
        st.rerun()

    st.caption("Prototype · Invoice processing")


# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <div style="font-size:0.85rem;letter-spacing:0.1em;">
        INTELLIGENT DOCUMENT PROCESSING
    </div>
    <h1>Invoice workspace</h1>
    <p>Extract, validate, review, and export invoice data in one place.</p>
</div>
""", unsafe_allow_html=True)


# ---------- TOP METRICS ----------
current_data = st.session_state.invoice_data

if current_data is None:
    metric_status = "Waiting"
    metric_vendor = "—"
    metric_total = "—"
    metric_issues = "—"
else:
    current_errors = validate_invoice(current_data)
    metric_status = "Needs review" if current_errors else "Valid"
    metric_vendor = str(current_data.get("vendor") or "—")
    metric_total = format_amount(current_data.get("total"))
    metric_issues = str(len(current_errors))

c1, c2, c3, c4 = st.columns(4)

c1.metric("Document status", metric_status)
c2.metric("Vendor", metric_vendor)
c3.metric("Invoice total", metric_total)
c4.metric("Validation issues", metric_issues)

st.divider()


# ---------- UPLOAD ----------
st.markdown('<div class="section-label">Step 01</div>',
            unsafe_allow_html=True)
st.subheader("Upload invoice")

uploaded_file = st.file_uploader(
    "Choose an invoice PDF",
    type=["pdf"],
    help="Upload a text-based PDF invoice.",
)

if uploaded_file:
    st.info(f"Selected file: {uploaded_file.name}")

    if st.button("Extract invoice data", type="primary"):
        try:
            # Import here so the UI can show a clear error if extractor.py is missing.
            from extractor import analyze_invoice

            # The backend accepts a file path; Streamlit's upload is file-like.
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                temp_pdf.write(uploaded_file.getvalue())
                temp_pdf_path = temp_pdf.name

            try:
                with st.spinner("Reading PDF and extracting invoice fields with AI..."):
                    extracted_data = analyze_invoice(temp_pdf_path)
            finally:
                Path(temp_pdf_path).unlink(missing_ok=True)

            # Keep only the fields used by the review, validation, and export UI.
            st.session_state.invoice_data = {
                field: extracted_data.get(field) for field in FIELDS
            }
            st.session_state.source_name = uploaded_file.name
            st.session_state.reviewed = False
            st.success("Extraction finished. Please review every field before exporting.")
            st.rerun()

        except Exception as exc:
            st.error(
                "Could not extract this invoice. Check that extractor.py and its "
                "dependencies are in the project folder, and that Ollama is running "
                "with the qwen3.5:4b model installed."
            )
            st.caption(f"Technical details: {exc}")

    if st.button("Use sample data for now"):
        st.session_state.invoice_data = SAMPLE_INVOICE.copy()
        st.session_state.source_name = uploaded_file.name
        st.session_state.reviewed = False
        st.rerun()

st.markdown(
    '<div class="note">You can use the sample invoice from the sidebar '
    'to test the review, validation, and export workflow. '
    'Real PDF extraction will be enabled during backend integration.</div>',
    unsafe_allow_html=True,
)

# ---------- REVIEW ----------
if st.session_state.invoice_data is not None:
    data = st.session_state.invoice_data

    st.divider()
    st.markdown('<div class="section-label">Step 02</div>',
                unsafe_allow_html=True)
    st.subheader("Review invoice details")
    st.caption(
        f"Source: {st.session_state.source_name} · "
        "Check the values before exporting."
    )

    with st.form("invoice_review"):
        left, right = st.columns(2)

        with left:
            invoice_number = st.text_input(
                "Invoice number",
                value=str(data.get("invoice_number") or ""),
            )
            vendor = st.text_input(
                "Vendor name",
                value=str(data.get("vendor") or ""),
            )
            invoice_date = st.text_input(
                "Invoice date (YYYY-MM-DD)",
                value=str(data.get("invoice_date") or ""),
            )
            subtotal = st.text_input(
                "Subtotal",
                value=str(data.get("subtotal") or ""),
            )

        with right:
            due_date = st.text_input(
                "Due date (YYYY-MM-DD)",
                value=str(data.get("due_date") or ""),
            )
            tax = st.text_input(
                "Tax",
                value=str(data.get("tax") or ""),
            )
            total = st.text_input(
                "Total",
                value=str(data.get("total") or ""),
            )

        submitted = st.form_submit_button(
            "Save reviewed invoice",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        st.session_state.invoice_data = {
            "invoice_number": invoice_number.strip(),
            "vendor": vendor.strip(),
            "invoice_date": invoice_date.strip(),
            "due_date": due_date.strip(),
            "subtotal": subtotal.strip(),
            "tax": tax.strip(),
            "total": total.strip(),
        }

        st.session_state.reviewed = True
        st.rerun()

    # Refresh data after a possible save
    data = st.session_state.invoice_data
    errors = validate_invoice(data)

    # ---------- VALIDATION ----------
    st.divider()
    st.markdown('<div class="section-label">Step 03</div>',
                unsafe_allow_html=True)
    st.subheader("Validation results")

    if errors:
        st.warning(
            f"{len(errors)} validation issue(s) found. "
            "Review the messages below."
        )

        for error in errors:
            st.markdown(f"- {error}")
    else:
        st.success("All current validation checks passed.")

    if st.session_state.reviewed:
        st.caption("Your latest form submission has been saved.")

    # ---------- EXPORT ----------
    st.divider()
    st.markdown('<div class="section-label">Step 04</div>',
                unsafe_allow_html=True)
    st.subheader("Export reviewed data")
    st.caption(
        "Exports use the current saved values, including any corrections."
    )

    json_data = json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
        default=str,
    )

    csv_data = pd.DataFrame([data], columns=FIELDS).to_csv(index=False)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "⬇ Download JSON",
            data=json_data,
            file_name="invoice.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "⬇ Download CSV",
            data=csv_data,
            file_name="invoice.csv",
            mime="text/csv",
            use_container_width=True,
        )

    if errors:
        st.info(
            "This invoice still has validation issues. "
            "You can download it for review, but it is not yet validated."
        )

else:
    st.divider()
    st.info(
        "No invoice loaded yet. Click 'Load sample invoice' "
        "in the sidebar to explore the workspace."
    )

# ---------- FOOTER ----------
st.divider()
st.caption(
    "DocuStruct AI · Hackathon prototype · "
    "Always review extracted data before relying on it."
)
