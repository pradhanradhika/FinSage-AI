import streamlit as st
from agent import get_consultation_response, get_application_guidance, explain_legal_terms, check_compliance, generate_savings_plan
from pathlib import Path

# Set page configuration
st.set_page_config(page_title="Loan & Mortgage Helper", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for visual appeal
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {background-color: #007bff; color: white; border-radius: 8px; padding: 10px 20px;}
    .stButton>button:hover {background-color: #0056b3;}
    .stTabs {background-color: #ffffff; border-radius: 10px; padding: 20px;}
    .stMarkdown h1 {color: #2c3e50; font-family: 'Arial', sans-serif;}
    .stMarkdown h2, h3 {color: #34495e;}
    .stSpinner {color: #007bff;}
    .success-box {background-color: #e7f3e7; padding: 15px; border-radius: 8px; border: 1px solid #28a745;}
    .info-box {background-color: #e6f3ff; padding: 15px; border-radius: 8px; border: 1px solid #007bff;}
    .stTextInput, .stNumberInput, .stSlider, .stSelectbox, .stTextArea {background-color: #ffffff; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

st.title("🏦FinSage: AI-Driven Loan Management and financial advisory system")
st.markdown("Your friendly AI-powered assistant for loan consultations, application guidance, regulatory compliance, and financial goal planning.")

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Loan Consultation", "📄 Loan Application Assistant", "🎯 Financial Goals Tracker"])

# ------------- TAB 1: LOAN CONSULTATION -----------------
with tab1:
    st.header("Loan & Mortgage Consultation")
    st.markdown("Answer a few questions to get personalized loan recommendations.")

    with st.form("consultation_form"):
        col1, col2 = st.columns(2)
        with col1:
            loan_type = st.selectbox("Select Loan Type:", ["Home Loan", "Auto Loan", "Business Loan", "Personal Loan"], help="Choose the type of loan you're interested in.")
            income = st.number_input("Monthly Income (₹):", min_value=0.0, step=1000.0, format="%.2f", help="Enter your net monthly income after taxes.")
        with col2:
            credit_score = st.slider("Estimated Credit Score:", 300, 850, 650, help="Select your credit score (300-850).")
            loan_amount = st.number_input("Desired Loan Amount (₹):", min_value=0.0, step=1000.0, format="%.2f", help="Enter the loan amount you need.")

        submitted = st.form_submit_button("💡 Get Loan Recommendation")
        if submitted:
            with st.spinner("Analyzing your financial profile..."):
                user_input = (
                    f"Loan Type: {loan_type}\n"
                    f"Monthly Income: ₹{income:,.2f}\n"
                    f"Credit Score: {credit_score}\n"
                    f"Loan Amount Needed: ₹{loan_amount:,.2f}"
                )
                response = get_consultation_response(user_input)
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("Here's Your Personalized Loan Recommendation:")
                st.markdown(response, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# ------------- TAB 2: LOAN APPLICATION ASSISTANT -----------------
with tab2:
    st.header("📄 Loan Application Assistant")
    st.markdown("Upload documents, provide financial details, and get guidance on your application and compliance.")

    with st.form("application_form"):
        st.subheader("Financial Documents")
        col1, col2 = st.columns(2)
        with col1:
            tax_return = st.file_uploader("Last 2 Years of Tax Returns (PDF)", type=["pdf"], help="Upload tax returns for income verification.")
            pay_stubs = st.file_uploader("Recent Pay Stubs (PDF)", type=["pdf"], help="Upload latest pay stubs (last 3 months).")
        with col2:
            bank_statements = st.file_uploader("Recent Bank Statements (PDF)", type=["pdf"], help="Upload bank statements for 3-6 months.")
            id_proof = st.file_uploader("ID Proof (PDF)", type=["pdf"], help="Upload a government-issued ID (e.g., Aadhaar, Passport).")

        st.subheader("Financial Details")
        col3, col4 = st.columns(2)
        with col3:
            income_details = st.text_input("Monthly Income (₹):", placeholder="e.g., 50000", help="Your current monthly income after taxes.")
            debts = st.text_input("Total Monthly Debts (₹):", placeholder="e.g., 10000", help="Sum of all monthly debt payments.")
        with col4:
            employment_status = st.selectbox("Employment Status:", ["Employed", "Self-Employed", "Unemployed", "Retired"], help="Your current employment status.")
            years_employed = st.number_input("Years at Current Job:", min_value=0.0, step=0.5, format="%.1f", help="How long have you been at your current job?")

        other_docs = st.text_area("Additional Documents or Notes:", placeholder="e.g., Property documents", help="Mention other relevant documents or details.")

        st.subheader("Regulatory Compliance and Loan Terms")
        loan_clause = st.text_area("Paste a Loan Clause (Optional):", placeholder="e.g., 'A prepayment penalty of $500 applies if the loan is paid off within 3 years.'", help="Paste a loan clause to get a simple explanation.")
        document_summary = st.text_area("Summarize Key Loan Document Details (Optional):", placeholder="e.g., Loan Amount: ₹20,00,000, Interest Rate: 7%, Term: 20 years, Fees: ₹10,000", help="Enter key details from your loan agreement for review.")

        submitted = st.form_submit_button("✅ Validate & Get Guidance")
        if submitted:
            with st.spinner("Checking your application and analyzing compliance..."):
                # Application Summary
                summary = f"""
**Application Summary**:
- **Documents Uploaded**:
  - Tax Returns: {"Provided" if tax_return else "Missing"}
  - Pay Stubs: {"Provided" if pay_stubs else "Missing"}
  - Bank Statements: {"Provided" if bank_statements else "Missing"}
  - ID Proof: {"Provided" if id_proof else "Missing"}
  - Other Documents/Notes: {other_docs if other_docs else "None"}
- **Financial Details**:
  - Monthly Income: {income_details if income_details else "Not Provided"}
  - Monthly Debts: {debts if debts else "Not Provided"}
  - Employment Status: {employment_status}
  - Years at Current Job: {years_employed if years_employed else "Not Provided"}
"""
                ai_feedback = get_application_guidance(summary)
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("🧾 Application Feedback and Next Steps:")
                st.markdown(ai_feedback, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Progress Bar
                completeness = 0
                if tax_return: completeness += 25
                if pay_stubs: completeness += 25
                if bank_statements: completeness += 25
                if id_proof: completeness += 25
                st.progress(completeness / 100.0)
                st.markdown(f"**Application Completeness: {completeness}%**")

                # Legal Terms Explanation
                if loan_clause:
                    with st.spinner("Explaining loan clause..."):
                        clause_explanation = explain_legal_terms(loan_clause)
                        st.markdown('<div class="info-box">', unsafe_allow_html=True)
                        st.info("📜 Loan Clause Explanation:")
                        st.markdown(clause_explanation, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                # Compliance Check
                compliance_input = f"""
Documents Provided:
- Tax Returns: {"Provided" if tax_return else "Missing"}
- Pay Stubs: {"Provided" if pay_stubs else "Missing"}
- Bank Statements: {"Provided" if bank_statements else "Missing"}
- ID Proof: {"Provided" if id_proof else "Missing"}
Document Summary: {document_summary if document_summary else "Not Provided"}
"""
                with st.spinner("Checking regulatory compliance..."):
                    compliance_feedback = check_compliance(compliance_input)
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("⚖️ Regulatory Compliance Check:")
                    st.markdown(compliance_feedback, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

# ------------- TAB 3: FINANCIAL GOALS TRACKER -----------------
with tab3:
    st.header("🎯 Financial Goals Tracker")
    st.markdown("Plan your financial future by setting goals and generating a savings plan.")

    with st.form("goals_form"):
        st.subheader("Financial Overview")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹):", min_value=0.0, step=1000.0, format="%.2f", help="Enter your net monthly income after taxes.")
            expenses = st.number_input("Monthly Expenses (₹):", min_value=0.0, step=1000.0, format="%.2f", help="Enter your total monthly expenses.")
        with col2:
            savings = st.number_input("Current Savings (₹):", min_value=0.0, step=1000.0, format="%.2f", help="Enter your current savings amount.")

        st.subheader("Add Your Goals")
        num_goals = st.number_input("Number of Goals:", min_value=1, max_value=5, step=1, help="Select how many financial goals you want to set.")
        goals_list = []
        for i in range(num_goals):
            st.markdown(f"**Goal {i+1}:**")
            col3, col4 = st.columns(2)
            with col3:
                name = st.text_input(f"Goal Name {i+1}:", key=f"goal_name_{i}", placeholder="e.g., Buy a Car", help="Name your financial goal.")
                amount = st.number_input(f"Target Amount (₹) {i+1}:", min_value=0.0, step=10000.0, format="%.2f", key=f"goal_amt_{i}", help="Enter the target amount for this goal.")
            with col4:
                years = st.number_input(f"Target in Years {i+1}:", min_value=1, max_value=30, step=1, key=f"goal_years_{i}", help="How many years to achieve this goal?")
            if name and amount > 0:
                goals_list.append({"name": name, "amount": amount, "years": years})

        submitted = st.form_submit_button("📈 Generate Savings Plan")
        if submitted:
            if income and expenses and goals_list:
                with st.spinner("Generating your savings plan..."):
                    goals_input = f"""
Monthly Income: ₹{income:,.2f}
Monthly Expenses: ₹{expenses:,.2f}
Current Savings: ₹{savings:,.2f}
Goals:
{chr(10).join([f"- {goal['name']}: ₹{goal['amount']:,.2f} in {goal['years']} years" for goal in goals_list])}
"""
                    response = generate_savings_plan(goals_input)
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("📊 Your Savings Plan:")
                    st.markdown(response, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Please fill all required fields (income, expenses, and at least one valid goal).")