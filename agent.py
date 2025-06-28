from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

llm = ChatOpenAI(
    temperature=0.7,
    base_url="https://api.together.xyz/v1",
    openai_api_key=TOGETHER_API_KEY,
    model="meta-llama/Llama-3-8b-chat-hf"
)

def get_consultation_response(user_input: str) -> str:
    from prompts import consultation_template
    prompt = PromptTemplate(input_variables=["user_input"], template=consultation_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(user_input)

def get_application_guidance(application_summary: str) -> str:
    from prompts import application_guidance_template
    prompt = PromptTemplate(input_variables=["application_summary"], template=application_guidance_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(application_summary)

def explain_legal_terms(loan_clause: str) -> str:
    from prompts import legal_terms_template
    prompt = PromptTemplate(input_variables=["loan_clause"], template=legal_terms_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(loan_clause)

def check_compliance(compliance_input: str) -> str:
    from prompts import compliance_template
    prompt = PromptTemplate(input_variables=["compliance_input"], template=compliance_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(compliance_input)

def generate_savings_plan(goals_input: str) -> str:
    from prompts import goals_template
    prompt = PromptTemplate(input_variables=["goals_input"], template=goals_template)  # Fixed variable name
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(goals_input)