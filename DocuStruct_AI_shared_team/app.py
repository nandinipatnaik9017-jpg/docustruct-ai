
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
    /* Main page */
    .stApp {
        background: #F7F9FC;
        color: #1E293B;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1320px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #163A5F;
    }

    /* Hero banner */
    .hero {
        padding: 2rem;
        border: 1px solid #DCE8F5;
        border-radius: 18px;
        background: linear-gradient(120deg, #FFFFFF 0%, #EAF3FF 100%);
        color: #163A5F;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 18px rgba(30, 64, 110, 0.05);
    }

    .hero h1 {
        color: #163A5F;
        font-size: 2.25rem;
        font-weight: 750;
        margin-top: 0.5rem;
        margin-bottom: 0.45rem;
    }

    .hero p {
        color: #52657A;
        font-size: 1rem;
        margin-bottom: 0;
    }

    /* Workflow section labels */
    .section-label {
        display: inline-block !important;
        background: #E8F0FE !important;
        color: #1D4ED8 !important;
        border: 1px solid #C7D7FE !important;
        padding: 6px 12px !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        margin-bottom: 10px !important;
        opacity: 1 !important;
    }

    /* Dashboard metrics */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(30, 64, 110, 0.035);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
    }

    div[data-testid="stMetricValue"] {
        color: #163A5F;
        font-weight: 750;
    }

    /* Buttons */
    div.stButton > button,
    div.stDownloadButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 10px;
        font-weight: 650;
        min-height: 2.7rem;
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
        background: #2563EB;
        border-color: #2563EB;
        color: #FFFFFF;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        border-color: #2563EB;
        color: #1D4ED8;
    }

    /* Input fields */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 9px;
    }

    /* Informational note */
    .note {
        border: 1px solid #DCE8F5;
        border-radius: 12px;
        padding: 14px 16px;
        background: #EFF6FF;
        color: #334155;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    /* Dividers */
    hr {
        border-color: #E2E8F0;
    }

    /* Responsive headings */
    @media (max-width: 768px) {
        .hero {
            padding: 1.25rem;
        }

        .hero h1 {
            font-size: 1.7rem;
        }

        .block-container {
            padding-top: 1rem;
        }
    }

    /* Force light backgrounds for common Streamlit components */
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background-color: #F7F9FC;
    }

    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background-color: #F7F9FC;
        color: #1E293B;
    }

    /* Cards and expandable sections */
    [data-testid="stExpander"],
    [data-testid="stExpander"] details,
    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] section {
        background-color: #FFFFFF;
        color: #1E293B;
        border-color: #E2E8F0;
    }

    /* Form and input containers */
    [data-testid="stForm"],
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-color: #E2E8F0;
    }

    /* Text input backgrounds */
    input,
    textarea,
    [data-baseweb="input"] input {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        -webkit-text-fill-color: #1E293B !important;
    }

    /* Code blocks and preformatted text */
    [data-testid="stCode"],
    pre {
        background-color: #F1F5F9 !important;
        color: #1E293B !important;
    }

    /* Fix text contrast across the light interface */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        color: #1E293B !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] small {
        color: #334155 !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #64748B !important;
    }

    /* Metric labels and values */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color: #64748B !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #163A5F !important;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
        border: 1px solid #DCE4EF !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploader"] *,
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] small {
        color: #334155 !important;
    }

    [data-testid="stFileUploader"] button {
        background: #EAF2FF !important;
        color: #1D4ED8 !important;
        border: 1px solid #BFD4FE !important;
    }

    /* Normal buttons */
    div.stButton > button,
    div.stDownloadButton > button {
        background: #FFFFFF;
        color: #1D4ED8 !important;
        border: 1px solid #CBD5E1;
    }

    div.stButton > button[kind="primary"] {
        background: #2563EB !important;
        color: #FFFFFF !important;
    }

    /* Captions and secondary text */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #64748B !important;
    }

    /* Success messages */
    [data-testid="stAlert"] p {
        color: #1E293B !important;
    }

    /* Improve sidebar brand title and subtitle visibility */
    [data-testid="stSidebar"] h2 {
        color: #163A5F !important;
        font-weight: 750 !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #64748B !important;
        opacity: 1 !important;
    }

    /* Sidebar subtitle: darker and easier to read */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #475569 !important;
        opacity: 1 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #475569 !important;
        opacity: 1 !important;
    }

    /* PDF uploader: add comfortable inner spacing */
    [data-testid="stFileUploader"] {
        padding: 16px !important;
        box-sizing: border-box !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploader"] section {
        padding: 12px !important;
        box-sizing: border-box !important;
        border-radius: 8px !important;
    }

    [data-testid="stFileUploader"] label {
        padding: 4px 6px !important;
        color: #334155 !important;
    }

    [data-testid="stFileUploader"] small {
        color: #64748B !important;
    }

/* Fix uploaded PDF filename visibility */
[data-testid="stFileUploader"] {
    background-color: #ffffff !important;
    color: #1e293b !important;
}

[data-testid="stFileUploader"] section {
    background-color: #f8fafc !important;
    color: #1e293b !important;
}

