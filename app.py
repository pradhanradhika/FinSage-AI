import streamlit as st
from agent import get_consultation_response, parse_financial_summary,get_application_guidance, explain_legal_terms, check_compliance, generate_savings_plan
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
    st.header("Loan Application Assistant")
    st.markdown("Enter your financial details for quick loan guidance.")
    with st.form("application_form"):
        financial_summary = st.text_area(
            "Describe Your Financial Situation:",
            placeholder="e.g., I earn ₹50,000 monthly, have a 700 credit score, and ₹10,000 in debts.",
            help="Include income, credit score, debts, or employment details."
        )
        loan_clause = st.text_area(
            "Paste a Loan Clause (Optional):",
            placeholder="e.g., 'A prepayment penalty of $500 applies...'",
            help="For explanation of loan terms."
        )

        submitted = st.form_submit_button("Get Guidance")
        if submitted:
            if not financial_summary or not financial_summary.strip():
                st.warning("Please provide a valid financial summary (e.g., income, credit score, debts).")
                parsed_data = {"income": None, "credit_score": None, "debts": None, "employment_status": None}
                summary = "**Application Summary**:\n\nIncome: Not Provided\nCredit Score: Not Provided\nDebts: Not Provided\nEmployment Status: Not Provided"
            else:
                with st.spinner("Analyzing your application..."):
                    parsed_data = parse_financial_summary(financial_summary)
                    summary = f"""**Application Summary**:
Income: {parsed_data.get('income', 'Not Provided')}
Credit Score: {parsed_data.get('credit_score', 'Not Provided')}
Debts: {parsed_data.get('debts', 'Not Provided')}
Employment Status: {parsed_data.get('employment_status', 'Not Provided')}
"""
                    ai_feedback = get_application_guidance(summary)
                    st.success("Application Feedback:")
                    st.markdown(ai_feedback, unsafe_allow_html=True)

        # Display parsed summary
        if submitted and summary:
            st.info("Parsed Details:")
            st.markdown(summary, unsafe_allow_html=True)

        # Progress Bar
        parsed_data = parsed_data if submitted else parse_financial_summary(financial_summary) if financial_summary else {}
        completeness = sum([
            25 if parsed_data.get('income') is not None and parsed_data.get('income') != 'Not Provided' else 0,
            25 if parsed_data.get('credit_score') is not None and parsed_data.get('credit_score') != 'Not Provided' else 0,
            25 if parsed_data.get('debts') is not None and parsed_data.get('debts') != 'Not Provided' else 0,
            25 if parsed_data.get('employment_status') is not None and parsed_data.get('employment_status') != 'Not Provided' else 0
        ])
        st.progress(completeness / 100.0)
        missing = []
        if parsed_data.get('income') is None or parsed_data.get('income') == 'Not Provided': missing.append("Income")
        if parsed_data.get('credit_score') is None or parsed_data.get('credit_score') == 'Not Provided': missing.append("Credit Score")
        if parsed_data.get('debts') is None or parsed_data.get('debts') == 'Not Provided': missing.append("Debts")
        if parsed_data.get('employment_status') is None or parsed_data.get('employment_status') == 'Not Provided': missing.append("Employment Status")
        st.markdown(f"**Application Completeness: {completeness}%**")
        if missing and submitted:
            st.warning(f"Please provide: {', '.join(missing)}")

        if loan_clause and submitted:
            clause_explanation = explain_legal_terms(loan_clause)
            st.info("Loan Clause Explanation:")
            st.markdown(clause_explanation, unsafe_allow_html=True)
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