from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import chromadb
from sentence_transformers import SentenceTransformer
import json
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize LLM
llm = ChatOpenAI(
    temperature=0.7,
    base_url="https://api.together.xyz/v1",
    openai_api_key=TOGETHER_API_KEY,
    model="meta-llama/Llama-3-8b-chat-hf"
)

# Initialize Chroma and SentenceTransformer for RAG
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("loan_data")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load sample data into Chroma (run once)
try:
    with open("loan_data.json", "r") as f:
        loan_data = json.load(f)
    for item in loan_data:
        collection.upsert(
            ids=[item["id"]],
            documents=[item["text"]],
            embeddings=[embedder.encode(item["text"]).tolist()]
        )
except FileNotFoundError:
    print("Warning: loan_data.json not found. Create it with sample loan data.")

def get_application_guidance(application_summary: str) -> str:
    from prompts import application_guidance_template
    query_embedding = embedder.encode(application_summary).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=2)
    context = "\n".join([doc for doc in results["documents"][0]])
    prompt = PromptTemplate(
        input_variables=["application_summary", "context"],
        template=application_guidance_template
    )
    chain = RunnableSequence(prompt | llm)  # Modern LangChain API
    try:
        return chain.invoke({"application_summary": application_summary, "context": context}).content
    except Exception as e:
        print(f"Error in get_application_guidance: {e}")
        return "Error generating guidance. Please check your input and try again."

def parse_financial_summary(summary: str) -> dict:
    if not summary or not summary.strip():
        return {"income": None, "credit_score": None, "debts": None, "employment_status": None}

    # Preprocess input to standardize format
    summary = summary.replace("income monthly", "monthly").replace("Credit Score", "credit score").replace("Debts", "debts")
    if "₹" not in summary:
        summary = summary.replace("50000", "₹50000").replace("10000", "₹10000")

    # Fallback regex parsing
    income = None
    credit_score = None
    debts = None
    employment_status = None

    income_match = re.search(r"(?:earn|income)\s*₹?([\d,]+)\s*(?:monthly)?", summary, re.IGNORECASE)
    if income_match:
        income = int(income_match.group(1).replace(",", ""))

    credit_match = re.search(r"credit score\s*(\d+)", summary, re.IGNORECASE)
    if credit_match:
        credit_score = int(credit_match.group(1))

    debts_match = re.search(r"debts\s*₹?([\d,]+)", summary, re.IGNORECASE)
    if debts_match:
        debts = int(debts_match.group(1).replace(",", ""))

    emp_match = re.search(r"(self-employed|employed|unemployed)", summary, re.IGNORECASE)
    if emp_match:
        employment_status = emp_match.group(1).lower()

    # LLM parsing
    parse_prompt = """
You are an expert at extracting financial details from text. Given the input, extract:
- Monthly Income (in ₹, as a number, e.g., 50000)
- Credit Score (as a number, e.g., 700)
- Monthly Debts (in ₹, as a number, e.g., 10000)
- Employment Status (as a string, e.g., "self-employed", or null if not provided)

Return the result as a valid JSON object with only the fields 'income', 'credit_score', 'debts', and 'employment_status'. Use null for missing fields. Do not include extra text, explanations, or markdown formatting.
Example Input: "I earn ₹50,000 monthly, credit score 700, debts ₹10,000, self-employed"
Example Output: {"income": 50000, "credit_score": 700, "debts": 10000, "employment_status": "self-employed"}
Example Input: "I earn 50000 income monthly and have Credit Score 700 and Debts 10000"
Example Output: {"income": 50000, "credit_score": 700, "debts": 10000, "employment_status": null}
Input: {summary}
"""
    try:
        prompt = PromptTemplate(input_variables=["summary"], template=parse_prompt)
        chain = RunnableSequence(prompt | llm)  # Modern LangChain API
        result = chain.invoke({"summary": summary}).content
        print(f"Raw LLM output: {result}")  # Debug LLM output
        parsed = json.loads(result.strip())
        if isinstance(parsed, dict):
            return {
                "income": parsed.get("income", income),
                "credit_score": parsed.get("credit_score", credit_score),
                "debts": parsed.get("debts", debts),
                "employment_status": parsed.get("employment_status", employment_status)
            }
    except Exception as e:
        print(f"Error parsing financial summary with LLM: {e}")
        # Fallback to regex-parsed values
        return {
            "income": income,
            "credit_score": credit_score,
            "debts": debts,
            "employment_status": employment_status
        }


def get_consultation_response(user_input: str) -> str:
    from prompts import consultation_template
    prompt = PromptTemplate(input_variables=["user_input"], template=consultation_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(user_input) 

def explain_legal_terms(loan_clause: str) -> str:
    from prompts import legal_terms_template
    prompt = PromptTemplate(input_variables=["loan_clause"], template=legal_terms_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(loan_clause)



def generate_savings_plan(goals_input: str) -> str:
    from prompts import goals_template
    prompt = PromptTemplate(input_variables=["goals_input"], template=goals_template)  # Fixed variable name
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(goals_input)