[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #dbe3ef !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
    color: #1e293b !important;
}

/* Fix uploaded PDF card and filename contrast */
[data-testid="stFileUploaderFile"] {
    background-color: #ffffff !important;
    border: 1px solid #dbe3ef !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFile"] * {
    color: #1e293b !important;
}

[data-testid="stFileUploaderFile"] a {
    color: #1d4ed8 !important;
}

[data-testid="stFileUploaderFile"] svg {
    fill: #1e293b !important;
    color: #1e293b !important;
}

/* Strong override for the uploaded-file preview */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] > div {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #1e293b !important;
    border-color: #dbe3ef !important;
}

/* Keep the filename and file size readable */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] *,
[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"],
[data-testid="stFileUploader"] [data-testid="stFileUploaderFileDetails"] {
    color: #1e293b !important;
}

/* Override dark backgrounds on nested elements */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] div,
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] span {
    background-color: transparent !important;
}

/* Preserve a light file-preview card */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
    border: 1px solid #dbe3ef !important;
    border-radius: 10px !important;
}

/* Fix uploaded PDF filename chip */
[data-testid="stFileChip"] {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #dbe3ef !important;
    border-radius: 10px !important;
}

[data-testid="stFileChip"] * {
    color: #1e293b !important;
}

[data-testid="stFileChip"] svg {
    color: #1e293b !important;
    fill: #1e293b !important;
}

/* High-contrast workflow section labels */
.section-label {
    display: inline-block !important;
    background-color: #DBEAFE !important;
    color: #1D4ED8 !important;
    padding: 6px 12px !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    margin-bottom: 8px !important;
    opacity: 1 !important;
}

/* Make section headings readable on the light theme */
h1, h2, h3 {
    color: #172554 !important;
    opacity: 1 !important;
}

/* Fix invoice review form text contrast */
[data-testid="stForm"] label,
[data-testid="stForm"] label p,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #172554 !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* Make entered invoice values readable */
[data-testid="stForm"] input,
[data-testid="stForm"] textarea,
[data-testid="stForm"] [data-baseweb="input"] input {
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
    background-color: #ffffff !important;
    border-color: #cbd5e1 !important;
}

/* Fix placeholders */
[data-testid="stForm"] input::placeholder,
[data-testid="stForm"] textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    opacity: 1 !important;
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

with c1:
    st.markdown("##### Document status")
    if metric_status == "Valid":
        st.success("✓ Valid")
    elif metric_status == "Needs review":
        st.warning("⚠ Needs review")
    else:
        st.info("Waiting for invoice")

with c2:
    st.markdown("##### Vendor")
    st.markdown(f"**{metric_vendor}**")

with c3:
    st.markdown("##### Invoice total")
    st.markdown(f"**{metric_total}**")

with c4:
    st.markdown("##### Validation issues")
    if metric_issues == "—":
        st.markdown("**—**")
    elif metric_issues == "0":
        st.success("0 issues")
    else:
        st.warning(f"{metric_issues} issues")

st.divider()


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
    '<div class="note">Upload an invoice PDF to extract data using AI. '
    'Review the extracted fields, correct any errors, validate the invoice, '
    'and download the results as JSON or CSV. '
    'You can also load the sample invoice to explore the workflow.</div>',
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

    if st.session_state.reviewed:
        st.success("✓ Invoice reviewed and saved successfully.")
    else:
        st.caption("📝 Review the extracted fields and save your changes.")




# ---------- VALIDATION ----------
    st.divider()
    st.markdown(
        '<div class="section-label">Step 03</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Validation results")

    if errors:
        st.warning(
            f"Found {len(errors)} issue(s). "
            "Please review the details below and correct the invoice."
        )

        for error in errors:
            st.markdown(
                f"""
                <div style="
                    background-color: #FFF7ED;
                    border: 1px solid #FED7AA;
                    border-left: 4px solid #EA580C;
                    border-radius: 8px;
                    padding: 10px 14px;
                    margin: 8px 0;
                    color: #9A3412;
                ">⚠️ {error}</div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.success(
            "✓ All validation checks passed. The invoice is valid."
        )

    if st.session_state.reviewed:
        st.caption("Your latest form submission has been saved.")


    # ---------- EXPORT ----------
   
    
    st.divider()
    st.markdown(
        '<div class="section-label">Step 04</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Export reviewed data")

    can_export = st.session_state.reviewed and not errors

    if can_export:
        st.success("Invoice reviewed and validated. Ready to export.")
    elif not st.session_state.reviewed:
        st.info("Save the reviewed invoice before exporting.")
    else:
        st.warning("Fix all validation issues before exporting.")

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
            disabled=not can_export,
        )

    with col2:
        st.download_button(
            "⬇ Download CSV",
            data=csv_data,
            file_name="invoice.csv",
            mime="text/csv",
            use_container_width=True,
            disabled=not can_export,
        )


# ---------- FOOTER ----------
st.divider()
st.caption(
    "DocuStruct AI · Hackathon prototype · "
    "Always review extracted data before relying on it."
)
