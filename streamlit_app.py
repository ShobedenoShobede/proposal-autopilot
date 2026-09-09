import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import datetime

# --------------------------------------------------------------
# HARDCODED PAYPAL EMAIL - ALL DEPOSITS GO DIRECTLY HERE
# --------------------------------------------------------------
PAYPAL_EMAIL = "omni.growth.venture@gmail.com"  # <-- YOUR EMAIL IS LOCKED IN

st.set_page_config(page_title="Freelance Proposal Pro", page_icon="📄", layout="centered")

st.title("📄 Freelance Proposal + Deposit Collector")
st.markdown("Generate a professional PDF proposal and collect a **50% deposit** instantly via PayPal.")

# --------------------------------------------------------------
# USER INPUT FORM
# --------------------------------------------------------------
with st.form("proposal_form"):
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client Name", placeholder="e.g., Acme Corp")
        hourly_rate = st.number_input("Your Hourly Rate ($)", min_value=5.0, value=75.0, step=5.0)
    with col2:
        project_name = st.text_input("Project Name", placeholder="e.g., Website Redesign")
        estimated_hours = st.number_input("Estimated Hours", min_value=1.0, value=20.0, step=1.0)

    project_desc = st.text_area("Detailed Project Scope", height=150, 
                                placeholder="Describe exactly what you will deliver...")
    
    submitted = st.form_submit_button("🚀 Generate Proposal & Deposit Link")

# --------------------------------------------------------------
# PDF GENERATION FUNCTION
# --------------------------------------------------------------
def generate_pdf(client, project, desc, rate, hours):
    total = rate * hours
    deposit = total / 2
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 72

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(72, y, "Freelance Service Proposal")
    y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y, f"Prepared for: {client}")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(72, y, f"Project: {project}")
    y -= 20
    c.drawString(72, y, f"Date: {datetime.datetime.now().strftime('%B %d, %Y')}")
    y -= 40

    # Scope
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y, "Scope of Work:")
    y -= 20
    c.setFont("Helvetica", 11)
    for line in desc.split("\n"):
        if y < 72:
            c.showPage()
            y = height - 72
            c.setFont("Helvetica", 11)
        c.drawString(72, y, f"• {line[:80]}")
        y -= 16

    # Financials
    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y, "Financial Summary")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(72, y, f"Hourly Rate:         ${rate:.2f}")
    y -= 18
    c.drawString(72, y, f"Estimated Hours:     {hours}")
    y -= 18
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, f"Total Price:         ${total:.2f}")
    y -= 18
    c.setFont("Helvetica", 12)
    c.drawString(72, y, f"Deposit (50% due now): ${deposit:.2f}")

    # Footer / Payment instructions
    y -= 40
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(72, y, "Payment instructions: Click the PayPal button on the website to secure your deposit.")
    c.drawString(72, y - 15, "Remaining balance due upon project completion.")

    c.save()
    buffer.seek(0)
    return buffer, total, deposit

# --------------------------------------------------------------
# PROCESSING LOGIC
# --------------------------------------------------------------
if submitted:
    if not client_name or not project_desc or not project_name:
        st.error("Please fill in all fields (Client, Project Name, and Scope).")
    else:
        total_price = hourly_rate * estimated_hours
        deposit_due = total_price / 2

        # 1. Generate PDF
        pdf_buffer, total, deposit = generate_pdf(client_name, project_name, project_desc, hourly_rate, estimated_hours)
        
        st.success(f"✅ Proposal ready! Total: ${total:.2f} | Deposit Required: ${deposit:.2f}")

        # 2. Download Button
        st.download_button(
            label="📥 Download PDF Proposal",
            data=pdf_buffer,
            file_name=f"Proposal_{client_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

        st.divider()
        st.subheader("💳 Pay 50% Deposit to Lock in Your Slot")

        # 3. DYNAMIC PAYPAL HTML BUTTON (Hardcoded to your email)
        paypal_html = f"""
        <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
            <input type="hidden" name="cmd" value="_xclick">
            <input type="hidden" name="business" value="{PAYPAL_EMAIL}">
            <input type="hidden" name="lc" value="US">
            <input type="hidden" name="item_name" value="Deposit for {project_name}">
            <input type="hidden" name="amount" value="{deposit:.2f}">
            <input type="hidden" name="currency_code" value="USD">
            <input type="hidden" name="button_subtype" value="services">
            <input type="hidden" name="no_note" value="1">
            <input type="hidden" name="shipping" value="0.00">
            <input type="hidden" name="return" value="https://your-streamlit-app.com/thank-you">
            <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_paynowCC_LG.gif" 
                   border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
        </form>
        """
        st.markdown(paypal_html, unsafe_allow_html=True)
        st.caption(f"💰 {deposit:.2f} USD will be charged to your client. You get paid instantly to {PAYPAL_EMAIL}")
        
        # --- VIRAL REFERRAL ENGINE (Add this to app.py) ---
        st.divider()
        st.subheader("🔄 Share & Earn (Free Proposals)")
        
        # Generate a unique ID based on their session
        import hashlib
        
        if "referral_id" not in st.session_state:
            st.session_state.referral_id = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8]
        
        ref_link = f"https://proposal-autopilot-wjdcknhjrbchzcy8ydztas.streamlit.app/?ref={st.session_state.referral_id}"
        
        st.caption("Refer a friend. When they generate their first proposal, you both get 10% off your next deposit.")
        st.code(ref_link, language="text")
        st.caption("📊 Share this link on LinkedIn, Twitter, or in your freelancer groups.")

        st.info("📌 **Next Step:** Send the PDF to your client, and direct them to this page to pay the deposit.")
